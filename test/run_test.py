
import sys, os, json, re
from pprint import pprint
sys.path.append( "../lib" )

#from docker import Client, tls, utils
import docker
from io import BytesIO

#### Internal libs
import Dockerfile

debug = True


CONFIG_HOST_0 = {
	'product':"dtestnginx",
	'docker':"https://192.168.99.100:2376",
	'maintainer':"peitur@gmail.com",
	'source':"centos",
	'version':"latest",
	'name':"testing",
	'tag':'peitur/dtestnginx',
	'upgrade':True,
	'tasks':[ ## Must be run in same order!! can contain: run, install, copy, add, volume
		{
			'install':['epel-release']
		},
		{
			'install':['nginx']
		},
		{
			'volume':"/tmp/test/conf"
		}
	],
	'ports':['2121',"8080"], ## ['intport':'extport'] or { "intport:extport" }
	'cmd':"/bin/sh"
}


CONFIG_HOST_1 = {
	'product':"dtestapp",
	'docker':"https://192.168.99.100:2376",
	'maintainer':"peitur@gmail.com",
	'source':"centos",
	'version':"latest",
	'name':"testing",
	'tag':'peitur/dtestapp',
	'upgrade':True,
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


CONFIG_HOST_2 = {
	'product':"dtestweb",
	'docker':"https://192.168.99.100:2376",
	'maintainer':"peitur@gmail.com",
	'source':"centos",
	'version':"latest",
	'name':"testing",
	'tag':'peitur/dtestweb',
	'upgrade':True,
	'tasks':[ ## Must be run in same order!! can contain: run, install, copy, add, volume
		{
			'install':[ "curl", "wget", "httpd"]
		}
	],
	'ports':["80","443"], ## ['intport':'extport'] or { "intport:extport" }
	'cmd':"/bin/sh"
}



CONFIG_HOST_3 = {
	'product':"dtestaccess",
	'docker':"https://192.168.99.100:2376",
	'maintainer':"peitur@gmail.com",
	'source':"centos",
	'version':"latest",
	'name':"testing",
	'tag':'peitur/dtestaccess',
	'upgrade':True,
	'tasks':[ ## Must be run in same order!! can contain: run, install, copy, add, volume
		{
			'install':["curl", "wget"]
		}
	],
	'ports':["22"], ## ['intport':'extport'] or { "intport:extport" }
	'cmd':"/bin/sh"
}


HOSTS = {
	'dtestnginx': { 'min':1, 'max':1, 'config':CONFIG_HOST_0 },
	'dtestapp': { 'min':1, 'max':3, 'config':CONFIG_HOST_1 },
	'dtestweb': { 'min':1, 'max':2,'depends': ['dtestapp'], 'config':CONFIG_HOST_2 },
	"dtestaccess": { 'min':1, 'max':1, 'config':CONFIG_HOST_3 }
}

def build_image( cli, config ):

	if debug:
		print("=========================================") 
		pprint( config )
		print("=========================================")


	try:
		df = Dockerfile.Dockerfile.build_from_config( config )

		if debug: 
			print("=========================================")
			print( df.as_string() )
			print("=========================================")

		f = BytesIO( df.as_string().encode('utf-8'))

	#	f = BytesIO( dockerfile.encode('utf-8') )
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


#######################################################
tls_config = docker.tls.TLSConfig( client_cert=('/vagrant/Docker/certs/cert.pem', '/vagrant/Docker/certs/key.pem'), verify=False )
cli = docker.Client(base_url='https://192.168.99.100:2376', tls=tls_config)


# pprint( HOSTS )
hostdep = {}
for cf in HOSTS:
	# First, lets build the images
	build_image( cli, HOSTS[ cf ][ 'config' ] )
	if 'depends' in HOSTS[ cf ]:
		hostdep[ cf ] = HOSTS[ cf ]['depends']
		print( ">>> %(cf)s depends on %(dep)s" % { 'cf': cf, 'dep': ",".join( hostdep[ cf ] ) } )

	print("## %(app)s minimum %(min)s maxumum %(max)s workers" % { 'app': cf ,'min': HOSTS[ cf ]['min'] ,'max': HOSTS[ cf ]['max'] } ) 

