import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDConnect(CMD):
	def __init__(self, token, url):
		self.type = CMDType.CONNECT
		self.token = token
		self.url = url
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		cmd = CMDConnect(d['token'],d['url'])
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDConnect.from_dict(json.loads(jd))