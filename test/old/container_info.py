
import sys, os, json, re
from pprint import pprint
sys.path.append( "../lib" )

#from docker import Client, tls, utils
import docker
from io import BytesIO

#### Internal libs

'''

 Container:
 {'Command': '/usr/bin/sleep 120',
  'Created': 1453811936,
  'HostConfig': {'NetworkMode': 'default'},
  'Id': 'd542535a709ac70178fef87880127665babdb07a6f33cb08d7df29944bd8ee2e',
  'Image': 'peitur/testing',
  'ImageID': '33668c52cc589a68586d9b58d88a323991618e8c43322c5461a7f5368f3fe890',
  'Labels': {'build-date': '2015-12-23',
             'license': 'GPLv2',
             'name': 'CentOS Base Image',
             'vendor': 'CentOS'},
  'Names': ['/condescending_bohr'],
  'Ports': [{'PrivatePort': 8080, 'Type': 'tcp'},
            {'PrivatePort': 2121, 'Type': 'tcp'}],
  'Status': 'Up 14 seconds'},

Network:
{'Containers': {},
  'Driver': 'bridge',
  'IPAM': {'Config': [{'Gateway': '172.17.0.1', 'Subnet': '172.17.0.1/16'}],
           'Driver': 'default'},
  'Id': '4fb5884a72805418ce8e7f47ef8fc706b612dcfb976fcdd2c170e86f87184c1c',
  'Name': 'bridge',
  'Options': {'com.docker.network.bridge.default_bridge': 'true',
              'com.docker.network.bridge.enable_icc': 'true',
              'com.docker.network.bridge.enable_ip_masquerade': 'true',
              'com.docker.network.bridge.host_binding_ipv4': '0.0.0.0',
              'com.docker.network.bridge.name': 'docker0',
              'com.docker.network.driver.mtu': '1500'},
  'Scope': 'local'},


Image:
{'Created': 1450971011,
  'Id': 'c8a648134623c453dc62abcd747eafa40af057e28cd5937baeebe2ed4c32094e',
  'Labels': {'build-date': '2015-12-23',
             'license': 'GPLv2',
             'name': 'CentOS Base Image',
             'vendor': 'CentOS'},
  'ParentId': '86bcb57631bd122c32b8e277b64b45ac00382e78e0d21530a50c090fd739d0ee',
  'RepoDigests': [],
  'RepoTags': ['centos:latest'],
  'Size': 0,
  'VirtualSize': 196641664}

{'Created': 1453923510,
  'Id': '166fbc6794bc86401e97511f9ddb5f3ce7e6edf4551efc4fc53681db5c248f55',
  'Labels': {'build-date': '2015-12-23',
             'license': 'GPLv2',
             'name': 'CentOS Base Image',
             'vendor': 'CentOS'},
  'ParentId': 'eac8ecd63574efaa0ce4223d86cefb71504276ddf76e6b36d01a459e09e48d9e',
  'RepoDigests': [],
  'RepoTags': ['peitur/dtestnginx:latest'],
  'Size': 0,
  'VirtualSize': 471566943},



## Container inspect Status (when start fails)
'State': {'Dead': False,
           'Error': '[8] System error: exec: "/usr/bin/slee": stat '
                    '/usr/bin/slee: no such file or directory',
           'ExitCode': -1,
           'FinishedAt': '0001-01-01T00:00:00Z',
           'OOMKilled': False,
           'Paused': False,
           'Pid': 0,
           'Restarting': False,
           'Running': False,
           'StartedAt': '0001-01-01T00:00:00Z',
           'Status': 'created'}}

'''

tls_config = docker.tls.TLSConfig( client_cert=('/vagrant/Docker/certs/cert.pem', '/vagrant/Docker/certs/key.pem'), verify=False )
cli = docker.Client( base_url='https://192.168.99.100:2376', tls=tls_config )

try:

	res = cli.volumes()
	print("===========VOLUMES=======================")
#	for r in res:
#		print(">>>>> "+ r['Id'] +" <<<<<")
#		pprint( cli.inspect_image( r['Id'] ) )
	pprint( res )
	print("=========================================")


	res = cli.images()
	print("===========IMAGES=======================")
	for r in res:
		print(">>>>> "+ r['Id'] +" <<<<<")
#		pprint( cli.inspect_image( r['Id'] ) )
	pprint(res )
	print("========================================")

	res = cli.networks()
	print("===========NETWORKS=======================")
	for r in res:
		print(">>>>> "+ r['Id'] +" <<<<<")
#		pprint( cli.inspect_network( r['Id'] ) )
	pprint(res )
	print("==========================================")

	res = cli.containers( all=True)
	print("===========CONTAINERS=======================")
	for r in res:
		print(">>>>> "+ r['Id'] +" <<<<<")
		pprint( cli.inspect_container( r['Id'] ) )
#	pprint(res )
	print("============================================")


	containers = {}
	print("===========EVENTS=======================")	

	for ev in cli.events( decode=True ):

#		pprint( ev )
		if ev['status'] == 'create':
			print("Reg: %(cont)s" % { 'cont': ev['id'] } )
			containers[ ev['id'] ] = ev


		if ev['status'] == 'die':
			start_time = containers[ ev['id'] ]['time']
			stop_time = ev['time']

			if ( stop_time - start_time ) < 10:
				print("WARN: Short runtime ( %(delta)s seconds)!! Suspected crash with container %(cont)s %(img)s" % { 'delta': stop_time - start_time ,'cont': ev['id'], 'img': ev['from'] } )
				pprint( ev )

			if ev['id'] in containers: del containers[ ev['id'] ]

		pprint( containers )
	print("========================================")

except Exception as error:
	pprint( error )


