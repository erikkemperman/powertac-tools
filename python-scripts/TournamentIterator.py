#!/usr/bin/python3
'''
Extracts state logs from compressed game files in a directory that presumably
contains the game logs from a tournament. Call stateLogIter(dir) where
dir is the directory containing the game logs. This returns an iterator over
paths to state logs extracted from the tournament.
'''
# Uses Python 3.4 or later

import re, os, tarfile, subprocess
from pathlib import Path

def stateLogIter (tournamentDir, sessionType='sim'):
    '''
    Returns a generator of state logs extracted from a directory
    of compressed game logs
    '''
    path = Path(tournamentDir)
    return (extractLog(name, sessionType, 'state')
            for name in path.glob('game-*-{}-logs.tar.gz'.format(sessionType)))

def traceLogIter (tournamentDir, sessionType='sim'):
    '''
    Returns a generator of trace logs extracted from a directory
    of compressed game logs
    '''
    path = Path(tournamentDir)
    return (extractLog(name, sessionType, 'trace')
            for name in path.glob('game-*-{}-logs.tar.gz'.format(sessionType)))


def extractLog (gameLog, sessionType, logType):
    '''
    Extracts logs from compressed game log file, if not already extracted.
    Returns path to state log.
    '''
    gameIdRe = re.compile('game-(\d+)-{}-logs.tar.gz'.format(sessionType))
    path = Path(gameLog)
    m = gameIdRe.search(str(path))
    if m:
        gameId = m.group(1)
        logPath = Path(path.parent, 'log',
                       'powertac-{}-{}.{}'.format(sessionType, gameId, logType))
        if not logPath.exists():
            #if os.name == "posix":
            #    p1 = subprocess.Popen(['tar', 'xzf', path.name], shell = True, cwd = str(path.parent))
            #    p1.wait()
            #elif os.name == "nt":
            pathdir = path.parent
            path = path.as_posix()
            pathdir = pathdir.as_posix()
            tar = tarfile.open(path)
            tar.extractall(pathdir)
            tar.close()
        return logPath
    else:
        gameId = 'xx'
        print('Failed to find game ID in ' + str(path))
        return False
