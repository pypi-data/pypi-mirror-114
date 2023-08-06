
import enum
import json



"""

 | length(4 bytes, unsinged, byteorder big) | data_type(BYTE) 0| DATA (length + 5)
 | length(4 bytes, unsinged, byteorder big) | data_type(BYTE) 1| JSON_HDR_LEN(4 bytes, unsinged, byteorder big) | JSON_HDR | DATA (length + JSON_HDR_LEN + 5)

length = total length of the "packet" including this length field
data_type = byte curtrently supported types are: JSON(0) BINARY(1)
DATA = variable size can be either JSON or raw binary data
"""

class CMD:
	def __init__(self):
		self.type = None

	def to_bytes(self):
		if self.type not in BINARY_TYPES:
			data = b'\x00' + self.to_json().encode()
		else:
			data = b'\x01'
			data += self.get_bytes()

		return (len(data)+4).to_bytes(4, byteorder = 'big', signed = False) + data

	def to_json(self):
		#needs to be implemented by the child class
		return None
	
	def get_bytes(self):
		#to be implemented by child if it's a binary one
		return None

	@staticmethod
	def from_bytes(data):
		length = int.from_bytes(data[:4], byteorder = 'big', signed = False)
		data_type = data[4]
		if data_type == 0:
			return CMD.from_json(data[5:length].decode())
		
		jlength = int.from_bytes(data[5:9], byteorder = 'big', signed = False)
		header = json.loads(data[9:9+jlength].decode())
		return type2cmd[CMDType(header['type'])].from_data(header, data[9+jlength:])

	@staticmethod
	def from_json(data_str):
		dd = json.loads(data_str)
		return type2cmd[CMDType(dd['type'])].from_dict(dd)


from aiosmbremote.protocol.cmdtypes import CMDType
from aiosmbremote.protocol.common.cmdok import CMDOK
from aiosmbremote.protocol.common.cmderr import CMDErr
from aiosmbremote.protocol.common.cmdlog import CMDLog
from aiosmbremote.protocol.common.cmdcontinue import CMDContinue
from aiosmbremote.protocol.common.cmdstop import CMDStop
from aiosmbremote.protocol.connection.cmdconnect import CMDConnect
from aiosmbremote.protocol.connection.cmdwebconnect import CMDWebConnect
from aiosmbremote.protocol.connection.cmddisconnect import CMDDisconnect
from aiosmbremote.protocol.connection.cmdconnection import CMDConnection
from aiosmbremote.protocol.filesystem.cmdlistshares import CMDListShares
from aiosmbremote.protocol.filesystem.cmdshare import CMDShare
from aiosmbremote.protocol.filesystem.cmdlistdirectory import CMDListDirectory
from aiosmbremote.protocol.filesystem.cmdfsentry import CMDFSEntry
from aiosmbremote.protocol.filesystem.cmdgetfiledata import CMDGetFileData
from aiosmbremote.protocol.filesystem.cmdfiledata import CMDFileData
from aiosmbremote.protocol.filesystem.cmdcreateentry import CMDCreateEntry
from aiosmbremote.protocol.filesystem.cmddelentry import CMDDelEntry
from aiosmbremote.protocol.dcsync.dcsync import CMDDcsync
from aiosmbremote.protocol.dcsync.usersecret import CMDUserSecret
from aiosmbremote.protocol.filesystem.fsentrysd import CMDFSEntrySD
from aiosmbremote.protocol.filesystem.cmdgetfsentrysd import CMDGetFSEntrySD
from aiosmbremote.protocol.taskscheduler.listtasks import CMDListTasks
from aiosmbremote.protocol.taskscheduler.taskentry import CMDTaskEntry
from aiosmbremote.protocol.taskscheduler.deltask import CMDDelTask
from aiosmbremote.protocol.taskscheduler.cmdexec import CMDTaskCmdExec
from aiosmbremote.protocol.taskscheduler.createtask import CMDCreateTask
from aiosmbremote.protocol.ioctl.listinterfaces import CMDListInterfaces
from aiosmbremote.protocol.ioctl.interfaceenty import CMDInterfaceEntry
from aiosmbremote.protocol.servicemanager.listservices import CMDListServices
from aiosmbremote.protocol.servicemanager.serviceentry import CMDServiceEntry
from aiosmbremote.protocol.servicemanager.createservice import CMDCreateService
from aiosmbremote.protocol.servicemanager.startservice import CMDStartService
from aiosmbremote.protocol.servicemanager.controlservice import CMDControlService
from aiosmbremote.protocol.secretsdump.registry import CMDSecretsdumpRegistry
from aiosmbremote.protocol.secretsdump.regsecret import CMDRegSecret
from aiosmbremote.protocol.secretsdump.lsasssecret import CMDLsassSecret
from aiosmbremote.protocol.secretsdump.lsass import CMDGetSecretLsass





__all__ = [
	'CMDType',
	'CMD',
	'CMDOK',
	'CMDErr',
	'CMDLog',
	'CMDConnect',
	'CMDConnection',
	'CMDListShares',
	'CMDShare',
	'CMDListDirectory',
	'CMDFSEntry',
	'CMDGetFileData',
	'CMDFileData',
	'CMDGetFileData',
	'CMDCreateEntry',
	'CMDDelEntry',
	'CMDContinue',
	'CMDDisconnect',
	'CMDDcsync',
	'CMDUserSecret',
	'CMDStop',
	'CMDGetFSEntrySD',
	'CMDFSEntrySD',
	'CMDListTasks',
	'CMDTaskEntry',
	'CMDDelTask',
	'CMDListInterfaces',
	'CMDInterfaceEntry',
	'CMDTaskCmdExec',
	'CMDCreateTask',
	'CMDWebConnect',
	'CMDListServices',
	'CMDServiceEntry',
	'CMDCreateService',
	'CMDStartService',
	'CMDControlService',
	'CMDSecretsdumpRegistry',
	'CMDRegSecret',
	'CMDLsassSecret',
	'CMDGetSecretLsass',

]

BINARY_TYPES = [
	CMDType.FILE_DATA,
]

type2cmd = {
	CMDType.OK : CMDOK,
	CMDType.ERR : CMDErr,
	CMDType.LOG : CMDLog,
	CMDType.CONNECT : CMDConnect,
	CMDType.CONNECTION : CMDConnection,
	CMDType.LIST_SHARES : CMDListShares,
	CMDType.SHARE : CMDShare,
	CMDType.LIST_DIRECTORY : CMDListDirectory,
	CMDType.FSENTRY : CMDFSEntry,
	CMDType.GET_FILE_DATA : CMDGetFileData,
	CMDType.FILE_DATA : CMDFileData,
	CMDType.GET_FSENTRY_SD : CMDGetFSEntrySD,
	CMDType.FSENTRY_SD : CMDFSEntrySD,
	CMDType.CREATE_ENTRY : CMDCreateEntry,
	CMDType.DELETE_ENTRY : CMDDelEntry,
	CMDType.CONTINUE : CMDContinue,
	CMDType.DISCONNECT : CMDDisconnect,
	CMDType.DCSYNC : CMDDcsync,
	CMDType.STOP : CMDStop,
	CMDType.LIST_TASKS : CMDListTasks,
	CMDType.TASK_ENTRY : CMDTaskEntry,
	CMDType.DELETE_TASK : CMDDelTask,
	CMDType.LIST_INTERFACES : CMDListInterfaces,
	CMDType.INTERFACE_ENTRY : CMDInterfaceEntry,
	CMDType.TASKCMDEXEC : CMDTaskCmdExec,
	CMDType.CREATE_TASK : CMDCreateTask,
	CMDType.WEBCONNECT : CMDWebConnect,
	CMDType.LIST_SERVICES : CMDListServices,
	CMDType.SERVICE_ENTRY : CMDServiceEntry,
	CMDType.CREATE_SERVICE : CMDCreateService,
	CMDType.START_SERVICE : CMDStartService,
	CMDType.CONTROL_SERVICE : CMDControlService,
	CMDType.GET_SECRET_REGISTRY : CMDSecretsdumpRegistry,
	CMDType.GET_SECRET_REGISTRY : CMDSecretsdumpRegistry,
	CMDType.LSASSSECRET : CMDLsassSecret,
	CMDType.GET_SECRET_LSASS : CMDGetSecretLsass,
}