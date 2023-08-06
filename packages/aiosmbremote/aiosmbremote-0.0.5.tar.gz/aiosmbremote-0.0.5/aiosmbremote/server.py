import websockets
import asyncio
from http import HTTPStatus
import os

from aiosmbremote import logger
from aiosmbremote.clienthandler import ClientHandler

MIME_TYPES = {
	"html": "text/html",
	"js": "text/javascript",
	"css": "text/css"
}


class Server:
	def __init__(self, listen_ip = '127.0.0.1', listen_port = 8765, ssl_ctx = None, http_root = None):
		self.listen_ip = listen_ip
		self.listen_port = listen_port
		self.ssl_ctx = ssl_ctx
		self.http_root = http_root
		self.wsserver = None
		self.clients = {}

	async def http_layer(self, path, request_headers):
		try:
			if "Upgrade" in request_headers:
				return  # Probably a WebSocket connection

			if path == '/':
				path = '/index.html'
			
			response_headers = [
				('Server', 'asyncio websocket server'),
				('Connection', 'close'),
			]

			# Derive full system path
			# pretty sure here is path traversal
			full_path = os.path.realpath(os.path.join(self.http_root, path[1:]))

			# Validate the path
			if os.path.commonpath((self.http_root, full_path)) != self.http_root or \
					not os.path.exists(full_path) or not os.path.isfile(full_path):
				logger.info("HTTP GET {} 404 NOT FOUND".format(path))
				return HTTPStatus.NOT_FOUND, [], b'404 NOT FOUND'

			# Guess file content type
			extension = full_path.split(".")[-1]
			mime_type = MIME_TYPES.get(extension, "application/octet-stream")
			response_headers.append(('Content-Type', mime_type))

			# Read the whole file into memory and send it out
			body = open(full_path, 'rb').read()
			response_headers.append(('Content-Length', str(len(body))))
			logger.info("HTTP GET {} 200 OK".format(path))
			return HTTPStatus.OK, response_headers, body


		except Exception as e:
			logger.exception('http_layer')
			return HTTPStatus.INTERNAL_SERVER_ERROR, response_headers, ''

	async def handle_client(self, ws, path):
		remote_ip, remote_port = ws.remote_address
		logger.debug('Client connected from %s:%d' % (remote_ip, remote_port))
		client = ClientHandler(ws)
		self.clients[client] = 1
		await client.run()
		await client.terminate()
	

	async def run(self):
		self.wsserver = await websockets.serve(self.handle_client, self.listen_ip, self.listen_port, ssl=self.ssl_ctx, process_request=self.http_layer)
		await self.wsserver.wait_closed()

