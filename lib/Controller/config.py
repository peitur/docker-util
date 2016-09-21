import sys,os, json, re
from pprint import pprint

import util

## make it into a singleton, only want one single store for all instanciations of config
class SingInstance( object ):
    __shared = {}
    def __init__( self ):
        self.__dict__ = self.__shared
    
    
class ConfigContent( SingInstance ):
    
    
    def __init__(self, filename = None, **options ):
        super( ConfigContent, self ).__init__()

        self.__debug = False
        if 'debug' in options and options['debug'] in (True, False):
            self.__debug = options['debug']

        if filename:
            self.__filename = filename


#######################

    ## variable management in config files.
    def __variable_apply( self ):
        
        var_rx = re.compile( r"<\|\s*(.+)\s*\|>" )
        
        varlist = {}
        ## first go through all key in config to add all string based basic variables.
        ## Variables depending on variables are still stricky though due to order of key loading.
        ## Should have made config into list to make sure it's all good at all times..
        for item in self.__config:
            if util.is_string( self.__config[ item ] ):
                if not var_rx.match( self.__config[ item ] ):
                    varlist[ item ] = self.__config[ item ]
                    
        for item in self.__config:
            if util.is_string( self.__config[ item ] ):
                m = var_rx.match( self.__config[ item ] )
                if m:
                    for v in m.groups( ):
                        vstr = r"<\|%s\|>" % ( v )
                        self.__config[ item ] = re.sub( vstr, varlist[ v ], self.__config[ item ] )
                varlist[ item ] = self.__config[ item ]

#######################
        

    def load_data( self, filename = None ):

        if not filename:
            filename = self.__filename
    
        data = []
        if self.__debug: print("DEBUG: Reading file %(fn)s" % {'fn': filename } )
        
        try:

            for line in open( filename, "r"):
                data.append( line.rstrip().lstrip() )
            
        except Exception as error:
            print("ERROR: Loading config file %s failed : %s" % ( filename, error ) )
    
        if self.__debug: print("DEBUG: Read %(ln)s lines from %(fn)s" % {'ln': len( data ), 'fn': filename } )
        if self.__debug:
            pprint( data )
        
        self.__config = json.loads( "\n".join( data ) )
        self.__variable_apply()
        
        return len( self.__config.keys() )



    def filename( self ):
        return self.__filename
    
    
    def get( self, key, default = None ):
        if key in self.__config:
            return self.__config[ key ]
        return default
    
    
    def __hash__( self ):
        return { 
            'filename': self.__filename, 
            'config': self.__config 
        }
    

if __name__ == "__main__":
    
    s1 = ConfigContent( "../../test/samples/config.json" )
    s1.load_data()
    pprint( s1.__hash__() )
    
    # s2 = ConfigContent()
    # s3 = ConfigContent()
    # s4 = ConfigContent()
    
    # pprint( s1.filename() )
    # pprint( s2.filename() )
    # pprint( s3.filename() )
    # pprint( s4.filename() )
    
    # pprint( s1.__hash__() )