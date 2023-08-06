import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDConnection(CMD):
	def __init__(self, token, cid):
		self.type = CMDType.CONNECTION
		self.token = token
		self.cid = cid
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		cmd = CMDConnection(d['token'],d['cid'])
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDConnection.from_dict(json.loads(jd))