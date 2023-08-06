import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDTaskCmdExec(CMD):
	def __init__(self, token, cid, command):
		self.type = CMDType.TASKCMDEXEC
		self.token = token
		self.cid = cid
		self.command = command
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		cmd = CMDTaskCmdExec(d['token'],d['cid'], d['command'])
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDTaskCmdExec.from_dict(json.loads(jd))