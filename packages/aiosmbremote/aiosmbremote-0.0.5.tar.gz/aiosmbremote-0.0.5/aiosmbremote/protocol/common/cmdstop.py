import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDStop(CMD):
	def __init__(self, token):
		self.type = CMDType.STOP
		self.token = token
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		cmd = CMDStop(d['token'])
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDStop.from_dict(json.loads(jd))