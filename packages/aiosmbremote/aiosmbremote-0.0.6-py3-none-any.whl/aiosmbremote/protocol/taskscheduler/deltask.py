import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDDelTask(CMD):
	def __init__(self, token, cid, name):
		self.type = CMDType.DELETE_TASK
		self.token = token
		self.cid = cid
		self.name = name
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		cmd = CMDDelTask(d['token'],d['cid'], d['name'])
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDDelTask.from_dict(json.loads(jd))