
import sys, os, json, re
from pprint import pprint
sys.path.append( "../lib" )

#from docker import Client, tls, utils
import docker
import threading, queue
from io import BytesIO



SUPPORTED_CACHE_TYPES = ['image','container','network','volume']

class DockerObjectCache:

	def __init__(self), client = None ) :
		self._client = client

		self._dirty = True
		self._content = None


	def refresh( self ):
		self._dirty = True

		return self._dirty

	def is_dirty( self ):
		return self._dirty



class DockerImageCache( DockerObjectCache ):
	def __init__(self, client = None ):
		super().__init__( self )

class DockerContainerCache( DockerObjectCache ):
	def __init__(self, client = None):
		super().__init__( self )

class DockerNetworkCache( DockerObjectCache ):
	def __init__(self, client = None):
		super().__init__( self )

class DockerResourceCache( DockerObjectCache ):
	def __init__(self, client = None):
		super().__init__( self )

class DockerVolumeCache( DockerObjectCache ):
	def __init__(self, client = None):
		super().__init__( self )







## Docker Cache object, data container
class DockerCache:

	def __init__(self, *args, **kwargs ):
		self.__client__ = None
		self.__manager__ = None
		self.__run__ = True
		self.__dirty__ = True
		self.__objects__ = {}

		if 'client' in kwargs: self.__client__ = kwargs['client']

		if 'types' in kwargs and type( kwargs['types'] ) is list ):
			for s in kwargs['types']:
				self.__objects__[ s ] = None

		if 'types' in kwargs and type( kwargs['types'] ) is str ):
			self.__objects__[ kwargs['types'] ] = None

		else:
			for s in SUPPORTED_CACHE_TYPES:
				self.__objects__[ s ] = None


	def __refresh_images__( self ):
		pass

	def __refresh_containers__( self ):
		pass

	def __refresh_volumes__( self ):
		pass

	def __refresh_network__( self ):
		pass

	def object_by_id( self, id ): ## if ANY id can not be found, set all types to dirty!
		pass

	def refresh( self, what = 'all' ):

		if what == 'all':
			what = SUPPORTED_CACHE_TYPES

		elif type( what ) is str:
			what = [what]



class DockerCacheSingelton( object ):
	__instance = None

	def __new__( self, *args, **kwargs ):
		if not self.__instance:
			print("Started singleton...")
			self.__instance = super( DockerCache, self ).__new__( self )

		return self.__instance



	def instance( self ):
		return __instance





if __name__ == "__main__":
	sys.exit()
