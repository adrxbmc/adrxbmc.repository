#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2015 AdrXbmc

import re,xbmcgui,xbmcaddon,base64
from utilis import *
from t0mm0.common.addon import Addon

addon_id = 'plugin.video.adultstv'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id)

def traducao(texto):
	return selfAddon.getLocalizedString(texto).encode('utf-8')

def powvideonet(url):
	import packer
	form_values = {}
	for i in re.finditer('<input.*?name="(.*?)".*?value="(.*?)".*?>', abrir_url(url)):
		form_values[i.group(1)] = i.group(2)
	xbmc.sleep(1000)
	html = net.http_POST(url, form_data=form_values).content
	texto = 'eval(function(p,a,c,k,e,d)'+re.findall("eval\(function\(p,a,c,k,e,d\)(.*?)</script>",html,re.DOTALL)[0]
	url_video = 'http' + re.compile("file:'http(.+?)'").findall(packer.unpack(texto).replace('\\',''))[0]
	return url_video
	
def videowoodtv(url):
	if not "embed" in url: url = 'http://videowood.tv/embed/' + re.compile('src="http://videowood.tv/embed/(.+?)"').findall(abrir_url(url))[0]
	codigo_fonte = abrir_url(url)
	file = re.compile('file: "(.+?)"').findall(codigo_fonte)[0]
	swf = re.compile('flashplayer: "(.+?)"').findall(codigo_fonte)[0]
	#streamurl = file + ' swfUrl=' + swf
	return file
	
def streaminto(url):
	form_values = {}
	for i in re.finditer('<input.*?name="(.*?)".*?value="(.*?)".*?>', abrir_url(url)):
		form_values[i.group(1)] = i.group(2)
	addon.show_countdown(5)
	html = net.http_POST(url, form_data=form_values).content
	rtmp = re.compile('streamer: "(.+?)"').findall(html)[0]
	playpath = re.compile(' file: "(.+?)"').findall(html)[0]
	swf = re.compile(' src: "(.+?)"').findall(html)[0]
	streamurl=rtmp + ' playPath=' + playpath + ' swfUrl=' + swf + ' live=true pageUrl=' + url
	return streamurl
	
def videomega_resolver(referer):

	html = abrir_url(referer)
	ref_data={'Host':'videomega.tv',
			  'Connection':'Keep-alive',
			  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			  #'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
			  'User-Agent':'stagefright/1.2 (Linux;Android 4.4.4)',
			  'Referer':referer}
	if re.search('http://videomega.tv/iframe.js',html):
		lines = html.splitlines()
		aux = ''
		for line in lines:
			if re.search('http://videomega.tv/iframe.js',line):
				aux = line
				break;
		ref = re.compile('ref="(.+?)"').findall(line)[0]
	else:
		try:
			hash = re.compile('"http://videomega.tv/validatehash.php\?hashkey\=(.+?)"').findall(html)[0]
			ref = re.compile('ref="(.+?)"').findall(abrir_url_tommy("http://videomega.tv/validatehash.php?hashkey="+hash,ref_data))[0]
		except:
			iframe = re.compile('"http://videomega.tv/iframe.php\?(.+?)"').findall(html)[0] + '&'
			ref = re.compile('ref=(.+?)&').findall(iframe)[0]
	
	#url = 'http://videomega.tv/iframe.php?ref=' + ref
	url = 'http://videomega.tv/cdn.php?ref='+ref+'&width=638&height=431&val=1'
	iframe_html = abrir_url_tommy(url,ref_data)
	#####
	url_video = re.compile('<source src="(.+?)"').findall(iframe_html)[0]
	#try: url_legendas = re.compile('<track kind="captions" src="(.+?)"').findall(iframe_html)[0]
	#except: url_legendas = '-'
	ref_data['Referer'] = url
	return url_video+headers_str(ref_data)
	'''
	code = re.compile('document.write\(unescape\("(.+?)"\)\)\;').findall(iframe_html)
	id = re.compile('<div id="(.+?)" name="adblock"').findall(iframe_html)[0]
	for c in code:
		aux = urllib.unquote(c)
		if re.search(id,aux):
			texto = aux
			break
	try: url_video = re.compile('file:"(.+?)"').findall(texto)[0]
	except: 
		try: url_video = re.compile('file: "(.+?)"').findall(texto)[0]
		except: url_video = '-'
	if not 'mp4' in url_video: 
		xbmcgui.Dialog().ok(traducao(2010),traducao(2030))
		return 'erro'
	#try: url_legendas = re.compile('http://videomega.tv/servesrt.php\?s=(.+?).srt').findall(texto)[0] + '.srt'
	#except: url_legendas = '-'
	ref_data={'Host':url_video.split('/')[2],
			  'Connection':'Keep-alive',
			  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			  'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
			  'Referer':'http://videomega.tv/player/jwplayer.flash.swf'}
	return url_video+headers_str(ref_data)
	'''
	
def vkcom_resolver(video_url):
	import random
	
	if re.search("vk\.com/video([\d]+)_([\d]+)", video_url):
		video_match = re.search("vk\.com/video([\d]+)_([\d]+)", video_url)
		video_oid = video_match.group(1)
		video_id = video_match.group(2)
		javaplugin_referer = "http://javaplugin.org/WL/vk/plugins/gkplugins_vk.swf?rand=0."+str(random.randint(1000000000000000,9999999999999999))
		codigo_fonte = abrir_url_custom("http://javaplugin.org/WL/vk/plugins/plugins_vk.php",referer = javaplugin_referer,post = {"url":video_url,"icookie":"","iagent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0","ihttpheader":"true","iheader":"true"})
		codigo_fonte_2 = abrir_url_custom("http://javaplugin.org/WL/vk/plugins/plugins_vk.php",referer = javaplugin_referer,post = {"checkcookie":"true"})
		codigo_fonte_3 = abrir_url_custom("http://javaplugin.org/WL/vk/plugins/plugins_vk.php",referer = javaplugin_referer,post = {"url":"https://vk.com/al_video.php","iagent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0","iheader":"true","icookie":"remixsid="+codigo_fonte_2[8:]+";remixlang=3","ipost":"true","ipostfield":"al=1&oid="+video_oid+"&act=video_embed_box&vid="+video_id,"isslverify":"true","ihttpheader":"true"})
		video_hash = re.search("<iframe.*?src=\".*?vk\.com/video_ext\.php\?oid\=.*?&id\=.*?&hash\=(.+?)\".*?>", codigo_fonte_3).group(1)
	elif re.search("vk\.com/video_ext\.php\?oid\=([-?\d]+)&id\=([\d]+)&hash\=(.+)", video_url):
		video_match = re.search("vk\.com/video_ext\.php\?oid\=([-?\d]+)&id\=([\d]+)&hash\=(.+?)&", video_url+'&')
		video_oid = video_match.group(1)
		video_id = video_match.group(2)
		video_hash = video_match.group(3)
	else:
		xbmcgui.Dialog().ok(traducao(2010),traducao(2030))
		return False
		
	api = 'http://api.vk.com/method/video.getEmbed?oid='+video_oid+'&video_id='+video_id+'&embed_hash='+video_hash+'&callback=responseWork'
	codigo_fonte = abrir_url_custom(api)
	qualidade = []
	urls = []
	for x in ["1080","960","720","480","360","240"]:
		try: u = re.compile('"url'+x+'":"(.+?)"').findall(codigo_fonte)[0]
		except: continue
		qualidade.append(x)
		urls.append(u.replace('\\',''))
	if len(urls)==0:
		xbmcgui.Dialog().ok(traducao(2010),traducao(2030))
		return False
	index = -1
	if selfAddon.getSetting('max_qual')=='true':
		max = 0
		for x in range(0,len(qualidade)):
			if int(qualidade[x])>max:
				max = qualidade[x]
				index = x
	else:
		index = xbmcgui.Dialog().select(traducao(2012), qualidade)
	if index==-1: return False
	return urls[index]
	
def hqq_resolver(url):

	#DECODERS

	def _decode2(file_url):
		def K12K(a, typ='b'):
			codec_a = ["k", "3", "8", "N", "x", "c", "5", "R", "D", "G", "L", "9", "g", "6", "T", "w", "p", "b", "7", "4", "v", "B", "s", "t", "m", "="]
			codec_b = ["u", "I", "Z", "z", "n", "Q", "f", "U", "l", "a", "1", "J", "i", "2", "Y", "0", "e", "o", "H", "V", "W", "X", "d", "y", "M", "q"]
			if 'd' == typ:
				tmp = codec_a
				codec_a = codec_b
				codec_b = tmp
			idx = 0
			while idx < len(codec_a):
				a = a.replace(codec_a[idx], "___");
				a = a.replace(codec_b[idx], codec_a[idx]);
				a = a.replace("___", codec_b[idx]);
				idx += 1
			return a

		def _xc13(_arg1):
			_lg27 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
			_local2 = ""
			_local3 = [0, 0, 0, 0]
			_local4 = [0, 0, 0]
			_local5 = 0
			while _local5 < len(_arg1):
				_local6 = 0;
				while _local6 < 4 and (_local5 + _local6) < len(_arg1):
					_local3[_local6] = ( _lg27.find( _arg1[_local5 + _local6] ) )
					_local6 += 1;
				_local4[0] = ((_local3[0] << 2) + ((_local3[1] & 48) >> 4));
				_local4[1] = (((_local3[1] & 15) << 4) + ((_local3[2] & 60) >> 2));
				_local4[2] = (((_local3[2] & 3) << 6) + _local3[3]);

				_local7 = 0;
				while _local7 < len(_local4):
					if _local3[_local7 + 1] == 64:
						break;
					_local2 += chr(_local4[_local7]);
					_local7 += 1;
				_local5 += 4;
			return _local2

		return _xc13(K12K(file_url, 'e'))
		
	def _decode(data):
		def O1l(string):
			ret = ""
			i = len(string) - 1;
			while i>=0:
				ret+= string[i]
				i-=1
			return ret

		def l0I(data, ):
			enc = ""
			dec = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
			i=0
			while True:
				h1 = dec.find(data[i]); i+=1;
				h2 = dec.find(data[i]); i+=1;
				h3 = dec.find(data[i]); i+=1;
				h4 = dec.find(data[i]); i+=1;
				bits = h1 << 18 | h2 << 12 | h3 << 6 | h4
				o1 = bits >> 16 & 0xff
				o2 = bits >> 8 & 0xff
				o3 = bits & 0xff
				if (h3 == 64):
					enc += unichr(o1)
				else:
					if (h4 == 64):
						enc += unichr(o1)+ unichr(o2)
					else:
						enc += unichr(o1)+ unichr(o2) + unichr(o3)
				if  (i >= len(data)):
					break
			return enc

		jsdec = l0I(O1l(data))
		escape= re.search("var _escape=\'([^\']+)", jsdec).group(1)
		return escape.replace('%','\\').decode('unicode-escape')

	###############################################################################
	u = re.compile('document.write\(unescape\("(.+?)"\)\)').findall(abrir_url(url))[0]
	u = urllib.unquote(u)
	vid = re.compile("var vid='(.+?)'").findall(u)[0]
	vurl = 'http://hqq.tv/player/embed_player.php?vid=%s&autoplay=no' % vid
	html = abrir_url(vurl)

	b64enc= re.search('base64([^\"]+)',html, re.DOTALL)
	b64dec = b64enc and base64.decodestring(b64enc.group(1))
	hash = b64dec and re.search("\'([^']+)\'", b64dec).group(1)
	form = _decode(hash)
	at = re.compile('name="at" id="text" value="(.+?)"').findall(form)[0]
	req = 'http://hqq.tv/sec/player/embed_player.php?vid=%s&at=%s&autoplayed=yes&referer=on&http_referer=&pass=' % (vid,at)
	
	match = re.compile('document.write\(unescape\("(.+?)"\)\)').findall(abrir_url(req))
	for m in match:
		code = urllib.unquote(m)
		try:
			h = re.compile('var.+?= "#(.+?)"').findall(code)[0]
			break
		except: pass
	
	l = len(h)
	i=0
	hex = ''
	while(i<l):
		if i%3==0: pass
		else: hex += h[i]
		i+=1
	return hex.decode('hex')