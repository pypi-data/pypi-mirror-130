import io
from .fd import Fds
class NotExisting:
    def write(self,anything):
        raise FileNotFoundError
    def read(self):
        raise FileNotFoundError
    def close(self):pass
class Protected:
    def __init__(self,path,mode='r'):
        self.path=path
        self.mode=mode
        self.closed=True
    def close(self):pass
    def write(self,anything):
        if self.mode.startswith('w'):
            raise PermissionError('You don\'t have a permission to write file {!r}')
        else:
            raise io.UnsupportedOperation('write')
    def read(self):
        if self.mode.startswith('r'):
            raise PermissionError('You don\'t have a permission to read from file {!r}')
        else:
            raise io.UnsupportedOperation('read')
class BlockedFD(Fds):
    def __init__(self):
        self.fds=[]
        self.stdout=Protected('<stdout>')
        self.stdin=Protected('<stdin>','w')
        self.stderr=Protected('<stderr>')
        self.__none=NotExisting
    
