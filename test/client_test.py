
import sys, os, json, re
from pprint import pprint
sys.path.append( "../lib" )

from docker import Client, tls
from io import BytesIO

#### Internal libs
import Dockerfile

debug = True


CONFIG = {
	'product':"dtestapp",
	'docker':"https://192.168.99.100:2376",
	'maintainer':"peitur@gmail.com",
	'source':"centos",
	'version':"latest",
	'name':"testing",
	'tag':'peitur/testing',
	'upgrade':True,
	'env':{ "TEST":"yes"},
	'tasks':[ ## Must be run in same order!! can contain: run, install, copy, add, volume
		{
			'comment':"Creating base dir",
			'run':'mkdir -p /tmp/test'
		},
		{
			'install':[ "python3.4", "curl", "wget"]
		},
		{
			'run':'ls > /tmp/test/list'
		},
		{
			'volume':"/tmp/test/conf"
		}
	],
	'ports':['2121',"8080"], ## ['intport':'extport'] or { "intport:extport" }
	'cmd':"/bin/sh"
}





tls_config = tls.TLSConfig( client_cert=('/vagrant/Docker/certs/cert.pem', '/vagrant/Docker/certs/key.pem'), verify=False )
cli = Client(base_url='https://192.168.99.100:2376', tls=tls_config)

try:

#	df = Dockerfile.Dockerfile( maintainer='Peter Bartha', source='centos', tag="testing", name='testing', cmd=["/bin/sh"] )
	df = Dockerfile.Dockerfile.build_from_config( CONFIG )

#	df.add_content( Dockerfile.DockerfileRun( "yum upgrade -y" ) )
#	df.add_content( Dockerfile.DockerfileRun( "yum install -y python3.4 curl wget" ) )
#	df.add_content( Dockerfile.DockerfileEnv( "TEST true" ) )
#	df.add_content( Dockerfile.DockerfilePort( "8080" ) )
#	df.add_content( Dockerfile.DockerfileEnv( "TEST true" ) )

	if debug: 
		print("=========================================")
		print( df.as_string() )
		print("=========================================")

	f = BytesIO( df.as_string().encode('utf-8'))

#	f = BytesIO( dockerfile.encode('utf-8') )
	response = [line for line in cli.build( fileobj=f, rm=True, tag=CONFIG['tag'] )]

	if debug:
		print("=========================================") 
		pprint( response )
		print("=========================================")


	xty = eval( response[-1].decode() )
	if 'stream' in xty and re.match( r"^Successfully", xty['stream'] ):
		print("Completed build")
	elif 'errorDetail' in xty:
		print("Error in build: %(err)s" % {'err': xty['errorDetail']['message'] })
	else:
		print("Unexpected result: ")
		pprint( xty )



except Exception as error:
	pprint( error )




