import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDFSEntrySD(CMD):
	def __init__(self, token, cid, path, sd, sddata):
		self.type = CMDType.FSENTRY_SD
		self.token = token
		self.cid = cid
		self.path = path
		self.sddata = sddata
		self.sd = sd
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)				
	
	@staticmethod
	def from_dict(d):
		cmd = CMDFSEntrySD(
			d['token'],
			d['cid'],
			d['path'],
			d['sd'],
			d['sddata']
		)
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDFSEntrySD.from_dict(json.loads(jd))