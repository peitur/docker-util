import os, sys, re, datetime
import json

from datetime import datetime, date, time
from pathlib import Path
from io import BytesIO

from docker import Client, tls

from pprint import pprint

#########################################################################


PROC="/proc"
PROC_STATUS_OL = "stat"
PROC_STATUS_ML = "status"

DOCKERD="dockerd"

MEMFILE = "meminfo"
LOADFILE = "loadavg"
CPUFILE = "cpuinfo"

#########################################################################

class Information:
    '''
        Just wanted a simple interface to follow for this.
    '''
    def __init__(self, **options ):
        pass

    def load_data( self ):
        raise NotImplementedError("ERROR: 'load_data' function is not implemented")

    def __str__( self ):
        raise NotImplementedError("ERROR: '__str__' function is not implemented")

    def __serialize__( self ):
        raise NotImplementedError("ERROR: '__serialize__' function is not implemented")

    def __dict__(self):
        raise NotImplementedError("ERROR: '__dict__' function is not implemented")

    def get_information( self ):
        raise NotImplementedError("ERROR: 'get_information' function is not implemented")



class ProcessInformation( Information ):
    '''
        Contains information of one process
    '''
    def __init__(self, pid, **options ):
        super( ProcessInformation, self ).__init__( **options )

        self.__process_fields = ['name','state','pid','ppid','threads','vmsize','vmpeak','uid','gid']

        self.__pid = pid
        self.__process_path = Path( "%(path)s/%(pid)s" % { 'path': PROC,'pid': pid } )
        self.__process_statusfile = Path( "%(path)s/%(fl)s" % { 'path': self.__process_path.__str__(),'fl': PROC_STATUS_ML } )
        self.__process_info = {}

        if 'filename' in options:
            self.__process_statusfile = Path( options['filename'] )

        if not self.__process_statusfile.exists():
            raise RuntimeError("ERROR: Process %s was not found" % ( self.__pid ) )


    def load_data( self ):
        with open( self.__process_statusfile.__str__(), "r" ) as fd:
            for line in fd:
                larray = re.split( r"\s+", re.sub( r":","", line ).lower() )
                if larray[0] in self.__process_fields:
                    self.__process_info[ larray[0] ] = larray[1]
            fd.close()
        
        return len( self.__process_info )

    def get_statusfile( self ):
        return self.__process_statusfile.__str__()

    def get_pid( self ):
        return self.__pid


    def filter( self, k = None ):
        if not k: raise AttributeError("ERROR: Missing key in filter")
        if k not in self.__process_fields: raise AttributeError("ERROR: Missing key in supported fields: %s" % ( ",".join( self.__process_fields ) ) )

        if k in self.__process_info:
            return { 'field': k, 'pid': self.__pid, 'value': self.__process_info[ k ] }


    def get_information( self ):
        return self.__process_info

    def __str__( self ):
        return str( self.__process_info )

    def __serialize__( self ):
        return json.dumps( self.__dict__() )

    def __dict__( self ):
        return self.__process_info


class ProcessTreeInformation( Information ):
    '''
        Contains information of one process
    '''
    def __init__(self, **options ):
        super( ProcessTreeInformation, self ).__init__( options )
        self.__process_list = {}


    def load_data( self ):
        ps_rx = re.compile( r"^/proc/([0-9]+)$" )
        for x in Path("/proc").iterdir():
            m = ps_rx.match( x.__str__() )
            if m:
                self.__process_list[ m.group(1) ] = ProcessInformation( m.group(1) )
                self.__process_list[ m.group(1) ].load_data()

        return len( self.__process_list.keys() )

    def get_information(self):
        return self.__process_list

    def get_pid( self, pid ):
        return self.__process_list[ pid ]

    def filter( self, k = None ):
        if not k: raise AttributeError("ERROR: Missing key in filter")

        result = []
        for p in self.__process_list:
            xk = self.__process_list[p].filter( k )
            result.append( { 'field': xk['field'], 'pid': xk['pid'], 'value': xk['value'] } )

        return result


    def __serialize__( self ):
        return json.dumps( self.__dict__() )

    def __dict__( self ):
        result = {}
        for p in self.__process_list:
            result[p] = self.__process_list[p].__dict__()

        return result


class MemoryInformation(Information):
    '''
        Handles (selected) memory information
    '''
    def __init__(self, **options ):
        super( MemoryInformation, self ).__init__( options )

        self.__memory_fields = ['memtotal','memfree','memavailable','buffers','cached','swaptotal','swapfree','swapcached','shmem','slab']

        self.__memory_file = Path( "%(path)s/%(mf)s" % { "path": PROC, "mf": MEMFILE } )
        self.__memory_info = {}

        if 'filename' in options:
            self.__memory_file = Path( options['filename'] )

        if not self.__memory_file.exists():
            raise RuntimeError("ERROR: Memory file was not found: %(fl)s" % {'fl': self.__memory_file} )


    def load_data( self ):
        
        with open( self.__memory_file.__str__(), "r" ) as fd:
            for line in fd:
                larray = re.split( r"\s+", re.sub( r":","", line ).lower() )
                if larray[0] in self.__memory_fields:
                    self.__memory_info[ larray[0] ] = larray[1]
            fd.close()
            
        return len( self.__memory_info )

    def filter( self, k = None ):
        if not k: raise AttributeError("ERROR: Missing key in filter")
        if k not in self.__memory_fields: raise AttributeError("ERROR: Missing key in supported fields: %s" % ( ",".join( self.__memory_fields ) ) )

        if k in self.__memory_info:
            return { 'field': k, 'value': self.__memory_info[ k ] }


    def get_information( self ):
        return self.__memory_info

    def __str__( self ):
        pass

    def __serialize__( self ):
        return json.dumps( self.__dict__() )


    def __dict__( self ):
        return self.__memory_info



class CpuInformation( Information ):
    '''
        Speciffic local CPU information
    '''
    def __init__(self, **options ):
        super( CpuInformation, self ).__init__( options )
        self.__cpu_fields = ['processor','vendor_id','model name','cpu mzh','bogmips']
        self.__cpu_data = []
        self.__rotate = self.__cpu_fields[0]
        self.__cpu_filename = Path( "%(path)s/%(fn)s" % { 'path':PROC, 'fn': CPUFILE } )

        if 'filename' in options:
            self.__cpu_filename = Path( options['filename'] )


    def load_data( self ):

        data = {}
        with open( self.__cpu_filename.__str__(), "r" ) as fd:
            for line in fd:
                larray = [ x.lstrip().rstrip() for x in re.split( r":", line ) ]
                if larray[0].lower() in self.__cpu_fields:
                    data[ larray[0].lower() ] = larray[1]
            
                if self.__rotate == larray[0].lower() and self.__rotate in data:
                    self.__cpu_data.append( data )
                    data = {}

        return len( self.__cpu_data )

    def __str__( self ):
        pass        

    def __serialize__( self ):
        return json.dumps( self.__dict__() )

    def __dict__( self ):
        return self.__cpu_data


class SystemLoadInformation(Information):
    '''
        Speciffic local system load information
    '''
    def __init__(self, **options ):
        super( SystemLoadInformation, self ).__init__( options )
        self.__load_fields = ['1m','5m','15m','qs','np']
        self.__load_data = {}
        self.__load_filename = Path( "%(path)s/%(fn)s" % { 'path': PROC, 'fn': LOADFILE } )
        
        if 'filename' in options:
            self.__load_filename = Path( options['filename'] )
        
        
    def load_data( self ):

        try:
            fd = open( self.__load_filename.__str__(), "r" )
            line = fd.readline().lstrip().rstrip()
            fd.close()

            for i, x in enumerate( re.split( r"\s+", line ) ):
                self.__load_data[ self.__load_fields[i] ] = x

        except Exception as error:
            pprint( error )
            
        return len( self.__load_data.keys() )
    
    def __str__( self ):
        pass

    def __serialize__( self ):
        return json.dumps( self.__dict__() )

    def __dict__( self ):
        return self.__load_data 



class DockerProcessInformation(Information):
    '''
        Speciffic docker process information
    '''
    def __init__(self, **options ):
        super( ProcessInformation, self ).__init__( options )
        pass

    def __str__( self ):
        pass

    def __serialize__( self ):
        pass

    def __dict__( self ):
        pass


class DockerInformation(Information):
    '''
        Speciffic docker generic information and
    '''
    def __init__(self, **options ):
        super( ProcessInformation, self ).__init__( options )
        pass

    def __str__( self ):
        pass

    def __serialize__( self ):
        pass

    def __dict__( self ):
        pass


class SystemInformation( Information ):

    def __init__(self, **options ):
        
        super( ProcessInformation, self ).__init__( options )

        self.__default_format = "object"
        if 'format' in options and options['format'] in ( "object","json","str", "string" ):
            self.__default_format = options['format']
        
        self.__cache_data = False  
        self.__cache_dirty = False

        if 'cached' in options:
            self.__cache_data = True    
            self.__cache_dirty = True


    def get( self, what, **options ):
        
        formt = self.__default_format
        if 'format' in options and options['format'] in ( "object","json","str", "string" ):
            formt = options['format']
        
        if what in ("cpu"):
            pass
        elif what in ("process"):
            pass
        elif what in ("memory"):
            pass
        elif what in ("loadavg"):
            pass
        else:
            raise AttributeError("ERROR: Type %s not supported" % ( what ) )


    def load_data( self ):
        pass
    
    
    def __str__( self ):
        pass

    def __serialize__( self ):
        pass

    def __dict__( self ):
        pass



#########################################################################
if __name__ == "__main__":
    pti = ProcessTreeInformation()
    if pti.load_data() > 0:
        pprint( pti.get_information() )
        pprint( pti.filter('name') )

    mi = MemoryInformation()
    mi.load_data()
    pprint( mi.get_information() )

    pprint( pti.__serialize__() )
    pprint( mi.__serialize__() )
    
    ci = CpuInformation( )
    ci.load_data()
    pprint( ci.__serialize__() )
    
    avi = SystemLoadInformation( )
    avi.load_data()
    pprint( avi.__serialize__() )
