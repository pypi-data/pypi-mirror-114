import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDFSEntry(CMD):
	def __init__(self, token, cid, is_file, name, size, creation_time, last_access_time, last_write_time, change_time, allocation_size, attributes):
		self.type = CMDType.FSENTRY
		self.token = token
		self.cid = cid

		self.is_file = is_file
		self.name = name
		self.size = size
		self.creation_time = creation_time
		self.last_access_time = last_access_time
		self.last_write_time = last_write_time
		self.change_time = change_time
		self.allocation_size = allocation_size
		self.attributes = attributes
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)

	@staticmethod
	def from_smbfile(token, cid, is_file, smbentry):
		return CMDFSEntry(
			token,
			cid,
			is_file,
			smbentry.name,
			smbentry.size if is_file is True else 0,
			smbentry.creation_time,
			smbentry.last_access_time,
			smbentry.last_write_time,
			smbentry.change_time,
			smbentry.allocation_size,
			smbentry.attributes,
		)					
	
	@staticmethod
	def from_dict(d):
		cmd = CMDFSEntry(
			d['token'],
			d['cid'],
			d['is_file'],
			d['name'], 
			d['size'], 
			d['creation_time'], 
			d['last_access_time'], 
			d['last_write_time'], 
			d['change_time'], 
			d['allocation_size'], 
			d['attributes'],	
		)
		return cmd

	@staticmethod
	def from_json(jd):
		return CMDFSEntry.from_dict(json.loads(jd))