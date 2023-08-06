import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDInterfaceEntry(CMD):
	def __init__(self, token, cid, ifindex, ifname):
		self.type = CMDType.INTERFACE_ENTRY
		self.token = token
		self.cid = cid
		self.ifindex = ifindex
		self.ifname = ifname
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		cmd = CMDInterfaceEntry(d['token'],d['cid'], d['ifindex'], d['ifname'])
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDInterfaceEntry.from_dict(json.loads(jd))