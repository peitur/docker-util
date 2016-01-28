
import sys, os, json, re
from pprint import pprint
sys.path.append( "../lib" )

#from docker import Client, tls, utils
import docker
import threading, queue
import time
from io import BytesIO





class DockerEventThread( threading.Thread ):

	def __init__( self, *args, **kwargs ):
		threading.Thread.__init__(self)
		self.__run__ = True

		val = args[0]

		self.__val__ = val

		print("Started thread ...")


	def run( self ):
		while( self.__run__ ):
			print( "tick %(x)s" % { 'x': self.__val__ } )
			time.sleep(1)


	def register( self, val ):
		self.__val__ = val

	def stop( self ):
		self.__run__ = False


class DockerEventListner( object ):
	__instance = None

	def __new__( self, *args, **kwargs ):
		if not self.__instance:
			print("Started singleton...")
			self.__instance = super( DockerEventListner, self ).__new__( self )
        
			DockerEventListner.__instance.__thread__ = DockerEventThread( *args, **kwargs )
			DockerEventListner.__instance.__thread__.start()
			
		return self.__instance

	def register( self, val ):
		try:
			DockerEventListner.__instance.__thread__.register( val )
		except Exception as error:
			pprint( error )


	def join( self ):
		DockerEventListner.__instance.__thread__.join()

	def stop( self ):
		try:
			if DockerEventListner.__instance.__thread__.is_alive( ) : DockerEventListner.__instance.__thread__.stop( )
		except Exception as error:
			pprint( error )

if __name__ == "__main__":
	x1 = DockerEventListner( "1" )
	x2 = DockerEventListner( "2" )
	x3 = DockerEventListner( "3" )

	print("wating...")
	time.sleep(5)
	x1.register( "a" )

	time.sleep(1)
	x2.register( "b" )

	time.sleep(1)
	x3.register( "c" )

	time.sleep(2)

	print("done")
	x1.stop()
	x2.stop()
	x3.stop()

	x1.join()
	x2.join()
	x3.join()