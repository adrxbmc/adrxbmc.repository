#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2015 AdrXbmc

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os,sys,time
import urlresolver
from resolvers import *

addon_id = 'plugin.video.adultstv'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
down_path = selfAddon.getSetting('download-folder')
mensagemprogresso = xbmcgui.DialogProgress()

################################################## 

def traducao(texto):
	return selfAddon.getLocalizedString(texto).encode('utf-8')

#MENUS############################################

def menu():
	addDir(traducao(2033),"http://streamxxx.tv/new-movies/",402,artfolder + 'videos.png')
	addDir(traducao(2034),"http://streamxxx.tv/category/movies/",402,artfolder + 'videos.png')
	addDir(traducao(2035),"http://streamxxx.tv/category/movies/international-movies/",402,artfolder + 'videos.png')
	addDir(traducao(2036),"http://streamxxx.tv/category/movies/film-porno-italian/",402,artfolder + 'videos.png')
	addDir(traducao(2037),"-",404,artfolder + 'cat.png')
	addDir(traducao(2022),"-",403,artfolder + 'search.png')
	
def clips():
	codigo_fonte = abrir_url("http://streamxxx.tv/")
	texto = re.findall('<a href="http://streamxxx.tv/category/clips/">(.*?)</ul>',codigo_fonte,re.DOTALL)[0]
	match = re.compile('<li id="menu-item-.+?" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-.+?"><a href="(.+?)">(.+?)</a></li>').findall(texto)
	for url, name in match:
		addDir(name,url,402,artfolder + 'videos.png')
	
def pesquisa():
	keyb = xbmc.Keyboard('', traducao(2022)+':')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		parametro_pesquisa=urllib.quote(search)
		url = 'http://streamxxx.tv/?s=' + str(parametro_pesquisa)
		listar_videos(url)
		
def listar_videos(url):
	codigo_fonte = abrir_url(url)
	match = re.compile('\s+\n\s+<div class="thumb">\s+<a class="clip-link" data-id=".+?" title="(.+?)" href="(.+?)">\s+<span class="clip">\s+<img src="(.+?)" alt=".+?" /><span class="vertical-align"></span>').findall(codigo_fonte)
	for title,link,img in match:
		addDir(title,link,401,img,1,False)
	try: 
		page = re.compile('rel="next" href="(.+?)">').findall(codigo_fonte)[0]
		addDir("Next page >>",page,402,artfolder + 'next.png')
	except: pass
	
def listar_fontes(name,url,iconimage):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	codigo_fonte = abrir_url(url);
	try: texto = re.findall('alt="Streaming Link:"(.*?)<center>',codigo_fonte,re.DOTALL)[0]
	except:
		try: texto = re.findall('alt="Streaming Link:"(.*?)</div>',codigo_fonte,re.DOTALL)[0]
		except:
			xbmcgui.Dialog().ok(traducao(2010), traducao(2038))
			return
	#print texto
	#links = re.compile('href="(.+?)"').findall(texto)
	links = re.compile('>http(.+?)</a>').findall(texto)
	links += re.compile('title="http(.+?)"').findall(texto)
	hosts = []
	sources = []
	for link in links:
		link = ('http' + link).replace("https","http")
		source = find_sources(link)
		if source: 
			hosts.append(re.compile("'host': '(.+?)'").findall(str(source))[0])
			sources.append(source)
		elif myresolvers(link):
			hosts.append(myresolvers(link))
			sources.append("myresolvers"+link)
	if len(hosts) == 0:
		xbmcgui.Dialog().ok(traducao(2010), traducao(2038))
		return
	if len(hosts) == 1: index=0
	else:
		index = xbmcgui.Dialog().select(traducao(2006), hosts)
		if index == -1: return
	if "myresolvers" in str(sources[index]): 
		try: urlplayer = _myresolvers(sources[index].replace("myresolvers",""))
		except:
			xbmcgui.Dialog().ok(traducao(2010), traducao(2039))
			return
	else:
		try: urlplayer = sources[index].resolve() + " live=true"
		except:
			xbmcgui.Dialog().ok(traducao(2010), traducao(2039))
			return
	try: play(name,urlplayer,iconimage)
	except: xbmcgui.Dialog().ok(traducao(2010), traducao(2039))
	
###################################################################################
def myresolvers(url):
	if "streamin.to" in url: return "streamin.to"
	if "videowood.tv" in url: return "videowood.tv"
	if "powvideo.net" in url: return "powvideo.net"
	else: return None

def _myresolvers(url):
	if "streamin.to" in url: return streaminto(url)
	if "videowood.tv" in url: return videowoodtv(url)
	if "powvideo.net" in url: return powvideonet(url)
	else: return None

def find_sources(url):
	sources=[]
	hosted_media = urlresolver.HostedMediaFile(url=url)
	sources.append(hosted_media)
	source = urlresolver.choose_source(sources)
	return source

def play(name,streamurl,iconimage = "DefaultVideo.png"):
	listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	player.play(streamurl,listitem)
	
def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addLink(name,url,iconimage,video=False):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	cm =[]
	if video: cm.append(('Download', 'XBMC.RunPlugin(%s?mode=307&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	liz.addContextMenuItems(cm, replaceItems=True) 	
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,total=1,pasta = True):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	cm =[]
	liz.addContextMenuItems(cm, replaceItems=True)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok