import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDGetFSEntrySD(CMD):
	def __init__(self, token, cid, is_file, path):
		self.type = CMDType.GET_FSENTRY_SD
		self.token = token
		self.cid = cid
		self.is_file = is_file
		self.path = path
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)				
	
	@staticmethod
	def from_dict(d):
		cmd = CMDGetFSEntrySD(
			d['token'],
			d['cid'],
			d['is_file'],
			d['path'],	
		)
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDGetFSEntrySD.from_dict(json.loads(jd))