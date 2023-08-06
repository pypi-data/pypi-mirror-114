import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDFileData(CMD):
	def __init__(self, cid, token, data, offset, size):
		self.type = CMDType.FILE_DATA
		self.cid = cid
		self.token = token
		self.size = int(size)
		self.offset = int(offset)
		self.data = data
	
	@staticmethod
	def from_data(hdr, data):
		return CMDFileData(hdr['cid'], hdr['token'], data, hdr['offset'], hdr['size'])


	def get_bytes(self):
		hj = json.dumps({'cid' : self.cid, 'token': self.token, 'type': self.type.value, 'offset': self.offset, 'size': self.size}).encode()
		payload = len(hj).to_bytes(4, byteorder='big', signed=False) 
		payload += hj
		payload += self.data
		return payload
