import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDCreateEntry(CMD):
	def __init__(self, token, cid, path, is_file):
		self.type = CMDType.CREATE_ENTRY
		self.token = token
		self.cid = cid
		self.path = path
		self.is_file = is_file
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		cmd = CMDCreateEntry(d['token'],d['cid'], d['path'], d['is_file'])
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDCreateEntry.from_dict(json.loads(jd))