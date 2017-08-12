#!/usr/bin/env python3


import os, re, sys, getopt
import multiprocessing
import subprocess, shlex
import json, pathlib
from pprint import pprint


## =============================================================
## utils
## =============================================================

## -----------------------------------------
# dirtree: builds rec. file list
# - path        : root path to start from
# - rx          : regexp used to filer wanted files
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
# _run_command: Run one command,
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

## ----------------------------------
# _run_command_line: Run one command, return each printed line to caller (called by "with"/"for" )
# - cmd_list    : command and arguments as list
# - opt         : dict of options
#   : debug     : debug info in function
def _run_command_line( cmd, **opt ):
    debug = False
    result = None

    if 'debug' in 'opt': debug = opt['debug']

    if type( cmd ).__name__ == "str":
        cmd = shlex.split( cmd )


## -----------------------------------------
# _read_text_file: read a text file
# - cmd_list    : command and arguments as list
# - opt         : dict of options
#   : debug     : debug info in function
# Returns: string list of all lines
def _read_text_file( filename, **options ):
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
# _read_json_file: Read a json file and return the content as dict
# - filename    : filename
# - opt         : dict of options
#   : debug     : debug info in function
# Returns: the json structure as a dict
def _read_json_file( filename, **options ):
    p = pathlib.Path( filename )

    if not p.exists():
        raise RuntimeError( "ERROR: File '%s' missing" % ( filename ) )

    if not p.is_file():
        raise RuntimeError( "ERROR: File '%s' must be regular file" % ( filename ) )

    with p.open( mode="r", buffering = -1 ) as jd:
         return json.load( jd )


def print_help( **opt ):
    print("# Help: %s" % ( opt['script'] ) )
    pprint( opt )


if __name__ == "__main__":

    conf = dict()
    conf['debug'] = False
    conf['help'] = False
    conf['config-file'] = None
    conf['target-file'] = None
    conf['build-dir'] = None
    conf['version'] = None
    conf['tags'] = None

    conf['script'] = sys.argv.pop(0)

    options = dict()

    try:
        opts, args = getopt.getopt(sys.argv, "hdc:d:b:v:T:", ["help", "debug","config=","target-file=","build-dir=","version=","tags="])
    except getopt.GetoptError as err:
        print(err) # will print something like "option -a not recognized"
        print_help( **options )
        sys.exit(2)

    for o, a in opts:
        if o in ("-d","--debug"): conf['debug'] = True
        elif o in ("-h","--help"): conf['help'] = True
        elif o in ("-c","--config"): conf['config-file'] = a
        elif o in ("-b", "--build-dir"): conf['build-dir'] = a
        elif o in ("-t", "--target-file"): conf['target-file'] = a
        elif o in ("-v", "--version"): conf['version'] = a
        elif o in ("-T", "--tags"): conf['tags'] = a

    if conf['tags']:
        conf['tags'] = re.split(",", conf['tags'] )

    try:
        if not conf['config-file']: raise RuntimeError("Missing configuration file!")
        if not conf['version']: raise RuntimeError("Missing build version!")
        if not conf['build-dir']: raise RuntimeError("Missing build directory!")

    except Exception as e:
        print( "ERROR: %s" % (e) )
        sys.exit(1)

    try:
        options = _read_json_file( conf['config-file'] )
    except Exception as e:
        print("EROOR Failed to parse configuration")
        print("ERROR: %s" % (e))

    pprint( conf )
    pprint( options )

sys.exit(0)
