import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDCreateTask(CMD):
	def __init__(self, token, cid, xmldata):
		self.type = CMDType.CREATE_TASK
		self.token = token
		self.cid = cid
		self.xmldata = xmldata
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		cmd = CMDCreateTask(d['token'],d['cid'], d['xmldata'])
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDCreateTask.from_dict(json.loads(jd))