import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDControlService(CMD):
	def __init__(self, token, cid, name, status):
		self.type = CMDType.CONTROL_SERVICE
		self.token = token
		self.cid = cid
		self.name = name
		self.status = status
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		cmd = CMDControlService(d['token'],d['cid'],d['name'],d['status'])
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDControlService.from_dict(json.loads(jd))