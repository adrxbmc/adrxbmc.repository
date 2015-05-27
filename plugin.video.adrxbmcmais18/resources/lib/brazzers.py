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
mensagemprogresso = xbmcgui.DialogProgress()

def traducao(texto):
	return selfAddon.getLocalizedString(texto).encode('utf-8')

def brazzers_menu():
	addDir(traducao(2019),'http://brazzershd.net/category/brazzers-hd/?orderby=date',201,artfolder + 'videos.png')
	addDir(traducao(2020),'http://brazzershd.net/category/brazzers-hd/?orderby=views',201,artfolder + 'videos.png')
	addDir(traducao(2021),'http://brazzershd.net/category/brazzers-hd/?orderby=likes',201,artfolder + 'fav.png')
	addDir(traducao(2022),'http://brazzershd.net/',203,artfolder + 'search.png')
	addDir(traducao(2023),'-',207,artfolder + 'cat.png')
	xbmc.executebuiltin("Container.SetViewMode(50)")

def download(name,url):
	if down_path == '':
		dialog = xbmcgui.Dialog()
		dialog.ok(traducao(2010), traducao(2024))
		selfAddon.openSettings()
		return
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	mensagemprogresso.update(0)
	
	try: video_url = re.compile('<iframe src="(.+?)"').findall(abrir_url(url))[0]
	except: return
	if re.search('urlvk=',video_url): video_url = urllib.unquote(video_url.split('urlvk=')[1])
	if video_url[:2] == '//': video_url = 'http:' + video_url
	url_video = vkcom_resolver(video_url)
	
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
	start_time = time.time()		# url - url do ficheiro    mypath - localizacao ex: c:\file.mp3
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
	  
def cat():
	codigo_fonte = abrir_url('http://brazzershd.net')
	match = re.compile('href="http://brazzershd.net/tag/(.+?)">(.+?)</a></li>').findall(codigo_fonte)
	addLink("[B][COLOR white]"+traducao(2028)+"[/COLOR][/B]",'','-')
	for url, titulo in match:
		titulo = titulo.replace('&#8217;',"'")
		addDir(titulo,'http://brazzershd.net/tag/' + url,201,artfolder + 'videos.png')
		if(titulo == '69'): 
			addLink("",'','-')
			addLink("[B][COLOR white]"+traducao(2029)+"[/COLOR][/B]",'','-')
	xbmc.executebuiltin("Container.SetViewMode(50)")
	
def listar_videos(url):
	codigo_fonte = abrir_url(url)
	match = re.compile('<h2 class="entry-title"><a href="(.+?)"').findall(codigo_fonte)
	match2 = re.compile('title="Permalink to (.+?)"').findall(codigo_fonte)
	match3 = re.compile('<img src="(.+?)320x180.jpg"').findall(codigo_fonte)

	a = []
	for x in range(0, len(match)):
		temp = [match[x],match2[x],match3[x]]; 
		a.append(temp);
	total=len(a)
	for url,titulo,img in a:
		titulo = titulo.replace("&#8211;","-")
		titulo = titulo.replace("&#8217;","'")
		if img[:2] == '//': img = 'http:' + img
		addDir(titulo,url,202,img+'320x180.jpg',False,total,True)
	
	try:
		page = re.compile('<link rel="next" href="(.+?)"').findall(codigo_fonte)[0]
		if page[:2] == '//': page = 'http:' + page
		addDir(traducao(2050),page,201,artfolder + 'next.png')
	except: pass
	
	xbmc.executebuiltin("Container.SetViewMode(500)")
	
def encontrar_fontes(name,url,iconimage):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	mensagemprogresso.update(0)
	html = abrir_url(url)
	try: 
		video_url = re.compile('vk.com(.+?)"').findall(html)[0]
		video_url = 'http://vk.com' + video_url
	except: 
		try: 
			video_url = re.compile('hqq.tv(.+?)"').findall(html)[0]
			video_url = 'http://hqq.tv' + video_url
		except: return
	video_url = urllib.unquote(video_url)
	
	if re.search('vk.com',video_url): url_video = vkcom_resolver(video_url)
	elif re.search('hqq.tv',video_url): url_video = hqq_resolver(video_url)
	else: return 
	
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
		url = 'http://brazzershd.net/?s=' + str(parametro_pesquisa)
		listar_videos(url)

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

def addDir(name,url,mode,iconimage,pasta = True,total=1,video=False):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	cm =[]
	if video: 
		cm.append(('Download', 'XBMC.RunPlugin(%s?mode=205&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
		liz.addContextMenuItems(cm, replaceItems=True) 
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok