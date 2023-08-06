import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDStartService(CMD):
	def __init__(self, token, cid, name):
		self.type = CMDType.START_SERVICE
		self.token = token
		self.cid = cid
		self.name = name
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		cmd = CMDStartService(d['token'],d['cid'],d['name'])
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDStartService.from_dict(json.loads(jd))