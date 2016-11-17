
import os, sys, re, datetime
import json

from Crypto.PublicKey import RSA
from datetime import datetime, date, time
from pathlib import Path
from io import BytesIO

from docker import Client, tls

from pprint import pprint


import Controller.config
import Controller.local
import Controller.message
import Controller.store

################################################################################

class HostKeyRSA( object ):
    
    def __init__( self, **options ):
        """
        """
        self.__debug = False
        if 'debug' in options and options['debug'] in (True, False):
            self.__debug = options['debug']

        self.__bits = 2048
        self.__key = None

        
        if 'bits' in options:
            self.__bits = options['bits']            
        
        if 'key' in options:
            self.__key = options['key']            

        if 'kfile' in options:
            self.__key_file = options['kfile']            

        if 'pkfile' in options:
            self.__pkey_file = options['pkfile']            


    def generate( self ):
        
#        key = RSA.generate(2048)
#        key.exportKey('PEM')
#        pubkey = key.publickey()
#        pubkey.exportKey('OpenSSH')
    
        self.__key = RSA.generate( self.__bits )

        


    def get_key( self ):
        return self.__key.exportKey( "PEM" )

    def get_pkey( self ):
        return self.__key.publickey().exportKey("OpenSSH")


    def clear( self ):
        pass



################################################################################
class Manager( object ):
    
    def __init__(self, config, **options ):
        self.__debug = False
        self.__cache = None
        
        if 'debug' in options and options['debug'] in (True, False):
            self.__debug = options['debug']
        
        
    
    
    
class ControlManager( Manager ):
    
    def __init__( self, config, **options  ):
        super( ControlManager, self ).__init__( config, **options  )
        
    

class HostManager( Manager ):
    
    def __init__( self, config, **options  ):
        super( HostManager, self ).__init__( config, **options  )
    
    
    
################################################################################
if __name__ == "__main__":
    pass