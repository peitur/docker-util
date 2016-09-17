import os, sys, re, datetime
import json

from datetime import datetime, date, time
from docker import Client, tls
from io import BytesIO

#########################################################################


PROC="/proc"
PROC_STATUS_OL = "stat"
PROC_STATUS_ML = "status"

DOCKERD="dockerd"

MEMFILE = "/proc/meminfo"

#########################################################################

class Information:
    '''
        Just wanted a simple interface to follow for this.
    '''
    def __init__(self):
        pass

    def __str__( self ):
        raise NotImplementedError("ERROR: function is not implemented")

    def __serialize__( self ):
        raise NotImplementedError("ERROR: function is not implemented")

    def __dict__(self):
        raise NotImplementedError("ERROR: function is not implemented")



class ProcessInformation(Information):
    '''
        Contains information of one process
    '''
    def __init__(self, pid, **options ):
        super( ProcessInformation, self ).__init__()

        self.__pid = pid
        self.__process_path = "%(path)s/%(pid)s" % {'path': PROC,'pid': pid }
        self.__process_info = {}

        if not os.path.exists( self.__process_path ):
            raise RuntimeError("ERROR: Process %s was not found" % ( self.__pid ) )



class MemoryInformation(Information):
    '''
        Handles memory information
    '''
    def __init__(self):
        super( ProcessInformation, self ).__init__()

        self.__memory_file = "%(path)s/%(mf)s" % { "path": PROC, "mf": MEMFILE }
        self.__memory_info = []

        if not os.path.exists( self.__memory_file ):
            raise RuntimeError("ERROR: Memory file was not found" )



class DockerProcessInformation(Information):
    '''
        Speciffic docker process information
    '''
    def __init__(self):
        super( ProcessInformation, self ).__init__()
        pass

class DockerInformation(Information):
    '''
        Speciffic docker generic information and
    '''
    def __init__(self):
        super( ProcessInformation, self ).__init__()
        pass



class SystemInformation(Information):

    def __init__(self):
        super( ProcessInformation, self ).__init__()

        self.__process_info = None
        self.__memory_info = None
        self.__docker_info = None




#########################################################################
if __name__ == "__main__":
    pass
