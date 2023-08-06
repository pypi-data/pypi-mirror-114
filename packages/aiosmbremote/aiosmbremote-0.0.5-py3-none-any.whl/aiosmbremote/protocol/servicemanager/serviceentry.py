import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDServiceEntry(CMD):
	def __init__(self, token, cid, name, display_name, status):
		self.type = CMDType.SERVICE_ENTRY
		self.token = token
		self.cid = cid
		self.name = name
		self.display_name = display_name
		self.status = status
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		cmd = CMDServiceEntry(d['token'],d['cid'],d['name'],d['display_name'],d['status'])
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDServiceEntry.from_dict(json.loads(jd))