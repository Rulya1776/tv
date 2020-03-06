# -*- coding: utf-8 -*-

import pdb
import settings as sett
from datetime import datetime 
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

HOST = 'localhost'
PORT =  12067
ADDR = (HOST, PORT)

class IPTVserver(BaseHTTPRequestHandler):
	def send_response(self, code, message = None):
		self.log_request(code) 
		self.wfile.write('%s %d %s\r\n' % (self.protocol_version, code, message))
		self.wfile.flush()

	def do_HEAD(self, contype):
		self.send_response(200, 'ok')
		self.send_header('Server', sett.nserver)
		self.send_header('Content-Type', contype)
		self.send_header('Date', self.date_time_string())
		self.end_headers()

	def do_GET(self):
		self.send_page(sett.nserver)

	def send_page(self,title): 
		if title == sett.nserver:
			version = 'v%s' % sett.version
		else:
			version = ''
		page = ( 
		'''<html>
				<head>
					<title>%s</title>
					<meta http-equiv = "Content-Type" content = "%s">
				</head>
				<body style="background-repeat: no-repeat;" background = "https://cdn.pixabay.com/photo/2019/02/19/19/45/thumbs-up-4007573_960_720.png">
					<i><h1 style="padding-left: 20px">%s<sup><small> %s</small></sup></h1>
					<hr width = "300" align = "left"></hr>
					<div style="padding-left: 20px">%s</div></i>
				</body>
			</html>''') % (title, sett.context,title, version, sett.copyrid)
		self.do_HEAD(sett.context)
		self.wfile.write(page)
		self.wfile.flush()
		
class homeIPTVserver():
	def start(self, addr):
		today = datetime.today().strftime('%d %B %Y in %H:%M')
		print '**** %s %s ****\nstart %s' % (sett.nserver, sett.version, today) 
		try:
			iptv = HTTPServer(addr, IPTVserver)
			iptv.serve_forever()
		except KeyboardInterrupt:
			iptv.socket.close()
			
homeIPTVserver().start(ADDR)
_
