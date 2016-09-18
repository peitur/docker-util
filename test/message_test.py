
import sys,os,re
sys.path.append( "../lib" )
sys.path.append( "./lib" )

from Controller.message import *
import unittest

class MessageTest( unittest.TestCase ):

    def setUp( self ):
        self.ok_message_list = {
            'RequestMessage': [{"to": "aaaa", "content": "cccccccc", "id": "1", "from": "bbbb", "type": "request"}],
            'ReplyMessage': [{"to": "aaaa", "content": "cccccccc", "id": "2", "from": "bbbb", "type": "reply"}],
            'InfoMessage': [{"to": "aaaa", "content": "cccccccc", "id": "3", "from": "bbbb", "type": "info"}],
            'UpdateMessage': [{"to": "aaaa", "content": "cccccccc", "id": "4", "from": "bbbb", "type": "update"}],
            'AlarmMessage': [{"to": "aaaa", "content": "cccccccc", "id": "5", "from": "bbbb", "type": "alarm"}]
        }

        self.nok_message_list = {
            'RequestMessage': [{"to": "aaaa", "content": "cccccccc", "id": "1", "from": "bbbb", "type": "test"}]
        }


    def tearDown( self ):
        pass

    def test_decode( self ):

        for o in self.ok_message_list:
            for k in self.ok_message_list[ o ]:
                self.assertEqual( type( decode_message( k ) ).__name__, o )

        for o in self.nok_message_list:
            for k in self.nok_message_list[ o ]:
                self.assertRaises( AttributeError, decode_message, k )

    def test_encode( self ):
        pass

    def test_alarm_message( self ):
        pass


    def test_request_message( self ):
        pass

    def test_reply_message( self ):
        pass

    def test_info_message( self ):
        pass

    def test_update_message( self ):
        pass
