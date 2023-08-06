#!/usr/bin/env python3
import fcntl, termios
from .perm import Protected,NotExisting
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

        self.closed=False
    def close(self):
        self.write_file.close()
        self.read_file.close()
        self.closed=True
    def write(self,cmd):
        assert not self.closed
        tiocsti(self.write_file,cmd)
    def read(self):
        assert not self.closed
        return self.read_file.read()
def tiocsti(file,cmd):
    if not cmd.endswith('\n'):
        cmd+='\n'
    for b in cmd:
        fcntl.ioctl(file, termios.TIOCSTI,b)
