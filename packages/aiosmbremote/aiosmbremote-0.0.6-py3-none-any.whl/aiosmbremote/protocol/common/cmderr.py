import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDErr(CMD):
	def __init__(self, token, reason, extra = ''):
		self.type = CMDType.ERR
		self.token = token
		self.reason = reason
		self.extra = extra
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		cmd = CMDErr(d['token'],d['reason'], d['extra'])
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDErr.from_dict(json.loads(jd))