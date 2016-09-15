#!/usr/bin/python3

import sys,os,re,getopt
import json

from docker import Client, tls
from io import BytesIO

from pprint import pprint

import Dockerfile

COLORS={
	"normal" : '\033[0m'
	"black" : '\033[30m'
	"red" : '\033[31m'
	"green" : '\033[32m'
 	"organge" : '\033[33m'
	"blue" :'\033[34m'
	"purple" :'\033[35m'
	"cyan" : '\033[36m'
	"yellow" : '\033[93m'
	"pink" : '\033[95m'
	"darkgray" : '\033[90m'
	"lightgray" : '\033[37m'
	"lightred" : '\033[91m'
	"lightgreen" : '\033[92m'
	"lightbleu" : '\033[94m'
	"lightcyan" : '\033[96m'
}

##############################################################
DEFAULT_OUTPUT="Dockerfile"
HELP_INFO={
	"generate":{
		"description":"Generate a Dockerfile",
		"options":[
			{ "params":["h","help"], "default":None, "description":"Help" },
			{ "params":["d","debug"], "default":None, "description":"debug" },
			{ "params":["t","test"], "default":None, "description":"test" },
			{ "params":["i","in"], "default":None, "description":"input file" },
			{ "params":["o","out"], "default":DEFAULT_OUTPUT, "description":"output file" }
	]},
	"run":{
		"description":"Generate a docker images",
		"options":[
			{ "params":["h","help"], "default":None, "description":"Help" },
			{ "params":["d","debug"], "default":None, "description":"debug" },
			{ "params":["t","test"], "default":None, "description":"test" },
			{ "params":["i","in"], "default":None, "description":"input file" }
	]}
}


##############################################################
def read_json( filename, **options ):
	'''
		Read a json file
		filename: filename
		options:
			- debug : toggle debugging

		Returns: term
	'''
	data = []

	debug = False
	if 'debug' in options and options['debug'] in [True, False]: debug = options['debug']

	if debug: print("DEBUG: Reading file %(fn)s" % {'fn': filename } )

	try:

		for line in open( filename, "r"):
			data.append( line.rstrip().lstrip() )

	except Exception as error:
		pprint(error)

	if debug: print("DEBUG: Read %(ln)s lines from %(fn)s" % {'ln': len( data ), 'fn': filename } )
	if debug:
		pprint( data )

	return json.loads( "\n".join( data ) )


def store_dockerfile( filename, data, **options ):


	if 'debug' in options and options['debug'] in [True, False]: debug = options['debug']
	if 'test' in options and options['test'] in [True, False]: test = options['test']

	fd = open( filename, "w" )
	fd.write( data )
	fd.close()

	return True

def build_image( df, **options ):

	debug = False
	test = False

	input_data = df

	if 'debug' in options and options['debug'] in [True, False]: debug = options['debug']
	if 'test' in options and options['test'] in [True, False]: test = options['test']

	cli = Client( )

	try:

		f = BytesIO( df.as_string().encode('utf-8'))
		response = [line for line in cli.build( fileobj=f, rm=True, tag=df.get_tag() )]

		if debug:
			print("=========================================")
			pprint( response )
			print("=========================================")


		xty = eval( response[-1].decode() )
		if 'stream' in xty and re.match( r"^Successfully", xty['stream'] ):
			print("Completed build")
			return True

		elif 'errorDetail' in xty:
			print("Error in build: %(err)s" % {'err': xty['errorDetail']['message'] })
			return False

		else:
			print("Unexpected result: ")
			pprint( xty )
			return False


	except Exception as error:
		pprint( error )
		return False

	return True


def generate_dockerfile( json_file, **options ):

	debug = False
	test = False

	dfcnt_list = []
	outputfile = None

	if 'debug' in options and options['debug'] in [True, False]: debug = options['debug']
	if 'test' in options and options['test'] in [True, False]: test = options['test']

	if 'output' in options: outputfile = options['output']

	return Dockerfile.Dockerfile.build_from_config( read_json( json_file, **options ), **options )

def print_help( **options ):

	print("Usage : <subcommands> [options]")
	print("This tool generates Dockerfiles from a simple json file and can also build the image in one go.")

	for subcmd in sorted( HELP_INFO ):
		part = HELP_INFO[subcmd]

		print("\n\t%(cmd)-32s%(descr)-64s" % {'cmd': subcmd, 'descr':part['description'] } )
		for opt in part['options']:
			sopt = "-"+opt['params'][0]
			lopt = "--"+opt['params'][1]
			print("\t\t%(sopt)2s %(lopt)-20s %(descr)-32s" % {'sopt':sopt, 'lopt': lopt, 'descr': opt['description'] } )



#################################
if __name__ == "__main__":


	debug = False
	test = False

	options = {}
	options['script'] = sys.argv.pop(0)
	options['command'] = None

	options['output'] = DEFAULT_OUTPUT
	options['storefile'] = None
	options['print'] = False

	if len( sys.argv ) > 0:
		options['command'] = sys.argv.pop(0)
	else:
		print_help( **options )
		sys.exit(-1)

	try:
		opts, args = getopt.getopt(sys.argv, "phdti:o:", ["print","help", "debug","test","in=", "out=","output="])
	except getopt.GetoptError as err:
		print(err) # will print something like "option -a not recognized"
		print_help( **options )
		sys.exit(2)

	for o, a in opts:
		if o in ["-d","--debug"]: debug = True
		elif o in ["-t","--test"]: test = True
		elif o in ["-p","--print"]: test = True
		elif o in ["-i","--in"]: options['jsonfile'] = a
		elif o in ["-o","--out"]: options['output'] = a


	options['debug'] = debug
	options['test'] = test


	try:

		if debug: pprint( options )

		if options['command'] == 'help':
			print_help( **options )

		elif options['command'] == 'generate':

			if not 'jsonfile' in options:
				print( "Missing josn input file input")
				print_help( **options )

			else:

				df = generate_dockerfile( options['jsonfile'], **options )

				if options['print'] :
					print( "\n".join( df.as_list() ) )

				if not options['test']:
					store_dockerfile( options['output'], "\n".join( df.as_list() ) , **options )

		elif options['command'] == 'build':

			df = generate_dockerfile( options['jsonfile'], **options )

			build_image( df, **options )

		else:
			print_help( **options )
			sys.exit(2)

	except Exception as error:
		pprint(error)
		print_help( **options )
		sys.exit(2)
