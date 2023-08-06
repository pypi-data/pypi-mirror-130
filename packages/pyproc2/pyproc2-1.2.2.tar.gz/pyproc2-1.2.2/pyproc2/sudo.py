import subprocess
import getpass
import warnings
import time
class SudoWarning(Warning):pass
class SudoError(Exception):pass
def getpoll(poll):
    if poll is None:
        return -1
    return poll
def sudo(cmd,user=''):
    if user:
        args=['sudo',cmd,'-u',user]
    else:
        args=['sudo', cmd]
    p=subprocess.Popen(args,stderr=subprocess.PIPE,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    time.sleep(0.1)
    if getpoll(p.poll())>0:
        stderr=p.stderr.read()
        raise SudoError(f'sudo failed: {stderr.decode()}')
    return p
