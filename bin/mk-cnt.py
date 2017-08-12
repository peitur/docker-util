#!/usr/bin/env python3


import os, re, sys, getopt
import multiprocessing
import subprocess, shlex
import json
from pprint import pprint


## =============================================================
## utils
## =============================================================
def dirtree( path, rx=r".*" ):
    result = list()
    for f in os.listdir( path ):
        p = "%s/%s" % ( path, f )
        if os.path.isdir( p ):
            result += dirtree( p, rx )
        else:
            if re.search( rx, f ):
                result.append( p )

    return result

def filename( filename ):
    return re.split( r"/", filename )[-1]

def filetype( filename ):
    return re.split( r"\.", filename )[-1]

def file_is_type( filename, tp ):
    chkt = filetype( filename )
    if chkt == tp:
        return True
    return False



## -----------------------------------------
# Run one command,
# - cmd_list    : command and arguments as list
# - opt         : dict of options
#   : debug     : debug info in function
def _run_command( cmd, **opt ):
    debug = False
    if 'debug' in 'opt': debug = opt['debug']

    result = list()
    if type( cmd ).__name__ == "str":
        cmd = shlex.split( cmd )

    prc = subprocess.Popen( cmd, universal_newlines=True, stdout=subprocess.PIPE )
    for line in prc.stdout.readlines():
        result.append( line.lstrip().rstrip() )
    return result


# Run one command, return each printed line to caller (called by "with"/"for" )
# - cmd_list    : command and arguments as list
# - opt         : dict of options
#   : debug     : debug info in function
def _run_command_line( cmd, **opt ):
    debug = False
    result = None

    if 'debug' in 'opt': debug = opt['debug']

    if type( cmd ).__name__ == "str":
        cmd = shlex.split( cmd )



def _read_text_file( filename, **options ):
    debug = set_debug( **options )
    with_comments = False
    if 'with_comments' in options and options['with_comments'] in (True, False):
        with_comments = options['with_comments']

    p = pathlib.Path( filename )

    if not p.exists():
        raise RuntimeError( "ERROR: File '%s' missing" % ( filename ) )

    if not p.is_file():
        raise RuntimeError( "ERROR: File '%s' must be regular file" % ( filename ) )

    result = list()
    with p.open( mode="r", buffering = -1 ) as f:
        for line in f.readlines():

            if with_comments and len( line ) > 1:
                result.append( ( line.rstrip() ) )

            elif len( line ) > 1 and not re.match( r"^\s*#", line ):
                result.append( ( line.rstrip() ) )

    return result

## -----------------------------------------
# Read a json file and return the content as dict
# - filename    : filename
# - opt         : dict of options
#   : debug     : debug info in function
def _read_json_file( filename, **options ):
    debug = set_debug( **options )

    p = pathlib.Path( filename )

    if not p.exists():
        raise RuntimeError( "ERROR: File '%s' missing" % ( filename ) )

    if not p.is_file():
        raise RuntimeError( "ERROR: File '%s' must be regular file" % ( filename ) )

    with p.open( mode="r", buffering = -1 ) as jd:
         return json.load( jd )




if __name__ == "__main__":

    conf['debug'] = False
    conf['script'] = sys.argv.pop(0)

    
