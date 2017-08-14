#!/usr/bin/env python3


import os, re, sys, getopt
import multiprocessing
import subprocess, shlex
import json, pathlib
import random, string

from pprint import pprint

COMMANDS={
    "yum":{
        "cmd":"yum",
        "config":"/etc/yum.conf",
        "target":None,
        "action":"install",
        "options":["tsflags=nodocs","group_package_types=mandatory"],
        "args":["--releasever=/", "-y","--nogpgcheck"],
        "list":None
    },
    "mknod":{
        "cmd":"mknod",
        "mode":"666",
        "path":None,
        "type":"c",
        "minor":None,
        "major":None
    },
    "mkdir":{
        "cmd":"mkdir",
        "mode":None,
        "args":["-p"],
        "path":None
    },
    "chroot":{
        "cmd":"chroot",
        "path":None,
        "exec":"/bin/bash",
        "name":"EOF",
        "run":[]
    },
    "copy":{
        "cmd":"cp",
        "args":[],
        "from":None,
        "to":None
    },
    "chmod":{
        "cmd":"chmod",
        "path":None,
        "access":None,
        "args":[]
    },
    "chown":{
        "cmd":"chown",
        "path":None,
        "user":None,
        "group":None,
        "args":[]
    },
    "rm":{
        "cmd":"rm",
        "args":[],
        "path":None
    },
    "tar":{
        "cmd":"tar",
        "args":[],
        "file":None,
        "path":None
    }
}

# mkdir -m 755 "$target"/dev
# mknod -m 600 "$target"/dev/console c 5 1
# mknod -m 600 "$target"/dev/initctl p
# mknod -m 666 "$target"/dev/full c 1 7
# mknod -m 666 "$target"/dev/null c 1 3
# mknod -m 666 "$target"/dev/ptmx c 5 2
# mknod -m 666 "$target"/dev/random c 1 8
# mknod -m 666 "$target"/dev/tty c 5 0
# mknod -m 666 "$target"/dev/tty0 c 4 0
# mknod -m 666 "$target"/dev/urandom c 1 9
# mknod -m 666 "$target"/dev/zero c 1 5

DEVICES=[
#     { 'file': "", 'mode':"", 'type':"", "major":"", "minor":"" }
    { 'file': "/dev/console", 'mode':"600", 'type':"c", "major":"5", "minor":"1" },
    { 'file': "/dev/initctl", 'mode':"666", 'type':"p", 'major':None, 'minor': None },
    { 'file': "/dev/full", 'mode':"666", 'type':"c", "major":"1", "minor":"7" },
    { 'file': "/dev/null", 'mode':"666", 'type':"c", "major":"1", "minor":"3" },
    { 'file': "/dev/ptmx", 'mode':"666", 'type':"c", "major":"5", "minor":"2" },
    { 'file': "/dev/random", 'mode':"666", 'type':"c", "major":"1", "minor":"8" },
    { 'file': "/dev/tty", 'mode':"666", 'type':"c", "major":"5", "minor":"0" },
    { 'file': "/dev/tty0", 'mode':"666", 'type':"c", "major":"4", "minor":"0" },
    { 'file': "/dev/urandom", 'mode':"666", 'type':"c", "major":"1", "minor":"9" },
    { 'file': "/dev/zero", 'mode':"666", 'type':"c", "major":"1", "minor":"5" }
]


## =============================================================
## utils
## =============================================================

def random_string(length):
   return ''.join( random.choice( string.ascii_lowercase  ) for i in range(length))

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


def _build_yum_command( lst, **opt ):

    y = dict( COMMANDS['yum'] )
    result = list()


    if type( lst ).__name__ == "str": lst = [ lst ]
    if 'target' in opt: y['target'] = [ "--installroot=%s" %( opt['target'] ) ]
    if 'action' in opt: y['action'] = opt['action']
    if 'config' in opt: y['config'] = opt['config']
    if 'options' in opt: y['options'] = opt['options']
    if 'args' in opt: y['args'] = opt['args']
    y['list'] = lst

    if not y['target']: raise RuntimeError("No target directory specified.")
    if not y['list']: raise RuntimeError("No packages/groups to install given.")

    result.append( y['cmd'] )

    if 'config' in y and y['config']:
        result.append( '-c' )
        result.append( y['config'] )

    if y['target'] and len( y['target'] ) > 0:
        for x in y['target']: result.append( x )

    for x in y['options']:
        result.append( "--setopt=%s" % ( x ) )

    result.append( y['action'] )
    for x in y['args']: result.append( x )
    for x in y['list']: result.append( x )

    return result


def _build_mknod_command( path, ntype='c', **opt ):
    n = dict( COMMANDS['mknod'] )
    result = list()

    n['path'] = re.sub( r"\/+", "/", path )
    n['type'] = ntype

    if 'mode' in opt: n['mode'] = opt['mode']
    if 'major' in opt: n['major'] = opt['major']
    if 'minor' in opt: n['minor'] = opt['minor']

    if not n['path']: raise RuntimeError( "No mknod path given")

    result.append( n['cmd'] )
    result.append( path )
    if n['mode']:
        result.append( "-m" )
        result.append( n['mode'] )

    result.append( n['type'] )
    if opt['major']: result.append( n['major'] )
    if opt['minor']: result.append( n['minor'] )

    return result

def _build_devices( buildroot, dev_list, **opt ):
    result = list()

    for d in dev_list:
        path = re.sub( r"\/+", "/", "%s/%s" % ( buildroot, d['file'] ) )
        result.append( _build_mknod_command( path, d['type'], mode=d['mode'], minor=d['minor'], major=d['major'] ) )
    return result

def _build_mkdir_command( path, **opt ):
    n = dict( COMMANDS['mkdir'] )
    result = list()

    n['path'] = re.sub( r"\/+", "/", path )

    if 'mode' in opt: n['mode'] = opt['mode']
    if 'args' in opt: n['args'] = opt['args']

    if not n['path']: RuntimeError( "No mkdir path given.")

    result.append( n['cmd'] )
    if n['args']:
        for x in n['args']:
            result.append( x )

    if n['mode']:
        result.append( "-m" )
        result.append( n['mode'] )

    result.append( n['path'] )

    return result

def _build_chroot_command( path, runlist=[], **opt ):
    n = dict( COMMANDS['chroot'] )
    result = list()

    n['path'] = re.sub( r"\/+", "/", path )

    if not n['path']: RuntimeError( "No chroot path given.")

    result.append( "%s %s %s <<%s" % ( n['cmd'], path, n['exec'], n['name'] ) )
    result.append( runlist )
    result.append( n['name'] )

    return result


def _build_copy_command( fromfile, tofile, **opt ):
    n = dict( COMMANDS['copy'] )
    result = list()

    n['from'] = re.sub( r"\/+", "/", fromfile )
    n['to'] = re.sub( r"\/+", "/", tofile )

    if 'args' in opt: n['args'] = opt['args']

    if not n['from']: RuntimeError( "No copy from path given.")
    if not n['to']: RuntimeError( "No copy to path given.")

    result.append( n['cmd'] )

    if n['args']:
        for x in n['args']:
            result.append( x )

    result.append( n['from'] )
    result.append( n['to'] )

    return result

def _build_rm_command( path, **opt ):
    n = dict( COMMANDS['rm'] )
    result = list()

    n['path'] = re.sub( r"\/+", "/", path )

    if not n['path']: RuntimeError( "No remove path given.")
    if 'args' in opt: n['args'] = opt['args']

    result.append( n['cmd'] )
    for x in n['args']:
        result.append( x )

    result.append( n['path'] )

    return result


def _build_chmod_command( path, access, **opt ):
    n = dict( COMMANDS['chmod'] )
    result = list()

    n['path'] = re.sub( r"\/+", "/", path )
    n['access'] = access

    if not n['path']: RuntimeError( "No chmod path given.")
    if not n['access']: RuntimeError( "No chmod access given.")

    if 'args' in opt: n['args'] = opt['args']

    result.append( n['cmd'] )
    for x in n['args']:
        result.append( x )

    result.append( n['access'] )
    result.append( n['path'] )

    return result


def _build_chown_command( path, user, group, **opt ):
    n = dict( COMMANDS['chown'] )
    result = list()

    n['path'] = re.sub( r"\/+", "/", path )
    n['user'] = user
    n['group'] = group

    if 'args' in opt: n['args'] = opt['args']

    if not n['path']: RuntimeError( "No chown path given.")
    if not n['user']: RuntimeError( "No chown user given.")
    if not n['group']: RuntimeError( "No chown group given.")


    result.append( n['cmd'] )
    for x in n['args']:
        result.append( x )

    result.append( "%s:%s" %( n['user'], n['group'] ) )
    result.append( n['path'] )

    return result



def _build_tar_command( filename, path, **opt ):
    n = dict( COMMANDS['tar'] )
    result = list()

    n['file'] = re.sub( r"\/+", "/", filename )
    n['path'] = re.sub( r"\/+", "/", path )
    if 'args' in opt: n['args'] = opt['args']


    if not n['file']: RuntimeError( "No tar target file given.")
    if not n['path']: RuntimeError( "No tar source path given.")

    result.append( n['cmd'] )
    for x in n['args']:
        result.append( x )

    result.append( n['file'] )
    result.append( n['path'] )

    return result


## -----------------------------------------
# run_command: Run one command,
# - cmd_list    : command and arguments as list
# - opt         : dict of options
#   : debug     : debug info in function
def run_command( cmd, **opt ):
    debug = False
    test = False
    if 'debug' in opt: debug = opt['debug']
    if 'test' in opt: test = opt['test']

    result = list()
    if type( cmd ).__name__ == "str":
        cmd = shlex.split( cmd )

    if debug: pprint( cmd )

    prc = subprocess.Popen( cmd, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
    for line in prc.stdout.readlines():
        print( "DEBUG: %s" % ( line.lstrip().rstrip() ) )
        result.append( line.lstrip().rstrip() )
    return result

## ----------------------------------
# run_command_line: Run one command, return each printed line to caller (called by "with"/"for" )
# - cmd_list    : command and arguments as list
# - opt         : dict of options
#   : debug     : debug info in function
def run_command_line( cmd, **opt ):
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

def _write_text_file( filename, data, **options ):

    filename = re.sub( r"\/+", "/", filename )

    if type( data ).__name__ == "list":
        data = "\n".join( data )

    pprint( [ "%s" % (filename) , data ] )
#    fd = open( filename, "w" )
#    fd.write( data )
#    fd.close()

def _write_json_file( filename, data, **options  ):
    pass


def print_help( **opt ):
    print("# Help: %s" % ( opt['script'] ) )
    pprint( opt )


if __name__ == "__main__":

    conf = dict()
    conf['debug'] = False
    conf['test'] = True
    conf['random-string'] = random_string( 8 )

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

    if not os.path.exists( conf['build-dir'] ):
        print("# -- Creating workdir %s" % ( conf['build-dir']) )
        os.makedirs( conf['build-dir'] )

    if os.environ[ "USER" ] != "root":
        print("# EE Must be root to run this ...")
        sys.exit(1)

    for cnt in options:
        found_error = False
        bdir = "%s_%s" % ( conf['build-dir'], conf['random-string'] )
        print("# --------------------------------------------------")
        print("# Processing container %s-%s Building in %s..."  % ( cnt['name'], cnt['version'], bdir ) )

        command_list = list()

    # 1. create build dir
    # 2. create device nodes
    # 3. prepare yum and yum repos
    # 4. install base packages with yum target
        print("# -- Create base devices...")
        run_command( _build_mkdir_command( "%s/%s" % (bdir, "/dev"), mode="755", args=["-p"], debug=conf['debug'] ), debug=conf['debug'] )
        for d in _build_devices( bdir, DEVICES, debug=conf['debug'] ):
            run_command( d, debug=conf['debug'] )

        print("# -- Copy GPG keys to new yum env.")
        run_command( _build_mkdir_command( "%s/%s" % (bdir, "/etc/pki"), mode="0755", args=['-p'], debug=conf['debug'] ), debug=conf['debug'] )
        run_command( _build_copy_command( "/etc/pki/rpm-gpg", "%s/%s" % (bdir, "/etc/pki/rpm-gpg" ), args=['-r'], debug=conf['debug'] ), debug=conf['debug'] )

        if len( cnt['repo-files'] ) > 0:
            print("# -- Copying system repo files into container...")
            run_command( _build_mkdir_command( "%s/%s" % (bdir, "/etc/yum.repos.d"), mode="0755", args=['-p'], debug=conf['debug'] ), debug=conf['debug'] )
            for rf in cnt['repo-files']:
                run_command( _build_copy_command( rf , "%s/%s" % (bdir, rf ), debug=conf['debug'] ), debug=conf['debug'] )

        if len( cnt['base-group'] ) > 0:
            print("# -- YUM Install base group...")
            run_command( _build_yum_command( cnt['base-group'], target=bdir, action="groupinstall" , debug=conf['debug']), debug=conf['debug'] )

        if len( cnt['base-packages'] ) > 0:
            print("# -- YUM Install base packages...")
            run_command( _build_yum_command( cnt['base-packages'], target=bdir, action="install", debug=conf['debug'] ), debug=conf['debug'] )

        if len( cnt['install-groups'] ) > 0:
            print("# -- YUM Install requested groups...")
            run_command( _build_yum_command( cnt['install-groups'], target=bdir, action="groupinstall" , debug=conf['debug']), debug=conf['debug'] )

        if len( cnt['install-packages'] ) > 0:
            print("# -- YUM Install requested packages...")
            run_command( _build_yum_command( cnt['install-packages'], target=bdir, action="install", debug=conf['debug'] ), debug=conf['debug'] )

        print("# --  YUM clean all ...")
        run_command( _build_yum_command( ['all'], target=bdir, options=[], args=["-y"], action="clean" , debug=conf['debug']), debug=conf['debug'] )


        print("# -- Clean up unwanted files, strip to minimize...")
        for strp in cnt['strip-paths']:
            print("# ---- Stripping: %s" % ( strp ) )
            run_command( _build_rm_command( "%s/%s" % (bdir, strp ), args=['-fR'], debug=conf['debug'] ), debug=conf['debug'] )

        print("# --- Clenaing yum cached files ... ")
        run_command( _build_rm_command( "%s/%s" % (bdir, "/var/cache/yum"), args=['-fR'], debug=conf['debug'] ), debug=conf['debug'] )
        run_command( _build_mkdir_command( "%s/%s" % (bdir, "/var/cache/yum"), mode="0755", args=['-p'], debug=conf['debug'] ), debug=conf['debug'] )

        print("# --- Cleaning ldconfig caches ...")
        run_command( _build_rm_command( "%s/%s" % (bdir, "/etc/ld.so.cache"), args=['-fR'], debug=conf['debug'] ), debug=conf['debug'] )
        run_command( _build_rm_command( "%s/%s" % (bdir, "/var/cache/ldconfig"), args=['-fR'], debug=conf['debug'] ), debug=conf['debug'] )
        run_command( _build_mkdir_command( "%s/%s" % (bdir, "/var/cache/ldconfig"), mode="0755", args=['-p'], debug=conf['debug'] ), debug=conf['debug'] )


        print("# -- Enable networking...")
        _write_text_file( "%s/%s" % ( bdir, "/etc/sysconfig/network"), [ "NETWORKING=yes","HOSTNAME=localhost.localdomain" ] )

        print("# -- Copying system files into container...")
        run_command( _build_copy_command( "/etc/hosts", "%s/%s" % (bdir, "/etc/hosts"), debug=conf['debug'] ), debug=conf['debug'] )


        if len( cnt['post-script'] ) > 0:
            for scr in cnt['post-script']:
                print("# -- Clean up unwanted files, strip to minimize...")
                # run_command( _build_chroot_command( bdir, ["ls", "pwd"], debug=conf['debug'] ))

        print("# -- Build resulting contained image file...")
        run_command( _build_tar_command( "%s-%s.tgz" % ( cnt['name'], cnt['version'] ), bdir, args=['--numeric-owner','--directory=%s'%(bdir),'-cf'], debug=conf['debug'] ), debug=conf['debug'] )

        if not found_error and not conf['debug']:
            print("# -- Clenaing up build dir %s..." % ( bdir ) )
            run_command( _build_rm_command( bdir, args=['-fR'], debug=conf['debug'] ), debug=conf['debug'] )

sys.exit(0)
