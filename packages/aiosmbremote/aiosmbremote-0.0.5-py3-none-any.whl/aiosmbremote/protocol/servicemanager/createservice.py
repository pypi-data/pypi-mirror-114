import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDCreateService(CMD):
	def __init__(self, token, cid, name, display_name, command):
		self.type = CMDType.CREATE_SERVICE
		self.token = token
		self.cid = cid
		self.name = name
		self.display_name = display_name
		self.command = command
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		cmd = CMDCreateService(d['token'],d['cid'],d['name'],d['display_name'],d['command'])
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDCreateService.from_dict(json.loads(jd))