import os
import asyncio
import traceback

import websockets
from aiosmbremote.protocol import *


async def client(server_url, smb_url):
	try:
		cid = None
		async with websockets.connect(server_url) as websocket:
			token = os.urandom(2).hex()
			cmd = CMDConnect(token, smb_url)
			print(1)
			await websocket.send(cmd.to_bytes())

			while True:
				res = await websocket.recv()
				reply = CMD.from_bytes(res)
				if reply.type == CMDType.CONNECTION:
					print('Connect OK! ID: %s' % reply.cid)
					cid = reply.cid
				elif reply.type == CMDType.OK:
					break
				
			token = os.urandom(2).hex()
			cmd = CMDListShares(token, cid)
			await websocket.send(cmd.to_bytes())
			
			while True:
				res = await websocket.recv()
				reply = CMD.from_bytes(res)
				if reply.type == CMDType.SHARE:
					print('Found share! Name: %s' % reply.sharename)
				elif reply.type == CMDType.OK:
					break


			token = os.urandom(2).hex()
			cmd = CMDListDirectory(token, cid, 'Users\\')
			await websocket.send(cmd.to_bytes())
			
			while True:
				res = await websocket.recv()
				reply = CMD.from_bytes(res)
				if reply.type == CMDType.FSENTRY:
					print('Found entry! Name: %s' % reply.name)
				elif reply.type == CMDType.OK:
					break


			token = os.urandom(2).hex()
			cmd = CMDListDirectory(token, cid, 'Users\\Default')
			await websocket.send(cmd.to_bytes())
			
			while True:
				res = await websocket.recv()
				reply = CMD.from_bytes(res)
				if reply.type == CMDType.FSENTRY:
					print('Found entry! Name: %s' % reply.name)
				elif reply.type == CMDType.OK:
					break
			
			print('======= FETCHING FILE =======')
			token = os.urandom(2).hex()
			cmd = CMDGetFileData(token, cid, 'Users\\Default\\NTUSER.DAT')
			await websocket.send(cmd.to_bytes())
			
			while True:
				res = await websocket.recv()
				reply = CMD.from_bytes(res)
				print(res[:0x200])
				if reply.type == CMDType.FILE_DATA:
					print('got file data!')
					#print('File data recieved! %s' % reply.data)
				elif reply.type == CMDType.OK:
					break

			print('======= CREATING FOLDER =======')
			token = os.urandom(2).hex()
			cmd = CMDCreateEntry(token, cid, 'Users\\Default\\testfolder', False)
			await websocket.send(cmd.to_bytes())
			data = await websocket.recv()
			reply = CMD.from_bytes(data)
			if reply.type != CMDType.OK:
				raise Exception('Error happened! %s' % data)


			print('======= PUTTING FILE =======')
			token = os.urandom(2).hex()
			cmd = CMDCreateEntry(token, cid, 'Users\\Default\\AD2.db', True)
			await websocket.send(cmd.to_bytes())
			data = await websocket.recv()
			reply = CMD.from_bytes(data)
			if reply.type != CMDType.CONTINUE:
				raise Exception('Error happened! %s' % data)
			
			with open('/home/devel/Desktop/AD2.db' , 'rb') as f:
				offset = 0
				while True:
					fdata = f.read(4096)
					if len(fdata) == 0:
						cmd = CMDOK(token)
						await websocket.send(cmd.to_bytes())
						data = await websocket.recv()
						reply = CMD.from_bytes(data)
						if reply.type != CMDType.OK:
							raise Exception('Error: Expected OK, %s found!' % reply.type)
						print('File sent!')
						break

					cmd = CMDFileData(cid, token, fdata, offset)
					offset += len(fdata)
					await websocket.send(cmd.to_bytes())
					data = await websocket.recv()
					reply = CMD.from_bytes(data)
					if reply.type != CMDType.CONTINUE:
						raise Exception('Error happened! %s' % data)

			
	except Exception as e:
		traceback.print_exc()
		print(e)

def main():
	import argparse
	parser = argparse.ArgumentParser(description='Test client')
	parser.add_argument('url', default = 'ws://127.0.0.1:8765', help='server url')
	parser.add_argument('smburl', default = 'smb2+ntlm-password://TEST\\victim:Passw0rd!1@10.10.10.2', help='SMB URL')

	args = parser.parse_args()

	asyncio.run(client(args.url, args.smburl))

if __name__ == '__main__':
	main()