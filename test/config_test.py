#!/usr/bin/python3

import sys,os,re
sys.path.append( "../lib" )
sys.path.append( "./lib" )

from Controller.message import *
from Controller.local import *

import unittest

from pprint import pprint

class ConfigurationTest( unittest.TestCase ):
    
    
    def setUp( self ):
        self.configfile = "samples/config.json"
    
    def tearDown( self ):
        pass
    
