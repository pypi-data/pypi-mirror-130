import os
import sys
from pwd import getpwuid as gpu
import subprocess
import time
import signal
import getpass
import platform
import warnings
import shlex
from .error import *
from . import tiocsti,fd,sudo,perm
class pyproc2(object):
    class signals:
        def __init__(self):
            self.__dict__.update({n:int(getattr(signal,n)) for n in dir(signal) if n.startswith('SI')})

        class Signalled:
            def stop(self):
                self.kill(pyproc2.signals.SIGSTOP)
                
            def cont(self):
                self.kill(pyproc2.signals.SIGCONT)
            def chld(self):
                self.kill(pyproc2.signals.SIGCHLD)
            def hup(self):
                self.kill(pyproc2.signals.SIGHUP)
            def term(self):
                self.kill(pyproc2.signals.SIGTERM)
        
    class SLEEPING:
        def __repr__(self):
            return 'SLEEPING'
    class RUNNING:
        def __repr__(self):
            return 'RUNNING'
    class UNKNOWN:
        def __repr__(self):
            return 'UNKNOWN'
    class STOPPED:
        def __repr__(self):
            return 'STOPPED'
    class _Process(signals.Signalled):
        def __init__(self,pid,proc_rm=None,owner=None):
            if proc_rm:
                proc_rm=str(proc_rm)
            
            self.pid=int(pid)

            self.path=os.path.join('/proc',str(pid))
            if not os.path.exists(self.path):
                raise ProcessLookupError("no such process: {}".format(self.pid))
            if not os.path.isdir(self.path):
                raise NotADirectoryError("not a directory")
            if 'status' not in os.listdir(self.path):
                raise FileNotFoundError
            self.fds=self.getfds()

            self.stdout=self.fds.stdout
            self.stdin=self.fds.stdin
            self.stderr=self.fds.stderr
            self.raw=open(os.path.join(self.path,'status')).read()
            self.data=[l.split(':',1) for l in self.raw.splitlines()]
            self.data=dict(self.data)
            self.data={k.lower().strip():v.lower().strip().replace('\t',' ') for k,v in self.data.items()}
            self.name=self['name']
            self.uid=os.stat(self.path).st_uid
            try:
                self.user=gpu(int(self.uid)).pw_name
            except KeyError:
                self.user='root'
            self.__owner=owner
                        #self.__dict__.update(self.data)
            
            self.statusdata=open(os.path.join(self.path,'stat')).read().split()
            self.cmd=open(os.path.join(self.path,'cmdline')).read().strip().replace('\x00',' ')
            if 'state' not in self.data:
                self.state=pyproc2().UNKNOWN
            else:
                stletter=self['state'].split()[0]
                if stletter.lower()=='s':
                    self.state=pyproc2().SLEEPING
                elif stletter.lower()=='r':
                    self.state=pyproc2().RUNNING
                elif stletter.lower()=='t':
                    self.state=pyproc2().STOPPED
                else:
                    self.state=pyproc2().UNKNOWN
        def communicate(self,prompt):
            self.stdin.write(prompt)
            return self.stdout.read()
        def getfds(self):
            try:
                self.fds=fd.Fds([tiocsti.TioFile(os.path.join(self.path,'fd',x)) for x in os.listdir(os.path.join(self.path,'fd'))],perm.NotExisting)
            except PermissionError:
                self.fds=perm.BlockedFD()
            return self.fds
        def __iter__(self):
            return iter([self])
        def __getitem__(self,i):
            return self.data[i]
        def __setitem__(self,n,i):
            self.data[n]=i
        def count_cpu(self):
            self.utime=int(self.statusdata[13])
            self.stime=int(self.statusdata[14])
            self.cutime=int(self.statusdata[15])
            self.cstime=int(self.statusdata[16])
            self.ttime=self.stime+self.utime+self.cutime+self.cstime
            self.startup=int(self.statusdata[21])
            secs=pyproc2().uptime - self.startup/pyproc2().CLK
            


            return 100*((self.ttime/pyproc2().CLK)/secs)
        def getowner(self):
            if self.__owner is None:
                return pyproc2.User(self.user)
            else:
                return self.__owner


        def duplicate(self,tout=0.001,strict=False):
            
            old=set(pyproc2().rescan(raw=True))
            if self.owner.name==getpass.getuser():
                popen=subprocess.Popen(shlex.split(self.cmd),stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            else:
                try:
                    popen=sudo.sudo(self.cmd,self.owner.name)
                except sudo.SudoError as e:
                    warnings.warn(Warning(str(e)+';aborting sudo'))
                    popen=subprocess.Popen(shlex.split(self.cmd),stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)

            pid=popen.pid
            return pyproc2().NewProcess(pyproc2._Process(pid),popen)

        def getparent(self):
            parent=pyproc2().NotExistingProcess()
            if 'ppid' in self.data:
                try:
                    parent=pyproc2()._Process(self.ppid,self.pid)
                except ProcessLookupError:
                    pass
            return parent

        def _cldrn(self):
            kids=open(os.path.join(self.path,'task',str(self.pid),'children')).read().split()
            return pyproc2().MakeProcessSet([pyproc2()._Process(int(p)) for p in kids])
        def child(self,ind=0):
            try:
                return self.children[ind]
            except IndexError:
                raise IndexError('child index overflow (maximum={})'.format(len(self.children)))
            except KeyError:
                return self.children
        def __getattr__(self,at):
            try:
                return pyproc2._Process(self.pid)[at]
            except KeyError:
                raise AttributeError(at)
        def __repr__(self):
            return str(self.pid)+r'{'+ self.name +r'}'
        def __eq__(self,sec):
            if sec.pid==self.pid:
                return True
            return False
        def kill(self,sig=9):
            for i in self.fds:
                if not i.closed:
                    i.close()


            self.__class__=pyproc2().NotExistingProcess
            try:
                os.kill(int(self.pid),sig)
            except PermissionError as err:
                reason=str(err)


                raise PermissionError("unable to kill process {}: {}".format(self,reason))
            except ProcessLookupError as err:
                self=pyproc2.NotExistingProcess()
                self.kill()
        def parentLevel(self,level):
            res=self
            for i in range(level):
                if not res.parent:
                    return res
                try:
                    res=res.parent
                except NotImplementedError:
                    return res
            return res
        cpu=property(count_cpu)
        children=property(_cldrn)
        parent=property(getparent)
        owner=property(getowner)
    class NewProcess(_Process):
        def __init__(self,process,popen=None):
            self.__process=process
            self.__dict__.update(process.__dict__)
            if popen is not None:
                self.__popen=popen
                self.stdout=popen.stdout
                self.stderr=popen.stderr
                self.stdin=popen.stdin
            else:
                pass
                #self.__class__=pyproc2()._Process
        def write(self,data):
            return self.stdin.write(data)
        def read(self,count=None):
            if count is None:
                return self.stdout.read()
            return self.stdout.read(count)
        def kill(self):
            self.__popen.terminate()
            try:
                self.__process.kill()
            except ProcessLookupError:
                pass
            self.__class__=pyproc2().NotExistingProcess

    class NotExistingProcess(NewProcess):
        def __init__(self):
            pass
        def __getattr__(self,foo):
            raise NotImplementedError("trying to acess attribute {} on non-existing process".format(foo))
        def kill(self,*args,**kwargs):
            raise NotImplementedError("trying to kill a non-existing process")
        def __repr__(self):
            return ''
        def __bool__(self):
            return False
    
    class ProcessSet(signals.Signalled):
        def __init__(self,pcs,name="<unknown>",rs=False):
            self.pcs=pcs
            self.pci=iter(pcs)
            if len(self.pcs)==0:
                if rs:
                    raise ProcessLookupError("no such process:{}".format(name))
                self=None
        def kill(self,signal=9):
            for pc in self.pcs:
                try:
                    pc.kill(signal)
                except NotImplementedError:
                    pass
        def __repr__(self):
            return 'ProcessSet({})'.format(repr(self.pcs).replace("]","").replace("[",""))
        def __iter__(self):
            return iter(self.pcs)
        def __getitem__(self,i):
            return self.pcs[i]
        def __setitem__(self,i,w):
            self.pcs[i]=w
        def __getattr__(self,at):
            return getattr(self.pcs[0],at)
        def __len__(self):
            return len(self.pcs)
    class User:
        def __init__(self,name):
            self.name=name
            self.processes=pyproc2().Process(user=self.name,_owner=self)
        def __repr__(self):
            return f'<User {self.name}>'
    def Process(self,a=None,_owner=None,**kwargs):
        if (a is None or a == NotImplemented) and kwargs=={}:
            raise TypeError(
                "you need either to specify process by first argument(PID or name) or by second argument(other properties)")
        if isinstance(a,int):
            return self._Process(a)
        elif isinstance(a,str):
            pcs=self.rescan(t=list)
            rs=[]
            for proc in pcs:
                if proc.name==a:
                     rs.append(self._Process(proc.pid,owner=_owner))
            if kwargs:
                rs=self._buildList(rs,self.filter(**kwargs))
            return self.MakeProcessSet(rs)
        elif a is None or a == NotImplemented:
            return self.filter(caseNone=self.NotExistingProcess(),_owner=_owner,**kwargs)
        else:
            raise TypeError(
                            "Bad type of first argument. Avalaible types are: str (name), int (pid) , None or NotImplemented (check only for other properties)"
                            )
                
    def _buildList(self,a1,a2):
        a1=list(a1)
        a2=list(a2)
        g=[]
        for item in a1:
            if item in a2:
                g.append(item)
        return g
    def rescan(self,t=ProcessSet,_owner=None,raw=False,warn=True):
        _running=os.listdir('/proc')
        run=[]
        for proc in _running:
            try:
                proc=int(proc)
                if raw:
                    run.append(proc)
                else:
                    try:
                        run.append(self.Process(proc,_owner=_owner))
                    except NotADirectoryError:pass
                    except ProcessLookupError:
                        if warn:
                            warnings.warn(ProcessKilledWarning(
                            f'process was killed during searching for running processes. This may cause problems if you wanted to reference the killed process. Process ID:{proc}'))

            except ValueError:pass
            
        return t(run)
    def kill(self,proc=None,sig=9,*args,**kwargs):
        a=self.Process(proc,*args,**kwargs)
        a.kill(sig)
    def get_total_cpu(self=None):
        cr=open('/proc/stat').readline().split()[1:4]
        return sum([int(a) for a in cr])
    def MakeProcessSet(self,u,_owner=None,caseNone=NotExistingProcess()):
        if len(u)==0:
            return caseNone
        elif len(u)==1:
            return self._Process(u[0].pid,owner=_owner)
        return self.ProcessSet(u)
    def filter(self,caseNone=[],_owner=None,**fields):
        running=[]
        for pid in self.rescan(raw=True):
            try:
                running.append(pyproc2()._Process(pid,owner=_owner))
            except ProcessLookupError:
                pass
        if fields=={}:
            return running
        res=[]
        for item in running:
            for fieldname,w in fields.items():
                if not hasattr(item,fieldname):
                    raise ValueError("no such field : {}").format(fieldname)
                if getattr(item,fieldname)==w:
                    res.append(item)
        return self.MakeProcessSet(res,caseNone=caseNone,_owner=_owner)
    def find(self,*args,**kwargs):
        return self.Process(*args,**kwargs)
    def _cpu(self,pc):
        return -pc.cpu
    def runningTop(self):
        return self.MakeProcessSet(sorted(self.running,key=self._cpu))
    def ticks(self=NotImplemented):
        return int(subprocess.getoutput("getconf CLK_TCK"))
    def logout(self,signal=9,user=getpass.getuser()):
        self.kill(sig=signal,user=user)
    def _current(self):
        return self.find(os.getpid())
    CLK = ticks()
    uptime=property(lambda foo:float(open("/proc/uptime").read().split()[0]))
    totalcpu=property(get_total_cpu)
    running=property(rescan)
    top=property(runningTop)
    current=property(_current)
    signals=signals()
    RUNNING=RUNNING()
    SLEEPING=SLEEPING()
    UNKNOWN=UNKNOWN()
    STOPPED=STOPPED()
if platform.system()!='Linux':

    raise OSError("the pyproc2 package works only on Linux")
sys.modules[__name__]=pyproc2()
