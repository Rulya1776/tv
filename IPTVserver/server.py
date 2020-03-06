# -*- coding: utf-8 -*-

import time
import urllib
 
TIMEOUT = 3  
LENDATA = 8192
MAXATTEMPT = 5
NAMEFILE = 'plist.m3u'
CHLIST = 'chlist.csv'

urllib.socket.setdefaulttimeout(TIMEOUT)

def scrtxt(text):
	print text.decode('utf8') 
	time.sleep(TIMEOUT) 
   
def vrfSTREAM(stream, idchann): 
	attempt = 0
	unf = 'udpxy not found'
	while attempt < MAXATTEMPT: 
		try: 
			openstrm = urllib.urlopen(stream)
			readstrm = openstrm.read(LENDATA) 
		except:
			attempt += 1
			print 'ch #%s - NO connection' % idchann  
		else:
			if Len(readstrm) == LENDATA:
				print 'ch #%s - GOOD stream' % idchann
				return  stream  + '\n' 
			else: 
				attempt += 1
				print 'ch #%s - BAD stream' % idchann 
		if stream == unf: 
			print 'ch #%s - %s' (idchann, unf)
		try:
			connectp = urllib.urlopen('http://proxytv.ru/iptv/php/onechan.php?ip=%s&code=%s'%(udpaddr,'114151330912258064'))  
			stream = connectp.read()
		except:
			pass
	stream = 'http://proxytv.ru/iptv/img/notv.mp4\n' 
	return stream
	
def robotIPTV(idchann, namechann, namegroup,tvgid, tvgshift):
	attempt = 0
	while attempt < MAXATTEMPT:
		try:
			connectp = urllib.urlopen('http://proxytv.ru/iptv/php/ allchan.php?id=%s&code=%s'%(idchann,'114151330912258064')) 
			allstream = connectp.read()
			break
		except:
			attempt += 1 
	if attempt < MAXATTEMPT: 
		extm3u = '#EXTM3U\n' 
		m3ufile = open( NAMEFILE, 'w') 
		m3ufile.write(extm3u) 
			
		channel = namechann.split(',') 
		onestream = allstream.split(',') 
		oneid = idchann.split(',')  
		onegroup = namegroup.split(',')
		onetvgid = tvgid.split(',')
		onetvgshift = tvgshift.split(',')
		 
		for i in range(len(onestream)): 
			onetvglogo = channel[i] 
			extinf = ('#EXTINF:-1 tvg-id="%s" tvg-shift="%s" tvg-logo="%s.png" group-title="%s",%s\n' % 
			(onetvgid[i], onetvgshift[i], onetvglogo, onegroup[i], channel[i]))   
			m3ufile.write(extinf)
			stream = vrfSTREAM(onestream[i], oneid[i]) 
			m3ufile.write(stream)
		m3ufile.close() 
		scrtxt('Плейлист сформирован успешно')  
	else:
		scrtxt('Сервер базы не ответил')
 
def readchannlist(channlist): 
	idchann = ''
	namechann = ''
	namegroup = ''
	tvgid = ''
	tvgshift = ''
	filelist = open(channlist, 'r') 
	for line in filelist.readlines():
		channel = line.split(';')
		idchann = idchann + channel[0].strip(' \n\t') + ','
		namechann = namechann + channel[1].strip(' \n\t') + ','
		namegroup = namegroup + channel[2].strip(' \n\t') + ','
		tvgid = tvgid + channel[3].strip('\n\t') + ',' 
		tvgshift = tvgshift + channel[4].strip('\n\t') + ',' 
	filelist.close() 
	return idchann.rstrip(','), namechann.rstrip(','), namegroup.rstrip(','),tvgid.rstrip(','),tvgshift.rstrip(',')
idchann,namechann,namegroup,tvgid,tvgshift = readchannlist(CHLIST) 
robotIPTV(idchann,namechann,namegroup,tvgid,tvgshift)  
