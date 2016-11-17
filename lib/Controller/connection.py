##
import os, sys, re, datetime
import json
import socket

from datetime import datetime, date, time
from pathlib import Path
from io import BytesIO

from pprint import pprint

## Generic Socket wrapper for application
class ManagerSocket( object ):

    def __init__( self, **options ):
        self.__debug = False
        self.__test = False

        if 'debug' in options and options['debug'] in (True, False): self.__debug = option['debug']
        if 'test' in options and options['test'] in (True, False): self.__test = option['test']

        self.__socket = None
        self.__port = None
        self.__token = None

        pass

## Generic Controller connection wrapper, used by the controlling host (service)
class ControllerConnection( object ):

    def __init__( self, **options ):
        self.__connection_state = False


## The generic client host connection, used by "client" hosts to talk to controller
class HostConnection( object ):

    def __init__( self ):
        self.__connection_state = False





if __name__ == "__main__":
    pass
