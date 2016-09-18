
import sys,os,re
sys.path.append( "../lib" )
sys.path.append( "./lib" )

from Controller.message import *
import unittest

class MessageTest( unittest.TestCase ):

    def setUp( self ):
        self.message_list = []


    def tearDown( self ):
        pass

    def test_decode( self ):
        pass

    def test_encode( self ):
        pass

    def test_alarm_message( self ):

        ok_message = [
            { 'mtype' : 'alarm', 'mid' : '1', 'mto' : 'aaaaa', 'mfrom' : 'bbbb', 'data' : {'message':'hello', 'state':'ok' } }
        ]

        nok_message = [
            { 'mtype' : 'test', 'mid' : 'abc', 'mto' : 'aaaaa', 'mfrom' : 'bbbb', 'data' : {'message':'hello', 'state':'ok' } }
        ]

        for ok in ok_message:
            self.assertEqual( type( AlarmMessage( ok['mid'], ok['mto'], ok['mfrom'], ok['data'] ) ).__name__, 'AlarmMessage' )


    def test_request_message( self ):
        pass

    def test_reply_message( self ):
        pass

    def test_info_message( self ):
        pass

    def test_update_message( self ):
        pass
