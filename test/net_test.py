
import sys, os, json, re
from pprint import pprint
sys.path.append( "../lib" )

#from docker import Client, tls, utils
import docker
from io import BytesIO

#### Internal libs

debug = True


# Params:
# name (str): Name of the network
# driver (str): Name of the driver used to create the network
# options (dict): Driver options as a key-value dictionary


OPTIONS={
	'name':'test1',
	'driver':'bridge',
	'options': {
	      "subnet":"172.20.0.0/16",
	      "iprange":"172.20.10.0/24",
	      "gateway":"172.20.10.11"
	}
}

tls_config = docker.tls.TLSConfig( client_cert=('/vagrant/Docker/certs/cert.pem', '/vagrant/Docker/certs/key.pem'), verify=False )
cli = docker.Client( base_url='https://192.168.99.100:2376', tls=tls_config )

try:

#	ipam_config = docker.utils.create_ipam_config( OPTIONS['options'] )
	res = cli.create_network( name=OPTIONS['name'], driver=OPTIONS['driver'] )

	print("==================================")
	pprint( res )
	print("==================================")

except Exception as error:
	pprint( error )




