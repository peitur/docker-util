#!/usr/bin/python3 

import sys,os,re,getopt
import json

from pprint import pprint

import Dockerfile

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
			data.append( line.lstrip() )

	except Exception as error:
		pprint(error)

	if debug: print("DEBUG: Read %(ln)s lines from %(fn)s" % {'ln': len( data ), 'fn':filename } )

	return json.loads( "\n".join( data ) )


def store_dockerfile( filename, **options ):


	if 'debug' in options and options['debug'] in [True, False]: debug = options['debug']
	if 'test' in options and options['test'] in [True, False]: test = options['test']


	return True

def build_image( dfcnt_list, **options ):

	debug = False
	test = False

	input_data = dfcnt_list
	outputfile = None

	if 'debug' in options and options['debug'] in [True, False]: debug = options['debug']
	if 'test' in options and options['test'] in [True, False]: test = options['test']

	cli = None

	try:

		response = [line for line in cli.build( fileobj=f, rm=True, tag=config['tag'] )]

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

	dfcnt_list = Dockerfile.Dockerfile.build_from_config( read_json( json_file, **options ), **options )

	if not outputfile:
		print( "\n".join( dfcnt_list) ) 

	return dfcnt_list

def print_help( **options ):
	print("HELP")
	pass




#################################
if __name__ == "__main__":

	options = {}
	options['debug'] = False
	options['test'] = False

	options['script'] = sys.argv.pop(0)
	options['command'] = None
	
	if len( sys.argv ) > 0:
		options['command'] = sys.argv.pop(0)
	else:
		print_help( **options )
		sys.exit(-1)

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hdtf:o:", ["help", "debug","test","file=", "output="])
	except getopt.GetoptError as err:
		print(err) # will print something like "option -a not recognized"
		print_help( **options )
		sys.exit(2)

	for o, a in opts:
		if o in ["-d","--debug"]: options['debug'] = True
		elif o in ["-t","--test"]: options['test'] = True
		elif o in ["-f","--file"]: options['jsonfile'] = a
		elif o in ["-o","--output"]: options['output'] = a

	pprint( options )

	try:

		if options['command'] == 'generate':
			if not 'jsonfile' in options:
				print( "Missing josn input file")
				print_help( **options )	
			else:
				generate_dockerfile( options['jsonfile'], **options )

		elif options['command'] == 'build':
			pass
	#		build_image( generate_dockerfile( options['jsonfile'], options ), options )	
		else:
			print_help( **options )
			sys.exit(2)

	except Exception as error:
		pprint(error)
		print_help( **options )
		sys.exit(2)


