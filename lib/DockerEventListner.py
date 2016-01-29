
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
		self.__client__ = None
		self.__run__ = True
		self.__monitor__ = []

		if 'client' in kwargs: 
			self.__client__ = kwargs['client']
		elif 'docker' in kwargs:

			tls_config = None
			if 'tls' in kwargs:
				tls_config = kwargs['tls']

			try:
				self.__client__ = docker.Client(base_url= kwargs['docker'] , tls=tls_config )
			except Exception as error:
				raise error


	def run( self ):
		if not self.__client__: 
			raise RuntimeError( "ERROR: Client not initialized")

		for evnt in self.__client__.events( decode=True ):

			if not self.__run__: break

			pprint( evnt )


	def stop( self ):
		self.__run__ = False


class DockerEventListner( object ):
	__instance = None

	def __new__( self, *args, **kwargs ):
		if not DockerEventListner.__instance:
			print("Started singleton...")
			DockerEventListner.__instance = super( DockerEventListner, self ).__new__( self )
        
			DockerEventListner.__instance.__thread__ = DockerEventThread( *args, **kwargs )
			DockerEventListner.__instance.__thread__.start()
			
		return DockerEventListner.__instance

	def instance( *args, **kwargs ):
		if not DockerEventListner.__instance:
			 DockerEventListner.__instance = DockerEventListner( *args, **kwargs )

		return DockerEventListner.__instance


	def register_container( self, id ):
		pass

	def join( self ):
		DockerEventListner.__instance.__thread__.join()

	def stop( self ):
		try:
			if DockerEventListner.__instance.__thread__.is_alive( ) : DockerEventListner.__instance.__thread__.stop( )
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
