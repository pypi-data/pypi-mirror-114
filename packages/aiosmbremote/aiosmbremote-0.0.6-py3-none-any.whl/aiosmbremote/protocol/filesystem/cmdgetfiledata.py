import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDGetFileData(CMD):
	def __init__(self, token, cid, path):
		self.type = CMDType.GET_FILE_DATA
		self.token = token
		self.cid = cid
		self.path = path
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		cmd = CMDGetFileData(d['token'],d['cid'], d['path'])
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDGetFileData.from_dict(json.loads(jd))