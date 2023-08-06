#!/usr/bin/env python3
'''launches new NCS instances and starts the NeoLoad LoadGenerator agent on them'''
import argparse
from concurrent import futures
import datetime
import json
import logging
import os
import subprocess
import sys
import time
# third-party module(s)
import requests
# neocortix modules
import ncscli.ncs as ncs
import ncscli.batchRunner as batchRunner
import ncscli.tellInstances as tellInstances
import startForwarders  # expected to be in the same directory


neoloadVersion = '7.10'  # '7.6', '7.7' and '7.10' are currently supported
nlWebWanted = False

class g_:
    signaled = False
    interrupted = False


class neoloadFrameProcessor(batchRunner.frameProcessor):
    '''defines details for installing Neotys Load Generator agent on a worker'''

    def installerCmd( self ):
        if neoloadVersion == '7.10':
            return 'nlAgent/install_7-10.sh'
        elif neoloadVersion == '7.7':
            return 'nlAgent/install_7-7.sh'
        else:
            return 'nlAgent/install_7-6.sh'

def sigtermSignaled():
    return g_.signaled

def commandInstance( inst, cmd, timeLimit ):
    deadline = time.time() + timeLimit
    sshSpecs = inst['ssh']
    #logInstallerOperation( iid, ['connect', sshSpecs['host'], sshSpecs['port']] )
    with subprocess.Popen(['ssh',
                    '-p', str(sshSpecs['port']),
                    '-o', 'ServerAliveInterval=30',
                    '-o', 'ServerAliveCountMax=12',
                    sshSpecs['user'] + '@' + sshSpecs['host'], cmd],
                    encoding='utf8',
                    #stdout=subprocess.PIPE,  # subprocess.PIPE subprocess.DEVNULL
                    ) as proc:  # stderr=subprocess.PIPE
        #logInstallerOperation( iid, ['command', cmd] )
        #stderrThr = threading.Thread(target=trackStderr, args=(proc,))
        #stderrThr.start()
        abbrevIid = inst['instanceId'][0:16]
        while time.time() < deadline:
            proc.poll() # sets proc.returncode
            if proc.returncode == None:
                logger.info( 'waiting for command on instance %s', abbrevIid)
            else:
                if proc.returncode == 0:
                    logger.debug( 'command succeeded on instance %s', abbrevIid )
                else:
                    logger.warning( 'instance %s gave returnCode %d', abbrevIid, proc.returncode )
                break
            if sigtermSignaled():
                break
            if g_.interrupted:
                break
            time.sleep(5)
        proc.poll()
        returnCode = proc.returncode if proc.returncode != None else 124 # declare timeout if no rc
        #if returnCode:
        #    logger.warning( 'command returnCode %s', returnCode )
        #if returnCode == 124:
        #    logInstallerEvent( 'timeout', args.instTimeLimit, iid )
        #else:
        #    logInstallerEvent('returncode', returnCode, iid )
        proc.terminate()
        try:
            proc.wait(timeout=5)
            if proc.returncode:
                logger.warning( 'ssh return code %d', proc.returncode )
        except subprocess.TimeoutExpired:
            logger.warning( 'ssh did not terminate in time' )
        #stderrThr.join()
        if returnCode:
            #logger.warning( 'terminating instance because installerFailed %s', iid )
            #terminateInstances( args.authToken, [iid] )
            #logOperation( 'terminateBad', [iid], '<recruitInstances>' )
            #purgeHostKeys( [inst] )
            return returnCode
        else:
            return 0
    return 1

def configureAgent( inst, port, timeLimit=500 ):
    iid = inst['instanceId']
    logger.debug( 'would configure agent on instance %s for port %d', iid[0:16], port )
    rc = 1
    # generate a command to modify agent.properties on the instance
    configDirPath = '~/neoload%s/conf' % neoloadVersion
    if nlWebWanted:
        cmd = "cat %s/nlweb.properties >> %s/agent.properties" % tuple( [configDirPath]*2 )
    else:
        cmd = ":"  # a null command
    cmd += " && sed -i 's/NCS_LG_PORT/%d/' ~/neoload%s/conf/agent.properties" % (port, neoloadVersion)
    cmd += " && sed -i 's/NCS_LG_HOST/%s/' ~/neoload%s/conf/agent.properties" % (forwarderHost, neoloadVersion)
    logger.debug( 'cmd: %s', cmd )
    rc = commandInstance( inst, cmd, timeLimit=timeLimit )
    return rc

def configureAgents( instances, ports, timeLimit=600 ):
    '''configure LG agents, in parallel'''
    returnCodes = []
    with futures.ThreadPoolExecutor( max_workers=len(instances) ) as executor:
        parIter = executor.map( configureAgent, instances, ports, timeout=timeLimit )
        returnCodes = [None] * len(instances)
        try:
            index = 0
            for returnCode in parIter:
                returnCodes[index] = returnCode
                index += 1
                time.sleep( .1 )
        except KeyboardInterrupt:
            logger.warning( 'interrupted, setting flag')
            g_.interrupted = True
            raise
        logger.debug( 'returnCodes: %s', returnCodes )
    return returnCodes

if __name__ == '__main__':
    # configure logger formatting
    logger = logging.getLogger(__name__)
    logFmt = '%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s'
    logDateFmt = '%Y/%m/%d %H:%M:%S'
    formatter = logging.Formatter(fmt=logFmt, datefmt=logDateFmt )
    logging.basicConfig(format=logFmt, datefmt=logDateFmt)
    #batchRunner.logger.setLevel(logging.DEBUG)  # for more verbosity
    logger.setLevel(logging.INFO)

    ap = argparse.ArgumentParser( description=__doc__, fromfile_prefix_chars='@',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter )
    ap.add_argument( '--forwarderHost', help='IP addr (or host name) of the forwarder host',
        default='localhost' )
    ap.add_argument( '--nWorkers', type=int, help='the number of agents to launch',
        default=10 )
    args = ap.parse_args()

    supportedVersions = ['7.6', '7.7', '7.10']
    if neoloadVersion not in supportedVersions:
        logger.error( 'version "%s" is not suppoprted; supported versions are %s',
            neoloadVersion, sorted( supportedVersions ) )
        sys.exit( 1 )

    dateTimeTag = datetime.datetime.now().strftime( '%Y-%m-%d_%H%M%S' )
    outDataDir = 'data/neoload_' + dateTimeTag

    # you may set forwarderHost manually here, to override auto-detect
    forwarderHost = args.forwarderHost
    if not forwarderHost:
        try:
            forwarderHost = requests.get( 'https://api.ipify.org' ).text
        except forwarderHost:
            logger.warning( 'could not get public ip addr of this host')
    if not forwarderHost:
        logger.error( 'forwarderHost not set')
        exit(1)
    
    authToken = os.getenv('NCS_AUTH_TOKEN') or 'YourAuthTokenHere'
    instTimeLimit = 13*60 if neoloadVersion in ['7.10'] else 30*60

    if nlWebWanted and not os.path.isfile( 'nlAgent/nlweb.properties'):
        logger.error( 'the file nlAgent/nlweb.properties was not found')
        sys.exit(1)
    try:
        # call runBatch to launch worker instances and install the load generator agent on them
        rc = batchRunner.runBatch(
            frameProcessor = neoloadFrameProcessor(),
            recruitOnly=True,
            pushDeviceLocs=False,
            commonInFilePath = 'nlAgent',
            authToken = authToken,
            encryptFiles=False,
            timeLimit = 60*60,
            instTimeLimit = instTimeLimit,
            filter = '{ "dar": "==100", "regions": ["usa"], "dpr": ">=48","ram:":">=5800000000","app-version": ">=2.1.14"}',
            outDataDir = outDataDir,
            nWorkers = args.nWorkers
        )
        if rc == 0:
            portRangeStart=7100
            launchedJsonFilePath = outDataDir +'/recruitLaunched.json'
            launchedInstances = []
            # get details of launched instances from the json file
            #TODO should get list of instances with good install, rather than all started instances
            with open( launchedJsonFilePath, 'r') as jsonInFile:
                try:
                    launchedInstances = json.load(jsonInFile)  # an array
                except Exception as exc:
                    logger.warning( 'could not load json (%s) %s', type(exc), exc )
                    sys.exit( 2 )
            launchedIids = [inst['instanceId'] for inst in launchedInstances ]
            startedInstances = [inst for inst in launchedInstances if inst['state'] == 'started' ]
            #logger.info( '%d instances were launched', len(startedInstances) )

            if neoloadVersion == '7.10':
                agentLogFilePath = '/root/.neotys/neoload/v7.10/logs/agent.log'
                starterCmd = 'cd ~/neoload7.10/ && /usr/bin/java -Xms512m -Xmx512m -Dvertx.disableDnsResolver=true -classpath $HOME/neoload7.10/.install4j/i4jruntime.jar:$HOME/neoload7.10/.install4j/launchera03c11da.jar:$HOME/neoload7.10/bin/*:$HOME/neoload7.10/lib/crypto/*:$HOME/neoload7.10/lib/*:$HOME/neoload7.10/lib/jdbcDrivers/*:$HOME/neoload7.10/lib/plugins/ext/* install4j.com.neotys.nl.agent.launcher.AgentLauncher_LoadGeneratorAgent start &'
            elif neoloadVersion == '7.7':
                agentLogFilePath = '/root/.neotys/neoload/v7.7/logs/agent.log'
                starterCmd = 'cd ~/neoload7.7/ && /usr/bin/java -Xmx512m -Dvertx.disableDnsResolver=true -classpath $HOME/neoload7.7/.install4j/i4jruntime.jar:$HOME/neoload7.7/.install4j/launchera03c11da.jar:$HOME/neoload7.7/bin/*:$HOME/neoload7.7/lib/crypto/*:$HOME/neoload7.7/lib/*:$HOME/neoload7.7/lib/jdbcDrivers/*:$HOME/neoload7.7/lib/plugins/ext/* install4j.com.neotys.nl.agent.launcher.AgentLauncher_LoadGeneratorAgent start &'
            else:
                agentLogFilePath = '/root/.neotys/neoload/v7.6/logs/agent.log'
                starterCmd = 'cd ~/neoload7.6/ && /usr/bin/java -Dneotys.vista.headless=true -Xmx512m -Dvertx.disableDnsResolver=true -classpath $HOME/neoload7.6/.install4j/i4jruntime.jar:$HOME/neoload7.6/.install4j/launcherc0a362f9.jar:$HOME/neoload7.6/bin/*:$HOME/neoload7.6/lib/crypto/*:$HOME/neoload7.6/lib/*:$HOME/neoload7.6/lib/jdbcDrivers/*:$HOME/neoload7.6/lib/plugins/ext/* install4j.com.neotys.nl.agent.launcher.AgentLauncher_LoadGeneratorAgentService start &'

            configuredInstances = []
            portMap = {}
            if True:  # nlWebWanted
                # configure the agent properties on each instance
                ports = list( range( portRangeStart, portRangeStart+len(startedInstances) ) )
                for index, inst in enumerate( startedInstances ):
                    iid = inst['instanceId']
                    portMap[iid] = index + portRangeStart
                returnCodes = configureAgents( startedInstances, ports, timeLimit=600 )
                for index, code in enumerate( returnCodes ):
                    if code==0:
                        configuredInstances.append( startedInstances[index] )
                    else:
                        iid = startedInstances[index].get('instanceId')
                        logger.info( 'inst %s was not configured properly', iid[0:8] )

            # start the agent on each instance 
            stepStatuses = tellInstances.tellInstances( configuredInstances, command=starterCmd,
                resultsLogFilePath=outDataDir +'/startAgents.jlog',
                timeLimit=30*60,
                knownHostsOnly=True
                )
            logger.debug( 'starter statuses: %s', stepStatuses )
            # make a list of instances where the agent was started
            goodIids = []
            for status in stepStatuses:
                if isinstance( status['status'], int) and status['status'] == 0:
                    goodIids.append( status['instanceId'])
                else:
                    logger.warning( 'could not start agent on %s', status['instanceId'][0:8] )
            goodInstances = [inst for inst in startedInstances if inst['instanceId'] in goodIids ]
            if goodInstances:
                time.sleep( 60 )
                # download the agent.log file from each instance
                stepStatuses = tellInstances.tellInstances( goodInstances,
                    download=agentLogFilePath, downloadDestDir=outDataDir +'/agentLogs',
                    timeLimit=30*60,
                    knownHostsOnly=True
                    )
                logger.debug( 'download statuses: %s', stepStatuses )
                # make a list of instances where the log file was downloaded and agent start is verified
                goodIids = []
                for status in stepStatuses:
                    if isinstance( status['status'], int) and status['status'] == 0:
                        iid = status['instanceId']
                        logFilePath = os.path.join( outDataDir, 'agentLogs', iid, 'agent.log' )
                        try:
                            with open( logFilePath, 'r' ) as logFile:
                                contents = logFile.read().rstrip()
                                if ' ERROR ' in contents:
                                    lastLine = contents.split('\n')[-1].strip()
                                    logger.warning( 'log for %s indicates error "%s"', iid[0:8], lastLine )
                                elif ': Agent started' not in contents:
                                    logger.warning( 'log for %s says it did not start', iid[0:8] )
                                else:
                                    goodIids.append( iid )
                        except Exception as exc:
                            logger.warning( 'exception reading log (%s) %s', type(exc), exc )
                    else:
                        logger.warning( 'could not download log from %s', status['instanceId'][0:8] )
                goodInstances = [inst for inst in goodInstances if inst['instanceId'] in goodIids ]
                with open( outDataDir + '/startedAgents.json','w' ) as outFile:
                    json.dump( goodInstances, outFile )

                # plot map of workers
                if os.path.isfile( outDataDir +'/startedAgents.json' ):
                    rc2 = subprocess.call( ['./plotAgentMap.py', '--dataDirPath', outDataDir],
                        stdout=subprocess.DEVNULL )
                    if rc2:
                        logger.warning( 'plotAgentMap exited with returnCode %d', rc2 )

                # start the ssh port-forwarding
                logger.info( 'would forward ports for %d instances', len(goodInstances) )
                forwarders = startForwarders.startForwarders( goodInstances,
                    forwarderHost=forwarderHost,
                    portMap=portMap,
                    portRangeStart=portRangeStart, maxPort=portRangeStart+100,
                    forwardingCsvFilePath=outDataDir+'/agentForwarding.csv'
                    )
                if len( forwarders ) < len( goodInstances ):
                    logger.warning( 'some instances could not be forwarded to' )
                logger.debug( 'forwarders: %s', forwarders )
                #TODO get iids only for successfully forwarded agents
                forwardedIids = [inst['instanceId'] for inst in goodInstances ]
                unusableIids = list( set(launchedIids) - set( forwardedIids) )
                if unusableIids:
                    logger.info( 'terminating %d unusable instances', len(unusableIids) )
                    ncs.terminateInstances( authToken, unusableIids )
            if launchedInstances:
                print( 'when you want to terminate these instances, use %s terminateAgents.py "%s"'
                    % (sys.executable, outDataDir))
        sys.exit( rc )
    except KeyboardInterrupt:
        logger.warning( 'an interuption occurred')
