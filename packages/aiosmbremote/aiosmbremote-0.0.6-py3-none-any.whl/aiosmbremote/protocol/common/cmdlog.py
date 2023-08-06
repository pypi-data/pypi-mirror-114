import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDLog(CMD):
	def __init__(self, token, level, msg):
		self.type = CMDType.LOG
		self.token = token
		self.level = level
		self.msg = msg
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		cmd = CMDLog(d['token'],d['level'], d['msg'])
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDLog.from_dict(json.loads(jd))