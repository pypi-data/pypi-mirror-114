import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDWebConnect(CMD):
	def __init__(self, token, tad, tid, uad, uid):
		self.type = CMDType.WEBCONNECT
		self.token = token
		self.tad = tad
		self.tid = tid
		self.uad = uad
		self.uid = uid

	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		cmd = CMDWebConnect(d['token'], d['tad'], d['tid'], d['uad'], d['uid'])
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDWebConnect.from_dict(json.loads(jd))