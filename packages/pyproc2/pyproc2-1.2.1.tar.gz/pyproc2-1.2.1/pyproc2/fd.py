from .error import FDError
from .perm import NotExisting
import os
class Fds:
    def __init__(self,fds):
        self.fds=fds
        self.stdout=self.fd(1,strict=False)
        self.stdin=self.fd(0,strict=False)
        self.stderr=self.fd(2,strict=False)
    def fd(self,f,strict=True):
        for i in self.fds:
            if os.path.split(i.path)[-1]==str(f):#not int (os.path.split(i)[-1]) == f
                return i
        else:
            if strict:
                raise FDError('no such fd: {}'.format(f))
            else:
                return NotExisting
    def __iter__(self):
        return iter( self.fds)
