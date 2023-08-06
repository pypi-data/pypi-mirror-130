#!/usr/bin/env python3
import fcntl, termios
import os
from .perm import Protected,NotExisting
import warnings
class OpenFileWarning(Warning):pass
class TioFile:
    def __init__(self,pth):
        self.path=pth
        try:
            self.write_file=open(pth,'w')
        except PermissionError:
            self.write_file=Protected(pth,'w')
        except OSError:
            self.write_file=NotExisting
        try:
            self.read_file=open(pth,'r')
        except PermissionError:
            self.read_file=Protected(pth,'r')
        except OSError:
            self.read_file=NotExisting
        open_files=0
        try:
            self.close()
        except:
            try:
                self.read_file.close()
            except:
                open_files+=1
        self.realpath=os.path.realpath(self.path)
        if open_files:
            warnings.warn(
                OpenFileWarning(f'there are {open_files} open files. This may cause OSError:too many open files'))

        self.closed=False
    def close(self):
        self.write_file.close()
        self.read_file.close()
        self.closed=True
    def write(self,cmd):
        assert not self.closed
        with open(self.path,'w')as self.write_file:
            tiocsti(self.write_file,cmd)
        
    def read(self):
        assert not self.closed
        with open(self.path)as self.read_file:
            return self.read_file.read()
def tiocsti(file,cmd):
    if not cmd.endswith('\n'):
        cmd+='\n'
    for b in cmd:
        fcntl.ioctl(file, termios.TIOCSTI,b)
