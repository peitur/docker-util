#!/usr/bin/python3

import sys,os,re
sys.path.append( "../lib" )
sys.path.append( "./lib" )

from Controller.message import *
from Controller.local import *

import unittest

from pprint import pprint

class MessageTest( unittest.TestCase ):
    
    
    def setUp( self ):
        self.sample_plist = ["1234","1235","1236","2236","3236","8236","9236"]
        self.sample_proc = "samples"
        self.sample_cpuinfo = "cpu_file"
        self.sample_loadavg = "loadavg_file"
    
    
    def tearDown( self ):
        pass
    
    def test_process_information( self ):
        pid1 = self.sample_plist[0]
        pid2 = self.sample_plist[1]
        
        xpfile1 = "%s/%s/%s" % ( self.sample_proc, pid1, "status" ) 
        xpfile2 = "%s/%s/%s" % ( self.sample_proc, pid2, "status" ) 

        self.assertEqual( ProcessInformation( pid1, filename=xpfile1 ).load_data() , 7 )
        self.assertEqual( ProcessInformation( pid2, filename=xpfile2 ).load_data() , 9 )

    def test_process_tree_information( self ):
        pass
    
    def test_memory_information( self ):
        pass
    
    def test_loadavg_information( self ):
        pass 
    
    def test_cpu_information( self ):
        pass
    
    def test_system_information( self ):
        pass
    
    