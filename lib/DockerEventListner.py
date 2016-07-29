
import sys, os, json, re, time
from pprint import pprint
sys.path.append( "../lib" )

#from docker import Client, tls, utils
import docker
import threading, queue

from io import BytesIO




## When a died container is detected, automatically remote the container.
## 1. check exit status of container, if error then  extract logs and store
## 2. remove the container.
class DockerEventThread( threading.Thread ):

	def __init__( self, *args, **kwargs ):
		threading.Thread.__init__(self)

		self.__client = None
		self.__run = True
		self.__monitor = {}
		self.__health_time = 60
		self.__debug = False

		if 'debug' in kwargs and kwargs['debug'] in [True,False]: self.__debug = kwargs['debug']
		if 'health_time' in kwargs: self.__health_time = kwargs['health_time']

		if 'client' in kwargs: 
			self.__client = kwargs['client']
		elif 'docker' in kwargs:

			tls_config = None
			if 'tls' in kwargs:
				tls_config = kwargs['tls']

			try:
				self.__client = docker.Client(base_url= kwargs['docker'] , tls=tls_config )
			except Exception as error:
				raise error




	def instance_die( self, evnt ):


		if self.__debug: pprint( evnt )

		start_time = 0
		if evnt['id'] in self.__monitor:
			start_time = self.__monitor[ evnt['id'] ]['time']
		
		stop_time = evnt['time']

		try:
			cnt_info = self.__client.inspect_container( evnt['id'] )
			'''
				State': {
				   'Dead': False,
		           'Error': '',
		           'ExitCode': 0,
		           'FinishedAt': '2016-01-29T13:23:26.889837639Z',
		           'OOMKilled': False,
		           'Paused': False,
		           'Pid': 0,
		           'Restarting': False,
		           'Running': False,
		           'StartedAt': '2016-01-29T13:23:23.866491807Z',
		           'Status': 'exited'}
		        }
			'''

	#			pprint( cnt_info )
			if ( stop_time - start_time ) <= self.__health_time :
				print("WARN: Short runtime ( %(delta)s seconds)!! %(cont)s %(img)s, OK limit is %(ok)s" % { 'ok': self.__health_time, 'delta': stop_time - start_time ,'cont': evnt['id'], 'img': evnt['from'] } )

			if cnt_info['State']['ExitCode'] < 0:
				print("ERROR: %(error)s" % {'error': cnt_info['State']['Error'] } )
				print("DUMP:")
				pprint( self.__client.logs( container=evnt['id'], timestamps=True ).decode() )
				print("END")
				self.__client.remove_container( evnt['id'], link=True, v=True )

			if evnt['id'] in self.__monitor: del self.__monitor[ evnt['id'] ]

		except Exception as error:
			if evnt['id'] in self.__monitor: del self.__monitor[ evnt['id'] ]
			pprint( error )
		


	def instance_error( self, evnt ):
		pass

	def instance_start( self, evnt ):

		if self.__debug: pprint( evnt )

		self.__monitor[ evnt['id'] ] = evnt

	def instance_create( self, evnt ):
		pass

	def instance_destroy( self, evnt ):
		pass

	def run( self ):
		if not self.__client: 
			raise RuntimeError( "ERROR: Client not initialized")

		for evnt in self.__client.events( decode=True ):
			if not self.__run: break

			'''
			{'from': 'centos',
			 'id': 'a4b39123f76e0b650e21d5b2ff082d0a8660746c2cf5d145450b5927191e6b11',
			 'status': 'destroy',
			 'time': 1454072225,
			 'timeNano': 1454072225781293611}
			'''

			if evnt['status'] == 'start':
				self.instance_start( evnt )

			if evnt['status'] == 'die':
				self.instance_die( evnt )



#				pprint( self.__client__.logs( evnt['id'] ) )
#				self.__client__.remove_container( evnt['id'], link=True, v=True )

#			pprint( evnt )


	def stop( self ):
		self.__run__ = False


class DockerEventListner( object ):
	__instance = None

	def __new__( self, *args, **kwargs ):

		self.__debug = False

		if 'debug' in kwargs and kwargs['debug'] in [True,False]: self.__debug = kwargs['debug']


		if not DockerEventListner.__instance:
			if self.__debug : print("Started singleton...")
			DockerEventListner.__instance = super( DockerEventListner, self ).__new__( self )
        
			DockerEventListner.__instance.__thread = DockerEventThread( *args, **kwargs )
			DockerEventListner.__instance.__thread.start()
			
		return DockerEventListner.__instance

	def instance( *args, **kwargs ):
		if not DockerEventListner.__instance:
			 DockerEventListner.__instance = DockerEventListner( *args, **kwargs )

		return DockerEventListner.__instance


	def register_container( self, id ):
		pass

	def join( self ):
		DockerEventListner.__instance.__thread.join()

	def stop( self ):
		try:
			if DockerEventListner.__instance.__thread.is_alive( ) : DockerEventListner.__instance.__thread.stop( )
		except Exception as error:
			pprint( error )







if __name__ == "__main__":

	tls_config = docker.tls.TLSConfig( client_cert=('/vagrant/Docker/certs/cert.pem', '/vagrant/Docker/certs/key.pem'), verify=False )
	cli = docker.Client(base_url='https://192.168.99.100:2376', tls=tls_config)


	x1 = DockerEventListner.instance( client=cli )

	print("wating...")
	
	try:
		time.sleep( 100 )
	except Exception as error:
		pprint( error )

	print("done")
	x1.stop()

	x1.join()
