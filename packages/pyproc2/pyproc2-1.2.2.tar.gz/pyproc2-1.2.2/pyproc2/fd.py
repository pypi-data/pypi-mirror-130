from .error import FDError
import os
class Fds:
    def __init__(self,fds,caseNone=None):
        self.fds=fds
        self.stdout=self.fd(1,strict=False)
        self.stdin=self.fd(0,strict=False)
        self.stderr=self.fd(2,strict=False)
        self.__none=caseNone
    def fd(self,f,strict=True):
        for i in self.fds:
            if os.path.split(i.path)[-1]==str(f):#not int (os.path.split(i)[-1]) == f
                return i
        else:
            if strict:
                raise FDError('no such fd: {}'.format(f))
            else:
                return self.__none
    def __iter__(self):
        return iter( self.fds)
