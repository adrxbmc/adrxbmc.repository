#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2015 AdrXbmc

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os,sys,time
from resolvers import *

addon_id = 'plugin.video.adultstv'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
down_path = selfAddon.getSetting('download-folder')
base_url = 'http://www.freehdporn.ws/'
mensagemprogresso = xbmcgui.DialogProgress()

def traducao(texto):
	return selfAddon.getLocalizedString(texto).encode('utf-8')

#MENUS############################################

def fhdp_menu():
	addDir('New HD Porn','http://www.freehdporn.ws/',301,artfolder + 'videos.png')
	addDir(traducao(2022),'-',303,artfolder + 'search.png')
	addDir(traducao(2031),'-',304,artfolder + 'estudios.png')
	addDir(traducao(2032),'-',305,artfolder + 'pstars.png')
	addDir(traducao(2028),'-',306,artfolder + 'cat.png')
	
###################################################################################
#FUNCOES
def download(name,url):
	if down_path == '':
		dialog = xbmcgui.Dialog()
		dialog.ok(traducao(2010), traducao(2024))
		selfAddon.openSettings()
		return
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	mensagemprogresso.update(0)
	try: url = re.compile('<iframe src="(.+?)" class="modal_video"').findall(abrir_url(url))[0].replace('../',base_url)
	except: pass
	url_video = vkcom_resolver(url)
	if not url_video: return
	url = url_video
	
	name = re.sub('[^-a-zA-Z0-9_.()\\\/ ]+', '',name)
	name += ' - ' + url_video[1] + '.mp4'
	mypath=os.path.join(down_path,name)
	if os.path.isfile(mypath) is True:
		dialog = xbmcgui.Dialog()
		dialog.ok(traducao(2010),traducao(2025))
		return
	mensagemprogresso.close()  
	dp = xbmcgui.DialogProgress()
	dp.create('Download')
	start_time = time.time()
	try: urllib.urlretrieve(url, mypath, lambda nb, bs, fs: dialogdown(nb, bs, fs, dp, start_time))
	except:
		while os.path.exists(mypath): 
			try: os.remove(mypath); break 
			except: pass
		dp.close()
		return
	dp.close()
	
def dialogdown(numblocks, blocksize, filesize, dp, start_time):
      try:
            percent = min(numblocks * blocksize * 100 / filesize, 100)
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: eta = 0 
            kbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '%.02f MB %s %.02f MB' % (currently_downloaded,traducao(2026), total) 
            e = ' (%.0f Kb/s) ' % kbps_speed 
            tempo = traducao(2027) + ' %02d:%02d' % divmod(eta, 60) 
            dp.update(percent, mbs + e,tempo)
      except: 
            percent = 100 
            dp.update(percent) 
      if dp.iscanceled(): 
            dp.close()
            raise StopDownloading('Stopped Downloading')

class StopDownloading(Exception):
      def __init__(self, value): self.value = value 
      def __str__(self): return repr(self.value)
	  
def listar_estudios():
	codigo_fonte = abrir_url('http://www.freehdporn.ws')
	try: texto = re.findall('<h2>Studios</h2>(.+?)</ul>',codigo_fonte,re.DOTALL)[0]
	except: return
	match = re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(texto)
	for url,titulo in match:
		addDir(titulo,base_url+url,301,artfolder + 'videos.png')
	xbmc.executebuiltin("Container.SetViewMode(50)")

def listar_actrizes():
	codigo_fonte = abrir_url('http://www.freehdporn.ws')
	try: texto = re.findall('<h2>Actresses</h2>(.+?)</ul>',codigo_fonte,re.DOTALL)[0]
	except: return
	match = re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(texto)
	for url,titulo in match:
		addDir(titulo,base_url+url,301,artfolder + 'videos.png')
	xbmc.executebuiltin("Container.SetViewMode(50)")

def listar_categorias():
	codigo_fonte = abrir_url('http://www.freehdporn.ws')
	try: texto = re.findall('<h2>Category</h2>(.+?)</ul>',codigo_fonte,re.DOTALL)[0]
	except: return
	match = re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(texto)
	for url,titulo in match:
		addDir(titulo,base_url+url,301,artfolder + 'videos.png')
	xbmc.executebuiltin("Container.SetViewMode(50)")
	
def listar_videos(url):
	codigo_fonte = abrir_url(url)
	match = re.compile('<a href="(.+?)" rel="noreferrer" target="_blank" title="(.+?)><img src="(.+?)"').findall(codigo_fonte)
	match += re.compile('<a href="(.+?)" title="(.+?)"><img src="(.+?)" alt=".+?" /></a>').findall(codigo_fonte)

	i=1
	total = len(match)
	for url,titulo,img in match:
		if titulo == '"':
			titulo = 'Video ' + str(i)
			i += 1
		else: titulo = titulo[:-1]
		if 'freehdporn.ws' not in img:
			img = base_url + img
		if 'freehdporn.ws' not in url:
			url = base_url + url
		titulo = titulo.replace("&#8211;","-")
		titulo = titulo.replace("&#8217;","'")
		addDir(titulo,url,302,img,total,False,True)
	
	page = re.compile("class='active'>.+?</a><a href='(.+?)'>.+?<").findall(codigo_fonte)
	try: url_base = re.compile('<link rel="canonical" href="(.+?)"').findall(codigo_fonte)[0]
	except: return
	for url_prox_pagina in page:
		addDir(traducao(2050),url_base + str(url_prox_pagina),301,artfolder + 'next.png')
		break
	xbmc.executebuiltin("Container.SetViewMode(500)")
	
def encontrar_fontes(name,url,iconimage):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	mensagemprogresso.update(0)
	try: url = re.compile('<iframe src="(.+?)" class="modal_video"').findall(abrir_url(url))[0].replace('../',base_url)
	except: pass
	url_video = vkcom_resolver(url)
	if url_video: play(name,url_video,iconimage)
	
def play(name,streamurl,iconimage = "DefaultVideo.png"):
	listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	player.play(streamurl,listitem)
	
def pesquisa():
	keyb = xbmc.Keyboard('', traducao(2022)+':')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		parametro_pesquisa=urllib.quote(search)
		url = 'http://freehdporn.ws/hd_porn.php?s=' + str(parametro_pesquisa)
		listar_videos(url)
	
###################################################################################

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addDir(name,url,mode,iconimage,total=1,pasta = True,video=False):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	cm =[]
	if video: 
		cm.append(('Download', 'XBMC.RunPlugin(%s?mode=307&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
		liz.addContextMenuItems(cm, replaceItems=True) 	
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok
	
def mode(mode,name,url,iconimage):
	if mode==300: fhdp_menu()
	elif mode==301: listar_videos(url)
	elif mode==302: encontrar_fontes(name,url,iconimage)
	elif mode==303: pesquisa()
	elif mode==304: listar_estudios()
	elif mode==305: listar_actrizes()
	elif mode==306: listar_categorias()
	elif mode==307: download(name,url)