import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDShare(CMD):
	def __init__(self, token, cid, sharename):
		self.type = CMDType.SHARE
		self.token = token
		self.cid = cid
		self.sharename = sharename
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		cmd = CMDShare(d['token'],d['cid'], d['sharename'])
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDShare.from_dict(json.loads(jd))