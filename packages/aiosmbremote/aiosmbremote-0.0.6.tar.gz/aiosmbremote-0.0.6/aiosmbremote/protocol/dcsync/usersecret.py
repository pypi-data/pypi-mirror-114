import json

from aiosmbremote.utils.encoder import UniversalEncoder
from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol import CMD

class CMDUserSecret(CMD):
	def __init__(self, cid, token):
		self.type = CMDType.USERSECRET
		self.cid = cid
		self.token = token
		self.domain = None

		self.nt_hash = None
		self.lm_hash = None
		
		self.object_sid = None
		self.pwd_last_set = None
		self.user_account_status = None
		
		self.lm_history = []
		self.nt_history = []
		self.kerberos_keys = []
		self.cleartext_pwds = []
	
	def to_dict(self):
		return self.__dict__
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls = UniversalEncoder)
	
	@staticmethod
	def from_dict(d):
		raise NotImplementedError()

	@staticmethod
	def from_smbuserecret(cid, token, su):
		us = CMDUserSecret(cid, token)
		dd = su.to_dict()
		us.domain = dd['domain']
		us.nt_hash = dd['nt_hash']
		us.lm_hash = dd['lm_hash']
		us.object_sid = dd['object_sid']
		us.pwd_last_set = dd['pwd_last_set']
		us.user_account_status = dd['user_account_status']
		us.lm_history = dd['lm_history']
		us.nt_history = dd['nt_history']
		us.kerberos_keys = dd['kerberos_keys']
		us.cleartext_pwds = dd['cleartext_pwds']

		return us

	@staticmethod
	def from_json(jd):
		return CMDUserSecret.from_dict(json.loads(jd))