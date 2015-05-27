#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2015 AdrXbmc

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os,sys,time

addon_id = 'plugin.video.adultstv'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
down_path = selfAddon.getSetting('download-folder')
mensagemprogresso = xbmcgui.DialogProgress()
base_url = 'http://www.xvideos.com/'

def traducao(texto):
	return selfAddon.getLocalizedString(texto).encode('utf-8')

def menu():
	addDir(traducao(2019),base_url,701,artfolder + 'videos.png')
	addDir(traducao(2021),'http://www.xvideos.com/best/',701,artfolder + 'fav.png')
	addDir(traducao(2029),'http://www.xvideos.com/pornstars',703,artfolder + 'pstars.png')
	addDir(traducao(2000),'http://www.xvideos.com/channels',703,artfolder + 'videos.png')
	addDir(traducao(2028),'-',706,artfolder + 'cat.png')
	addDir(traducao(2022),'-',705,artfolder + 'search.png')
	
def cat():
	html = abrir_url(base_url)
	cat = re.findall('<div id="categories"(.*?)</div>',html,re.DOTALL)[0]
	match = re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(cat)
	for u, c in match:
		while c[0]==' ': c = c[1:]
		addDir(c,base_url+u,701,artfolder + 'cat.png')
	
def pesquisa():
	keyb = xbmc.Keyboard('', traducao(2022)+':')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		parametro_pesquisa=urllib.quote(search)
		url = 'http://www.xvideos.com/?k=' + str(parametro_pesquisa)
		listar_videos(url)
	
def listar_profiles(url):
	html = abrir_url(url)
	pstars = re.findall('<div class="thumbProfile"(.*?) videos',html,re.DOTALL)
	
	for p in pstars:
		match = re.compile('<a href="(.+?)">(.+?)</a>').findall(p)
		img = re.compile('<img src="(.+?)"').findall(p)[0]
		if re.search('pornstars-click',match[0][0]):
			link = base_url+match[0][0].replace('pornstars-click','profiles')+'/pornstar_videos/0/0/'
		elif re.search('channels-click',match[0][0]):
			link = base_url+match[0][0].replace('channels-click','profiles')+'/uploads/0/0/'
		else: return
		addDir(match[0][1],link,704,img)
	try:
		nextp = re.compile('<li><a class="nP" href="(.+?)">Next</a></li>').findall(html)[0]
		addDir(traducao(2050),base_url+nextp,703,artfolder + 'next.png')
	except: pass
	
def listar_videos2(url):
	html = abrir_url(url)
	videos = re.findall('<div class="thumbBlock"(.*?)/span\>',html,re.DOTALL)
	for vid in videos:
		match = re.compile('<a href="(.+?)"><img src="(.+?)"').findall(vid)
		title = re.compile('<p><a href=".+?">(.+?)</a></p>').findall(vid)[0]
		try:
			duration = re.compile('class="duration">(.+?)<').findall(vid)[0]
			duration = int(re.compile('\((.+?) min').findall(duration)[0])
		except: duration = 0
		addDir(title,base_url+match[0][0],702,match[0][1],False,duration=duration)
	
	try:
		nextp = re.compile('<li><a class="nP" data-type="(.+?)" data-id=".+?" data-page="(.+?)">Next</a></li>').findall(html)[0]
		nextp = url.split(nextp[0])[0] + nextp[0] +'/0/' + nextp[1]
		print nextp
		addDir(traducao(2050),nextp,704,artfolder + 'next.png')
	except: pass
	
def listar_videos(url):
	html = abrir_url(url)
	videos = re.findall('<div class="thumbInside">(.*?)/span\>',html,re.DOTALL)
	for vid in videos:
		match = re.compile('<a href="(.+?)"><img src="(.+?)"').findall(vid)
		title = re.compile('title="(.+?)"').findall(vid)[0]
		try:
			duration = re.compile('class="duration">(.+?)<').findall(vid)[0]
			duration = int(re.compile('\((.+?) min').findall(duration)[0])
		except: duration = 0
		addDir(title,base_url+match[0][0],702,match[0][1],False,duration=duration)
	
	try:
		nextp = re.compile('<li><a class="nP" href="(.+?)">Next</a></li>').findall(html)[0]
		addDir(traducao(2050),base_url+nextp,701,artfolder + 'next.png')
	except: pass
	
def play(name,url,iconimage):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	url_video = urllib.unquote(re.compile('flv_url=(.+?)&').findall(abrir_url(url))[0])
	liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	mensagemprogresso.close()
	player.play(url_video,liz)
	
def mode(mode,name,url,iconimage,offset):
	if mode==700: menu()
	elif mode==701: listar_videos(url)
	elif mode==702: play(name,url,iconimage)
	elif mode==703: listar_profiles(url)
	elif mode==704: listar_videos2(url)
	elif mode==705: pesquisa()
	elif mode==706: cat()
	
def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link
		
def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,pasta = True,total=1,video=False,offset=0,duration=False):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&offset="+str(offset)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	if duration: liz.setInfo(type="Video", infoLabels={"duration":duration})
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	cm =[]
	if video: 
		cm.append(('Download', 'XBMC.RunPlugin(%s?mode=205&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
		liz.addContextMenuItems(cm, replaceItems=True) 
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok