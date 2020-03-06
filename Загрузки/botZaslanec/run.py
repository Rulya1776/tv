# -*- coding: utf-8 -*-

t = '*****************************************************'
x = '* (C) 2015 - 2018 Aleksey S.Galickiy for ProxyTV RU *'
t = '*****************************************************'

import iplib, socket, threading, struct, time

class scanUDP():
	def __init__(self, addr, port):

		self.uHOST = addr
		self.uPORT = port
		self.do_UDP()

	def do_UDP(self):
		plistM3U = ''
		count = 0
		block = 1316
		plistM3U = '#EXTM3U tvg-autor="https://www.youtube.com/channel/UCQGGNWAIMrlmfMZN-oO3fPQ"\n'
		ip = iplib.IPv4Address(self.uHOST)
		for i in range(255):
			host = str(ip + i)
			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
				sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
				sock.bind(('', self.uPORT))
				mreq = struct.pack('=4sl', socket.inet_aton(host), socket.INADDR_ANY)
				sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)	
				data = sock.recv(block)	
				if len(data) == block:
					count += 1
					plistM3U += '#EXTINF: -1,channel #%s\n'%count
					plistM3U += 'udp://@%s:%s\n'%(host, self.uPORT)
					print '%s -yes'%host
				else:
					print '%s -no'%host
			except:
				print '%s -no'%host
			data = 0
		fileM3U = open('plist.m3u', 'w')
		fileM3U.write(plistM3U)
		fileM3U.close	
		print "Found channels:", str(count)
		print "Playlist saved to file: %s.m3u"%self.uHOST
		time.sleep(3)

def startScaner():
	try:
		print '%s\n%s\n%s\n'%(t, x, t)
		udport = raw_input("Input addr:port >>> ")
		up = udport.split('.')  
		ip  = up[3].split(':')
		ip1 = int(up[0])
		if ip1 > 255 or ip1 < 0: ip1 = int('a')
		ip2 = int(up[1])
		if ip2 > 255 or ip2 < 0: ip2 = int('a')
		ip3 = int(up[2])
		if ip3 > 255 or ip3 < 0: ip3 = int('a')
		ip4 = int(ip[0])
		if ip4 > 255 or ip4 < 0: ip4 = int('a')
		port = int(ip[1])
		if port > 65535 or port < 0: port = int('a')
		addr = '%s.%s.%s.0'%(ip1, ip2, ip3)

	except:
		udport = ''

	finally:
		if udport != '':
			try:
				delay = float(raw_input("Input delay, mS >>> ")) / 1000
				
			except:
				delay = 0
				
			finally:
				if delay == 0: delay = 0.33
				socket.setdefaulttimeout(delay)
				scanUDP(addr, port)
		else:
			print 'Invalid ADDR or PORT!'
		print
		print "Bye, bye people."
		time.sleep(3)
	
startScaner()
