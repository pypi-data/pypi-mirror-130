from .error import FDError
import os
class Fds:
    def __init__(self,fds):
        self.fds=fds
        self.stdout=self.fd(1)
        self.stdin=self.fd(0)
        self.stderr=self.fd(2)
    def fd(self,f):
        for i in self.fds:
            if os.path.split(i.path)[-1]==str(f):#not int (os.path.split(i)[-1]) == f
                return i
        else:
            raise FDError('no such fd: {}'.format(f))
    def __iter__(self):
        return iter( self.fds)
