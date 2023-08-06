import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDRegSecret(CMD):
	def __init__(self, token, cid, result):
		self.type = CMDType.REGSECRET
		self.token = token
		self.cid = cid
		self.result = result
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		cmd = CMDRegSecret(d['token'],d['cid'],d['result'])
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDRegSecret.from_dict(json.loads(jd))