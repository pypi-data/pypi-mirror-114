import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDLsassSecret(CMD):
	def __init__(self, token, cid, result_txt, result_grep, result_json):
		self.type = CMDType.LSASSSECRET
		self.token = token
		self.cid = cid
		self.result_txt = result_txt
		self.result_grep = result_grep
		self.result_json = result_json
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		cmd = CMDLsassSecret(d['token'],d['cid'],d['result_txt'],d['result_grep'],d['result_json'])
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDLsassSecret.from_dict(json.loads(jd))