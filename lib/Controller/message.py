#!/bin/env python3

import sys,os,re
import json

class MessageId:
    '''
    '''
    def __init__( self, mid, **options ):
        '''
        '''
        if type( mid ).__name__ == 'MessageId':
            self.__message_id = mid.__str__()
        else:
            self.__message_id = mid

        self.__debug = False
        if 'debug' in options:
            self.__debug = True


    def __dict__( self ):
        return { 'id': self.__message_id }

    def __str__( self ):
        return self.__message_id.__str__()


class MessageType:

    def __init__(self, mtype, **options ):
        '''
        '''
        self.TYPES=['request','reply','info','update','alarm']

        if type( mtype ).__name__ == 'MessageType':
            self.__message_type = mtype.__str__()
        else:
            self.__message_type = mtype

        if self.__message_type not in self.TYPES:
            raise AttributeError( "ERROR: Unsupported message type %s" % ( mtype ) )


        self.__debug = False
        if 'debug' in options:
            self.__debug = True

    def __dict__( self ):
        return { 'type': self.__message_type }

    def __str__( self ):
        return self.__message_type.__str__()



class MessageEndpoint:
    '''
    '''
    def __init__( self, epoint, **options ):
        '''
        '''

        if type( epoint ).__name__ == 'MessageEndpoint':
            self.__message_endpoint = epoint.__str__()
        else:
            self.__message_endpoint = epoint

        self.__debug = False
        if 'debug' in options:
            self.__debug = True

    def __dict__( self ):
        return { 'endpoint': self.__message_endpoint }

    def __str__( self ):
        return self.__message_endpoint.__str__()



class MessageData:
    '''
    '''
    def __init__( self, mdata, **options ):
        '''
        '''
        if type( mdata ).__name__ == 'MessageData':
            self.__message_content = mdata.__str__()
        else:
            self.__message_content = mdata

        self.__debug = False
        if 'debug' in options:
            self.__debug = True


    def __dict__( self ):
        return { 'content': self.__message_content }

    def __str__( self ):
        return self.__message_content.__str__()



class Message:
    '''
    '''
    def __init__( self, mid, mtype, mto, mfrom, mdata, **options ):
        '''
        Constructor, new message container
        '''

        self.__message_id = MessageId( mid )
        self.__message_type = MessageType( mtype )
        self.__message_to = MessageEndpoint( mto )
        self.__message_from = MessageEndpoint( mfrom )
        self.__message_content = MessageData( mdata )

        self.__debug = False
        if 'debug' in options:
            self.__debug = True


    def message_id( self ):
        return self.__message_id

    def message_receiver( self ):
        return self.__message_to

    def message_type( self ):
        return self.__message_type

    def message_sender( self ):
        return self.__message_from

    def message_content( self ):
        return self.__message_content


    def __dict__( self ):
        mid = self.__message_id.__dict__()
        mtype = self.__message_type.__dict__()
        mto = self.__message_to.__dict__()
        mfrom = self.__message_from .__dict__()
        mcontent =  self.__message_content.__dict__()
        return {
            "id": mid['id'],
            "type": mtype['type'],
            "to": mto['endpoint'],
            "from": mfrom['endpoint'],
            "content": mcontent['content']
        }

    def __str__( self ):
        return "id:%(id)s;type:%(type)s;to:%(to)s;from:%(from)s;content:%(data)s" % { 'id': self.__message_id,'type':self.__message_type, 'to':self.__message_to, 'from':self.__message_from, 'data':self.__message_content }

    def __serialize__( self ):
        return json.dumps( self.__dict__( ) )








#################################################################################

class RequestMessage( Message ):
    '''
    '''
    def __init__( self, mid, mto, mfrom, mdata, **options ):
        '''
        '''
        Message.__init__( self, mid, MessageType('request'), mto, mfrom, mdata, **options )

        self.__debug = False
        if 'debug' in options:
            self.__debug = True

#################################################################################

class ReplyMessage( Message ):
    '''
    '''
    def __init__( self, mid, mto, mfrom, mdata, **options ):
        '''
        '''
        Message.__init__( self, mid, MessageType('reply'), mto, mfrom, mdata, **options )

        self.__debug = False
        if 'debug' in options:
            self.__debug = True

#################################################################################

class InfoMessage( Message ):
    '''
    '''
    def __init__( self, mid, mto, mfrom, mdata, **options ):
        '''
        '''
        Message.__init__( self, mid, MessageType('info'), mto, mfrom, mdata, **options )

        self.__debug = False
        if 'debug' in options:
            self.__debug = True


#################################################################################

class UpdateMessage( Message ):
    '''
    '''
    def __init__( self, mid, mto, mfrom, mdata, **options ):
        '''
        '''
        Message.__init__( self, mid, MessageType('update'), mto, mfrom, mdata, **options )

        self.__debug = False
        if 'debug' in options:
            self.__debug = True

class AlarmMessage( Message ):
    '''
    '''
    def __init__( self, mid, mto, mfrom, mdata, **options ):
        '''
        '''
        Message.__init__( self, mid, MessageType('alarm'), mto, mfrom, mdata, **options )

        self.__debug = False
        if 'debug' in options:
            self.__debug = True


#################################################################################
def encode_message( data, **options ):
    '''
    '''
    if type( data ).__name__ == 'str': return data
    elif type( data ).__name__ == 'dict': return data.__str__()
    else: return data.__serialize__()


def decode_message( data, **options ):
    '''
    '''
    ## assuming json if indata is a string
    xdata = None
    if type( data ).__name__ == 'str':
        xdata = json.loads( data )
    elif type( data ).__name__ == 'dict':
        xdata = data

    if xdata['type'] in ( 'request' ):
        return RequestMessage( xdata['id'],xdata['to'],xdata['from'],xdata['content'], **options )
    elif xdata['type'] in ( 'reply' ):
        return ReplyMessage( xdata['id'],xdata['to'],xdata['from'],xdata['content'], **options )
    elif xdata['type'] in ( 'info' ):
        return InfoMessage( xdata['id'],xdata['to'],xdata['from'],xdata['content'], **options )
    elif xdata['type'] in ( 'update' ):
        return UpdateMessage( xdata['id'],xdata['to'],xdata['from'],xdata['content'], **options )
    elif xdata['type'] in ( 'alarm' ):
        return AlarmMessage( xdata['id'],xdata['to'],xdata['from'],xdata['content'], **options )
    else:
        raise AttributeError("ERROR: Unsupported message type: '%s'" % ( xdata['type'] ) )

if __name__ == "__main__":


    # Todo: Redo this as unit tests in a propper implementation
    from pprint import pprint

    pprint( RequestMessage("1", "aaaa", "bbbb","cccccccc" ).__serialize__() )
    pprint( ReplyMessage("2", "aaaa", "bbbb","cccccccc" ).__serialize__() )
    pprint( InfoMessage("3", "aaaa", "bbbb","cccccccc" ).__serialize__() )
    pprint( UpdateMessage("4", "aaaa", "bbbb","cccccccc" ).__serialize__() )
    pprint( AlarmMessage("5", "aaaa", "bbbb","cccccccc" ).__serialize__() )

    pprint( decode_message( RequestMessage("1", "aaaa", "bbbb","cccccccc" ).__serialize__() ).__str__() )
    pprint( decode_message( ReplyMessage("2", "aaaa", "bbbb","cccccccc" ).__serialize__() ).__str__() )
    pprint( decode_message( InfoMessage("3", "aaaa", "bbbb","cccccccc" ).__serialize__() ).__str__() )
    pprint( decode_message( UpdateMessage("4", "aaaa", "bbbb","cccccccc" ).__serialize__() ).__str__() )
    pprint( decode_message( AlarmMessage("5", "aaaa", "bbbb","cccccccc" ).__serialize__() ).__str__() )

    pass
