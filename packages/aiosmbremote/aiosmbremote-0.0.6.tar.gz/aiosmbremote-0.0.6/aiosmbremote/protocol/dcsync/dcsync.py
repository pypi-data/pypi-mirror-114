import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDDcsync(CMD):
	def __init__(self, cid, token, username = None):
		self.type = CMDType.DCSYNC
		self.cid = cid
		self.token = token
		self.username = username
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		cmd = CMDDcsync(d['cid'], d['token'], d.get('username'))
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDDcsync.from_dict(json.loads(jd))