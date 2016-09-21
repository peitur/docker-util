#!/usr/bin/python3

import sys,os,re
sys.path.append( "../lib" )
sys.path.append( "./lib" )

import util
import unittest

from pprint import pprint

class UtilTest( unittest.TestCase ):
    
    
    def test_positive_types( self ):
        self.assertTrue( util.is_string( "abcd" ) )
        self.assertTrue( util.is_boolean( True ) )
        self.assertTrue( util.is_integer( 1234 ) )
        self.assertTrue( util.is_list( [1,2,3,4]) )
        self.assertTrue( util.is_dict( {"foo":"bar"} ) )

    def test_neg_strings( self ):
        self.assertFalse( util.is_string( ["a","b","c"] ) )
        
    def test_neg_integers( self ):
        self.assertFalse( util.is_integer( "1234" ) )
        self.assertFalse( util.is_integer( [1,2,3] ) )
    
    def test_neg_booelans( self ):
        self.assertFalse( util.is_boolean( "True" ) )
        self.assertFalse( util.is_boolean( "abcd" ) )
        
    def test_neg_lists( self ):
        self.assertFalse( util.is_list( "1234" ) )
        self.assertFalse( util.is_list( 12345 ) )
        
    def test_neg_dicts( self ):
        self.assertFalse( util.is_dict( ["foo","bar"] ) )
