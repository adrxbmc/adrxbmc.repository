#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2015 AdrXbmc

import urllib,urllib2,xbmcgui,re,xbmcaddon
from t0mm0.common.net import Net
net = Net()

addon_id = 'plugin.video.adultstv'
selfAddon = xbmcaddon.Addon(id=addon_id)

def traducao(texto):
	return selfAddon.getLocalizedString(texto).encode('utf-8')

def str_int(str):
	try: int(str[0])
	except: return -1
	for x in range(0,len(str)):
		try: int(str[x])
		except: return int(str[0:x])
	return int(str)
	
def file_name(path):
	import ntpath
	head, tail = ntpath.split(path)
	return tail or ntpath.basename(head)

def m3u8(m3u):
	try:
		inf = abrir_url(m3u).splitlines()
		qualidade = []
		qualidade_str = []
		for line in inf:
			line=line.strip()
			if line.startswith('#EXT-X-STREAM-INF'): 
				qualidade.append(str_int(line.split('#EXT-X-STREAM-INF')[1].split('BANDWIDTH=')[1]))
				qualidade_str.append('%s kbps' % (str_int(line.split('#EXT-X-STREAM-INF')[1].split('BANDWIDTH=')[1])/1000))
		m3u8=''
		if len(qualidade)==0:
			#xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
			#return "erro"
			return m3u
		if selfAddon.getSetting('max_qual')=='true': qualidade_escolhida = str(max(qualidade))
		else:
			index = xbmcgui.Dialog().select(traducao(2012), qualidade_str)
			if index == -1: return
			qualidade_escolhida = str(qualidade[index])
		for x in range(0,len(inf)):
			if 'BANDWIDTH='+qualidade_escolhida in inf[x]:
				m3u8 = inf[x+1]
				break
		if not re.search('http://', m3u8):
			m3u8 = m3u.replace(file_name(m3u),m3u8)
		return m3u8
	except:
		xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
		return "erro"
		
def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def abrir_url_tommy(url,referencia,form_data=None,erro=True):
	print "A fazer request tommy de: " + url
	try:
		if form_data==None:link = net.http_GET(url,referencia).content
		else:link= net.http_POST(url,form_data=form_data,headers=referencia).content.encode('latin-1','ignore')
		return link

	except urllib2.HTTPError, e:
		return "Erro"
	except urllib2.URLError, e:
		return "Erro"

def abrir_url_custom(url,**kwargs):
	for key, value in kwargs.items(): exec('%s = %s' % (key, repr(value)))
	if 'post' in locals():
		data = urllib.urlencode(post)
		req = urllib2.Request(url,data)
	else: req = urllib2.Request(url)
	if 'headers' in locals():
		for x in range(0, len(headers)):
			req.add_header(headers.keys()[x], headers.values()[x])
	if 'user_agent' in locals(): req.add_header('User-Agent', user_agent)
	else: req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:33.0) Gecko/20100101 Firefox/33.0')
	if 'referer' in locals(): req.add_header('Referer', referer)
	if 'timeout' in locals(): response = urllib2.urlopen(req, timeout=timeout)
	else: response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link
	
def headers_str(headers):
	start = True
	headers_str = ''
	for k,v in headers.items():
		if start:
			headers_str += '|'+urllib.quote_plus(k)+'='+urllib.quote_plus(v)
			start = False
		else: headers_str += '&'+urllib.quote_plus(k)+'='+urllib.quote_plus(v)
	return headers_str