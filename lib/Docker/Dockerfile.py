from docker import Client, tls
from io import BytesIO
from os import path
import json

from datetime import datetime, date, time


PKGMGR_MAP = {
	'alphine':{
		'os':['alphine'],
		'yes':"",
		'cmd':{
			'install':"apk install",
			'upgrade':"pkg update && apk upgrade"
		}
	},
	'apt-get':{
		'os':['ubuntu','debian','hypriot/rpi-.*'],
		'yes':"-y",
		'cmd': {
			'install':'apt-get install',
			'upgrade':'apt-get update && apt-get upgrade'
		}
	},
	'yum': {
		'os':['centos','redhat'],
		'yes':"-y",
		'cmd': {
			'install':'yum install',
			'upgrade':'yum update'
		}
	}
}





################################################################
## Base class
################################################################
class DockerfileBase:
	def __init__( self, initial = [], comment = None ):
		if type( initial ) is str: initial = [initial]
		self._type='base'
		self._content = []

		if comment:
			self._content.append( { 'comment':comment} )

		self._content += initial



	def add( self, cont, comment = None ):
		if comment:
			self._content.append( { 'comment':comment } )
		self._content.append( { 'content':content } )


	def as_array( self, with_comments = True ):
		return self._content

	def as_string( self ):
		return "\n".join( self.as_array() )

	def get_type( self ):
		return type( self )

	def get_content( self ):
		return self._content

	def get_length( self ):
		return len( self._commands )


################################################################
class DockerfileRun( DockerfileBase ):
	def __init__( self, initial = [], comment = None ):
		DockerfileBase.__init__( self, initial, comment )
		self._type = 'command'


	def as_array( self, with_comments = True ):
		res = []

		for line in self._content:
			if 'comment' in line and line['comment'] and with_comments: res.append( "# %(com)s" % { 'com': line['comment'] } )
			elif 'content' in line and line['content'] :  res.append( "RUN %(cmd)s" % {'cmd': line['content'] } )
			else: res.append( "RUN %(cmd)s" % {'cmd': line } )

		return res




################################################################
class DockerfileVolume( DockerfileBase ):
	def __init__( self, initial = [], comment = None ):
		DockerfileBase.__init__( self, initial, comment )
		self._type = 'volume'



	def as_array( self, with_comments = True ):
		res = []

		for line in self._content:
			if 'comment' in line and line['comment'] and with_comments: res.append( "# %(com)s" % { 'com': line['comment'] } )
			elif 'content' in line and line['content'] :  res.append( "VOLUME %(vol)s" % {'vol': line['content'] } )
			else: res.append( "VOLUME %(vol)s" % {'vol': line } )

		return res



################################################################
class DockerfilePort( DockerfileBase ):
	def __init__( self, initial = [], comment = None ):
		DockerfileBase.__init__( self, initial, comment )
		self._type = 'ports'


	def as_array( self, with_comments = True ):
		res = []

		for line in self._content:
			if 'comment' in line and line['comment'] and with_comments: res.append( "# %(com)s" % { 'com': line['comment'] } )
			elif 'content' in line and line['content'] :  res.append( "EXPOSE %(prt)s" % {'prt': line['content'] } )
			else: res.append( "EXPOSE %(prt)s" % {'prt': line } )

		return res


################################################################
class DockerfileEnv( DockerfileBase ):
	def __init__( self, initial = [], comment = None ):
		DockerfileBase.__init__( self, initial, comment )
		self._type = 'env'



	def as_array( self, with_comments = True ):
		res = []

		for line in self._content:
			if 'comment' in line and line['comment'] and with_comments: res.append( "# %(com)s" % { 'com': line['comment'] } )
			elif 'content' in line and line['content'] :  res.append( "ENV %(env)s" % {'env': line['content'] } )
			else: res.append( "ENV %(env)s" % {'env': line } )

		return res



################################################################
class DockerfileCopy( DockerfileBase ):
	def __init__( self, initial = [], comment = None ):
		DockerfileBase.__init__( self, initial, comment )
		self._type = 'copy'


	def as_array( self, with_comments = True ):
		res = []

		for line in self._content:
			if 'comment' in line and line['comment'] and with_comments: res.append( "# %(com)s" % { 'com': line['comment'] } )
			elif 'content' in line and line['content'] :  res.append( "COPY %(cpy)s" % {'cpy': line['content'] } )
			else: res.append( "COPY %(cpy)s" % {'cpy': line } )

		return res



################################################################
class DockerfileAdd( DockerfileBase ):
	def __init__( self, initial = [], comment = None ):
		DockerfileBase.__init__( self, initial, comment )
		self._type = 'add'



	def as_array( self, with_comments = True ):
		res = []

		for line in self._content:
			if 'comment' in line and line['comment'] and with_comments: res.append( "# %(com)s" % { 'com': line['comment'] } )
			elif 'content' in line and line['content'] :  res.append( "ADD %(cpy)s" % {'add': line['content'] } )
			else: res.append( "ADD %(cpy)s" % {'add': line } )

		return res




################################################################
class Dockerfile:

	def __init__( self, **options ):
		self._debug = False
		self._docker_file = None
		self._config_file = None
		self._image_name  = None
		self._cmd = "/bin/sh" ## if the type is a list, add as list, else string

		self._maintainer = "None"
		self._image_source = None
		self._image_base = None
		self._image_version = "latest"
		self._image_tag = None
		self._image_user = 'root'

		self._image_auto_upgrade = True

		self._content = []

		if 'debug' in options: self._debug = True
		if 'docker_file' in options: self._docker_file = options['docker_file']
		if 'config_file' in options: self._config_file = options['config_file']
		if 'name' in options: self._image_name = options['name']
		if 'maintainer' in options: self._maintainer = options['maintainer']
		if 'tag' in options: self._image_tag = options['tag']
		if 'base' in options: self._image_base = options['base']
		if 'source' in options: self._image_source = options['source']
		if 'version' in options: self._image_version = options['version']
		if 'cmd' in options: self._cmd = options['cmd']
		if 'upgrade' in options: self._auto_upgrade = options['upgrade']
		if 'user' in options: self._image_user = options['user']


	def get_tag( self ): return self._image_tag
	def get_name( self ): return self._image_name

	def add_content( self, data_class ):
		self._content.append( data_class )

	def add_newline( self, num = 1 ):
		## Each new line will be doubled in to_string due to the join oprtation!!
		for n in range( 0, num ):
			self._content.append( "\n" )

	def add_cmd( self, cmd ):
		self._cmd = cmd

	def add_user( self, user = 'root' ):
		self._image_user = user

	def add_tag( self, tag ):
		self._image_tag = tag

	def add_name( self, name ):
		self._image_name = name

	def as_array( self, with_comments = True ):
		res = []

		res.append( "FROM %(from)s:%(version)s" % {'from': self._image_source, 'version': self._image_version } )
		res.append( "MAINTAINER %(maint)s" % {'maint': self._maintainer } )
		res.append( "USER %(user)s" % {'user': self._image_user } )


		for cnt in self._content:
			if type( cnt ) is str:
				res.append( cnt )

			else: res.extend(
				cnt.as_array( with_comments ) )


		if type( self._cmd ) is list:
			res.append( "CMD [ %(cmd)s ]" % {'cmd': "\""+"\",\"".join( self._cmd ) + "\"" } )
		elif type( self._cmd ) is str:
			res.append( "CMD [ \"%(cmd)s\" ]" % {'cmd': self._cmd } )
		else:
			print("WARN: CMD was not set, unknown type: %(cmd)s" % { 'cmd': type( self._cmd ) })

		return res

	def as_string( self , with_comments = True):
		return "\n".join( self.as_array( with_comments ) )

	def auto_upgrade( self, val = None ):
		if val and type( val ) is bool:
			self._image_auto_upgrade = val

		return self._image_auto_upgrade


	def supported_pkgmgr( self, inbase = None ):

		base = self._image_base
		if inbase: base = inbase

		res = None
		for k in PKGMGR_MAP:
			if base in PKGMGR_MAP[k]["os"]:
				return k

		return res

	def build_from_config( config, **options ):

		cmd=["/bin/sh"]

		if 'maintainer' not in config: raise RuntimeError("No maintainer")
		if 'base' not in config: raise RuntimeError("Missing container base")
		if 'source' not in config: raise RuntimeError("Missing container source")


		df = Dockerfile( maintainer=config['maintainer'], source=config['source'], base=config['base'] )
		if 'name' in config: df.add_name( config['name'] )
		if 'tag' in config:  df.add_tag( config['tag'] )
		if 'cmd' in config:  df.add_cmd( config['cmd'] )
		if 'user' in config: df.add_user( config['user'] )

		curr_time_dt = datetime.utcnow().strftime('%s')
		curr_time_str = datetime.utcnow()
		release_str = "%(key)s %(val)s" % { 'key': 'CREATED_TIME', 'val': curr_time_str }
		df.add_content( DockerfileEnv( release_str ) )


		pkgmgr = df.supported_pkgmgr( )
		pkg_cfg = PKGMGR_MAP[pkgmgr]

		if 'product' in config:
			product_str = "%(key)s %(val)s" % { 'key': 'PRODUCT', 'val':config['product'] }
			df.add_content( DockerfileEnv( product_str ) )

		if 'env' in config:
			envlist = []
			for e in config['env']:
				envlist.append( "%(k)s %(v)s" % { 'k': e, 'v': config['env'][e] } )
			df.add_content( DockerfileEnv( envlist ) )


		if df.auto_upgrade() or config['upgrade'] == True:
			if 'upgrade' in config and pkgmgr != None:
				update_str = "%(cmd)s %(yes)s" % { 'cmd': pkg_cfg[ 'cmd' ]['upgrade'], 'yes': pkg_cfg[ 'yes' ] }
				df.add_content( DockerfileRun( update_str ) )

		if 'tasks' in config:
			for tsk in config['tasks']:

				comment = None
				if 'comment' in tsk:
					comment = tsk['comment']

#				run, install, copy, add, volume
				if 'install' in tsk and len( tsk['install'] ) > 0:
					install_str = "%(cmd)s %(yes)s %(packages)s" % { 'cmd': pkg_cfg[ 'cmd' ]['install'], 'yes': pkg_cfg['yes'], 'packages': " ".join( tsk['install'] ) }
					df.add_content( DockerfileRun( install_str, comment ) )


				if 'run' in tsk:
					df.add_content( DockerfileRun( tsk['run'], comment ) )

				if 'copy' in tsk:
					df.add_content( DockerfileCopy( tsk['copy'], comment ) )

				if 'add' in tsk:
					df.add_content( DockerfileAdd( tsk['add'], comment ) )

				if 'volume' in tsk:
					df.add_content( DockerfileVolume( tsk['volume'], comment ) )

				if 'env' in tsk:
					df.add_content( DockerfileEnv( tsk['env'], comment ) )


		if 'ports' in config:
			portlist = []

			if len( config['ports'] ) > 0:
	 			portlist.append( "%(pl)s" % { 'pl': " ".join( config['ports'] ) } )

			df.add_content( DockerfilePort( portlist ) )

		return df
