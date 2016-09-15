#!/bin/env python3

import sys,os,re
import json

class MessageId:
    '''
    '''
    def __init__( self, mid, **options ):
        '''
        '''
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
        self.TYPES=['request','reply','info','update']

        if mtype not in self.TYPES:
            raise AttributeError( "ERROR: Unsupported message type %s" % ( mtype ) )

        self.__message_type = mtype

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
    def __init__( self, data, **options ):
        '''
        '''
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
        self.__message_id = mid
        self.__message_type = mtype
        self.__message_to = mto
        self.__message_from = mfrom
        self.__message_content = mdata

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
        return "id:%(id)s;to:%(to)s;from:%(from)s;content:%(data)s" % { 'id': self.__message_id, 'to':self.__message_to, 'from':self.__message_from, 'data':self.__message_content }

#################################################################################

class RequestMessage( Message ):
    '''
    '''
    def __init__( self, mid, mtype, mto, mfrom, mdata, **options ):
        '''
        '''
        self.__debug = False
        if 'debug' in options:
            self.__debug = True

#################################################################################

class ReplyMessage( Message ):
    '''
    '''
    def __init__( self, mid, mtype, mto, mfrom, mdata, **options ):
        '''
        '''
        self.__debug = False
        if 'debug' in options:
            self.__debug = True

#################################################################################

class InfoMessage( Message ):
    '''
    '''
    def __init__( self, mid, mtype, mto, mfrom, mdata, **options ):
        '''
        '''
        self.__debug = False
        if 'debug' in options:
            self.__debug = True


#################################################################################

class UpdateMessage( Message ):
    '''
    '''
    def __init__( self, mid, mtype, mto, mfrom, mdata, **options ):
        '''
        '''
        self.__debug = False
        if 'debug' in options:
            self.__debug = True

#################################################################################

if __name__ == "__main__":
    pass
