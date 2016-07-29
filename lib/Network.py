from docker import Client, tls
from io import BytesIO
from os import path
import json

from datetime import datetime, date, time

'''
 --aux-address=map[]      auxiliary ipv4 or ipv6 addresses used by Network driver
  -d, --driver=bridge      Driver to manage the Network
  --gateway=[]             ipv4 or ipv6 Gateway for the master subnet
  --help=false             Print usage
  --ip-range=[]            allocate container ip from a sub-range
  --ipam-driver=default    IP Address Management Driver
  -o, --opt=map[]          set driver specific options
  --subnet=[]              subnet in CIDR format that represents a network segment
'''


SUPPORTED_OPTIONS=['gateway','ip-range','ipam-driver','subnet','driver-opt' ]

class DockerNetwork:

	def __init__( self ):
		pass



  def create_network( name, driver, **options ):
    pass


if __name__ == "__main__":
	sys.exit()