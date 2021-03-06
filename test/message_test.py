#!/usr/bin/python3

import sys,os,re
sys.path.append( "../lib" )
sys.path.append( "./lib" )

from Controller.message import *
import unittest

from pprint import pprint

class MessageTest( unittest.TestCase ):

    def setUp( self ):
        self.ok_message_list = {
            'RequestMessage': [{"to": "aaaa", "content": "cccccccc", "id": "1", "from": "bbbb", "type": "request"}],
            'ReplyMessage': [{"to": "aaaa", "content": "cccccccc", "id": "2", "from": "bbbb", "type": "reply"}],
            'InfoMessage': [{"to": "aaaa", "content": "cccccccc", "id": "3", "from": "bbbb", "type": "info"}],
            'UpdateMessage': [{"to": "aaaa", "content": "cccccccc", "id": "4", "from": "bbbb", "type": "update"}],
            'AlarmMessage': [{"to": "aaaa", "content": "cccccccc", "id": "5", "from": "bbbb", "type": "alarm"}]
        }

        self.ok_string_output = {
            "RequestMessage": 'id:1;type:request;to:aaaa;from:bbbb;content:cccccccc',
            "ReplyMessage": 'id:2;type:reply;to:aaaa;from:bbbb;content:cccccccc',
            "InfoMessage": 'id:3;type:info;to:aaaa;from:bbbb;content:cccccccc',
            "UpdateMessage": 'id:4;type:update;to:aaaa;from:bbbb;content:cccccccc',
            "AlarmMessage": 'id:5;type:alarm;to:aaaa;from:bbbb;content:cccccccc'          
        }

        self.ok_serialize_output = {
            "RequestMessage": '{"to": "aaaa", "type": "request", "from": "bbbb", "content": "cccccccc", "id": "1"}',
            "ReplyMessage": '{"to": "aaaa", "type": "reply", "from": "bbbb", "content": "cccccccc", "id": "2"}',
            "InfoMessage": '{"to": "aaaa", "type": "info", "from": "bbbb", "content": "cccccccc", "id": "3"}',
            "UpdateMessage": '{"to": "aaaa", "type": "update", "from": "bbbb", "content": "cccccccc", "id": "4"}',
            "AlarmMessage": '{"to": "aaaa", "type": "alarm", "from": "bbbb", "content": "cccccccc", "id": "5"}'            
        }

        self.nok_message_list = {
            'RequestMessage': [{"to": "aaaa", "content": "cccccccc", "id": "1", "from": "bbbb", "type": "test"}],
            'Message': [{"to": "aaaa", "content": "cccccccc", "id": "0", "from": "bbbb", "type": "message"}]
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
        classStr = "AlarmMessage"
        
        sample = self.ok_message_list[ classStr ][0]
        sample_object = AlarmMessage( sample['id'], sample['to'],sample['from'], sample['content'] )
        self.assertEqual( type( sample_object ).__name__ , classStr )
        self.assertEqual( sample_object.__str__(), self.ok_string_output[ classStr ] )
        self.assertEqual( str( sample_object ), self.ok_string_output[ classStr ] )
        self.assertEqual( sample_object.__dict__(), self.ok_message_list[ classStr ][0] )
#        self.assertEqual( sample_object.__serialize__(), self.ok_serialize_output[ classStr ] )
        self.assertEqual( sample_object.message_id().__str__() , "5" )
        self.assertEqual( sample_object.message_sender().__str__(), "bbbb" )
        self.assertEqual( sample_object.message_receiver().__str__() , "aaaa" )
        self.assertEqual( sample_object.message_type().__str__() , "alarm" )
        self.assertEqual( sample_object.message_content().__str__() , "cccccccc" )
        self.assertEqual( type( sample_object.message_id() ).__name__ , "MessageId" )
        self.assertEqual( type( sample_object.message_sender() ).__name__, "MessageEndpoint" )
        self.assertEqual( type( sample_object.message_receiver() ).__name__ , "MessageEndpoint" )
        self.assertEqual( type( sample_object.message_type() ).__name__ , "MessageType" )
        self.assertEqual( type( sample_object.message_content() ).__name__ , "MessageData" )


    def test_request_message( self ):
        classStr = "RequestMessage"
        
        sample = self.ok_message_list[ classStr ][0]
        sample_object = RequestMessage( sample['id'], sample['to'],sample['from'], sample['content'] )
        self.assertEqual( type( sample_object ).__name__ , classStr )
        self.assertEqual( sample_object.__str__(), self.ok_string_output[ classStr ] )
        self.assertEqual( str( sample_object ), self.ok_string_output[ classStr ] )
        self.assertEqual( sample_object.__dict__(), self.ok_message_list[ classStr ][0] )
#        self.assertEqual( sample_object.__serialize__(), self.ok_serialize_output[ classStr ] )
        self.assertEqual( sample_object.message_id().__str__() , "1" )
        self.assertEqual( sample_object.message_sender().__str__(), "bbbb" )
        self.assertEqual( sample_object.message_receiver().__str__() , "aaaa" )
        self.assertEqual( sample_object.message_type().__str__() , "request" )
        self.assertEqual( sample_object.message_content().__str__() , "cccccccc" )
        self.assertEqual( type( sample_object.message_id() ).__name__ , "MessageId" )
        self.assertEqual( type( sample_object.message_sender() ).__name__, "MessageEndpoint" )
        self.assertEqual( type( sample_object.message_receiver() ).__name__ , "MessageEndpoint" )
        self.assertEqual( type( sample_object.message_type() ).__name__ , "MessageType" )
        self.assertEqual( type( sample_object.message_content() ).__name__ , "MessageData" )


    def test_reply_message( self ):
        classStr = "ReplyMessage"
        
        sample = self.ok_message_list[ classStr ][0]
        sample_object = ReplyMessage( sample['id'], sample['to'],sample['from'], sample['content'] )
        self.assertEqual( type( sample_object ).__name__ , classStr )
        self.assertEqual( sample_object.__str__(), self.ok_string_output[ classStr ] )
        self.assertEqual( str( sample_object ), self.ok_string_output[ classStr ] )
        self.assertEqual( sample_object.__dict__(), self.ok_message_list[ classStr ][0] )
#        self.assertEqual( sample_object.__serialize__(), self.ok_serialize_output[ classStr ] )
        self.assertEqual( sample_object.message_id().__str__() , "2" )
        self.assertEqual( sample_object.message_sender().__str__(), "bbbb" )
        self.assertEqual( sample_object.message_receiver().__str__() , "aaaa" )
        self.assertEqual( sample_object.message_type().__str__() , "reply" )
        self.assertEqual( sample_object.message_content().__str__() , "cccccccc" )
        self.assertEqual( type( sample_object.message_id() ).__name__ , "MessageId" )
        self.assertEqual( type( sample_object.message_sender() ).__name__, "MessageEndpoint" )
        self.assertEqual( type( sample_object.message_receiver() ).__name__ , "MessageEndpoint" )
        self.assertEqual( type( sample_object.message_type() ).__name__ , "MessageType" )
        self.assertEqual( type( sample_object.message_content() ).__name__ , "MessageData" )


    def test_info_message( self ):
        classStr = "InfoMessage"
        
        sample = self.ok_message_list[ classStr ][0]
        sample_object = InfoMessage( sample['id'], sample['to'],sample['from'], sample['content'] )
        self.assertEqual( type( sample_object ).__name__ , classStr )
        self.assertEqual( sample_object.__str__(), self.ok_string_output[ classStr ] )
        self.assertEqual( str( sample_object ), self.ok_string_output[ classStr ] )
        self.assertEqual( sample_object.__dict__(), self.ok_message_list[ classStr ][0] )
#        self.assertEqual( sample_object.__serialize__(), self.ok_serialize_output[ classStr ] )
        self.assertEqual( sample_object.message_id().__str__() , "3" )
        self.assertEqual( sample_object.message_sender().__str__(), "bbbb" )
        self.assertEqual( sample_object.message_receiver().__str__() , "aaaa" )
        self.assertEqual( sample_object.message_type().__str__() , "info" )
        self.assertEqual( sample_object.message_content().__str__() , "cccccccc" )
        self.assertEqual( type( sample_object.message_id() ).__name__ , "MessageId" )
        self.assertEqual( type( sample_object.message_sender() ).__name__, "MessageEndpoint" )
        self.assertEqual( type( sample_object.message_receiver() ).__name__ , "MessageEndpoint" )
        self.assertEqual( type( sample_object.message_type() ).__name__ , "MessageType" )
        self.assertEqual( type( sample_object.message_content() ).__name__ , "MessageData" )


    def test_update_message( self ):
        classStr = "UpdateMessage"
        
        sample = self.ok_message_list[ classStr ][0]
        sample_object = UpdateMessage( sample['id'], sample['to'],sample['from'], sample['content'] )
        self.assertEqual( type( sample_object ).__name__ , classStr )
        self.assertEqual( sample_object.__str__(), self.ok_string_output[ classStr ] )
        self.assertEqual( str( sample_object ), self.ok_string_output[ classStr ] )
        self.assertEqual( sample_object.__dict__(), self.ok_message_list[ classStr ][0] )
#        self.assertEqual( sample_object.__serialize__(), self.ok_serialize_output[ classStr ] )
        self.assertEqual( sample_object.message_id().__str__() , "4" )
        self.assertEqual( sample_object.message_sender().__str__(), "bbbb" )
        self.assertEqual( sample_object.message_receiver().__str__() , "aaaa" )
        self.assertEqual( sample_object.message_type().__str__() , "update" )
        self.assertEqual( sample_object.message_content().__str__() , "cccccccc" )
        self.assertEqual( type( sample_object.message_id() ).__name__ , "MessageId" )
        self.assertEqual( type( sample_object.message_sender() ).__name__, "MessageEndpoint" )
        self.assertEqual( type( sample_object.message_receiver() ).__name__ , "MessageEndpoint" )
        self.assertEqual( type( sample_object.message_type() ).__name__ , "MessageType" )
        self.assertEqual( type( sample_object.message_content() ).__name__ , "MessageData" )


    def test_generic_message( self ):
        classStr = "Message"
        
        for a in self.ok_message_list:
            for b in self.ok_message_list[a]:
                Message( b['id'], b['type'], b['to'], b['from'], b['content'] )

        for a in self.nok_message_list:
            for sample in self.nok_message_list[a]:
                with self.assertRaises( AttributeError ) as test:
                    Message( sample['id'], sample['type'], sample['to'],sample['from'], sample['content'] ) 


