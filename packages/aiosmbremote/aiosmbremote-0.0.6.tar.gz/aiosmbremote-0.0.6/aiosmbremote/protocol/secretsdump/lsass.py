import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDGetSecretLsass(CMD):
	def __init__(self, token, cid, method):
		self.type = CMDType.GET_SECRET_LSASS
		self.token = token
		self.cid = cid
		self.method = method
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		cmd = CMDGetSecretLsass(d['token'],d['cid'],d['method'])
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDGetSecretLsass.from_dict(json.loads(jd))