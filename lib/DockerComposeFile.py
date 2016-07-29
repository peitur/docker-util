import sys, os, json, re
from pprint import pprint
sys.path.append( "../lib" )

#from docker import Client, tls, utils
import docker
import threading, queue
from io import BytesIO

class DockerComposeFile:

    def __init__( self, **options ):
        pass

    
