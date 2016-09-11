#!/usr/bin/env python3.4

import os,sys,re
import json

from pprint import pprint

def load_json( filename, **options ):
	data = []
	for line in open( filename, "r" ):
		data.append( line.rstrip() )

	return json.loads( "".join( data ) )


def extract_variable( line, **options ):
	var = []

	extr_re = re.compile( r"%%([a-z0-9]+)%%" )
	for m in extr_re.finditer( line ):
		var.append( m.group(1) )

	return var

def apply_variable( line, var, val, **options ):
	return re.sub( r'%%'+var+'%%', val, line )


if __name__ == "__main__":

	filename = "test.json"
	d = load_json( filename )

	pprint(d)

	x = []
	for line in d['data']:
		vlist = extract_variable( line )
		if len( vlist ) > 0:
			for v in vlist:
				if v in d['var']:
					line = apply_variable( line, v, d['var'][v] )
#				else:
#					x.append( line )

			x.append( line )

		else:
			x.append( line )


	pprint( x )