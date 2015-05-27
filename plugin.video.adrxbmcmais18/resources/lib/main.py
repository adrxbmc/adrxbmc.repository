#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2015 AdrXbmc
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os,sys,xbmcvfs,time,requests
import brazzers
import fhdp
import streamxxx
import uppod
import boaf
import ioncube
import erotik
import xvideos
from utilis import *

try:
	addon_pdf = xbmc.translatePath('special://home/addons/plugin.image.pdfreader/resources/lib')
	sys.path.append(addon_pdf)
	from pdf import pdf
	pdf = pdf()
	hpdf = True
except:
	hpdf = False


h = HTMLParser.HTMLParser()

addon_id = 'plugin.video.adultstv'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
user_agent = 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36'
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
if xbmc.getCondVisibility('system.platform.windows'): pastaperfil = pastaperfil.replace('\\','/')
mensagemprogresso = xbmcgui.DialogProgress()
entra_canais = selfAddon.getSetting('entra_canais')

ttv_api = 'http://super-pomoyka.us.to/trash/ttv-list/ttv.m3u'

def traducao(texto):
	return selfAddon.getLocalizedString(texto).encode('utf-8')

#MENUS############################################

def CATEGORIES():
	if selfAddon.getSetting('vista') == '0':
		addDir(traducao(2000),'-',21,artfolder + 'canais.png')
		addDir(traducao(2001),'-',1,artfolder + 'lista.png')
		addDir(traducao(2002),'-',101,artfolder + 'movie.png')
		addDir(traducao(2068),'-',105,artfolder + 'revistas.png')
		addDir(traducao(2003),'-',22,artfolder + 'settings.png',False)
		xbmc.executebuiltin("Container.SetViewMode(500)")
		xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
	else:
		addDir(traducao(2000),'-',21,artfolder + 'canais_m.png')
		addDir(traducao(2001),'-',1,artfolder + 'lista_m.png')
		addDir(traducao(2002),'-',101,artfolder + 'movie_m.png')
		addDir(traducao(2068),'-',105,artfolder + 'revistas_m.png')
		addDir(traducao(2003),'-',22,artfolder + 'settings_m.png',False)
		xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
		xbmc.executebuiltin("Container.SetViewMode(501)")
	if selfAddon.getSetting('pass') == "false": password()
	
def revistas(offset):
	if not hpdf:
		dialog = xbmcgui.Dialog()
		dialog.ok("Error!","PDF Reader not found.","Please install it.")
		return
		
	#http://www.mediafire.com/folder/uyf3rp6l2m141
	id = 'uyf3rp6l2m141'
	
	#folders_url='http://www.mediafire.com/api/folder/get_content.php?folder_key='+id+'&chunk=1&content_type=folders&response_format=json&rand=1789'
	#files_url='http://www.mediafire.com/api/folder/get_content.php?r=srhp&content_type=files&filter=all&order_by=name&order_direction=asc&chunk=1&version=2&folder_key='+id+'&response_format=json'

	files_url='http://www.mediafire.com/api/folder/get_content.php?r=srhp&content_type=files&filter=all&order_by=name&order_direction=asc&chunk='+str(offset)+'&version=2&folder_key='+id+'&response_format=json'
	codigo_fonte = abrir_url(files_url).replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
	match=re.findall('"filename":"(.+?)".+?"normal_download":"(.+?)"',codigo_fonte)
	for name, url in match:
		addDir(name.replace('.pdf',''),url.replace('\\',''),106,artfolder + 'revistas.png',False)
	if len(match)==100:
		addDir(traducao(2050),'-',105,artfolder + 'next.png',offset=offset+1)
	xbmc.executebuiltin("Container.SetViewMode(50)")
	
def videos():
	addDir("Brazzers",'-',200,artfolder + 'brazzers_icon.png')
	addDir("Free HD Porn",'-',300,artfolder + 'fhdp_icon.png')
	addDir("Streamxxx",'-',400,artfolder + 'streamxxx.png')
	#addDir('BoaFoda.com','-',500,artfolder + 'boaf.png')
	addDir('Ero-tik','-',600,artfolder + 'erotik.png')
	addDir('XVideos','-',700,artfolder + 'xvideos.png')
	addDir('AdrXbmc +18','-',110,artfolder + 'ab.png', pasta=False)
	bla_video('bla','bla','bla','bla')
	xbmc.executebuiltin("Container.SetViewMode(500)")
	
def bla_video(mode,name,url,iconimage):
	try:
		from bla import bla
		bla.bla_video(mode,name,url,iconimage)
	except: pass
	
def abelhas():
	addon = 'plugin.video.abelhas'
	if not xbmc.getCondVisibility('System.HasAddon('+addon+')'):
		xbmcgui.Dialog().ok(traducao(2010), traducao(2077))
		return
	
	url = urllib.quote_plus('http://abelhas.pt/AdrXbmc.18')
	name = 'Ir para uma Abelha'
	xbmc.executebuiltin('XBMC.Container.Update(plugin://%s?mode=3&url=%s&name=%s)' % (addon, url,name))
	
def _ch(name):
	if selfAddon.getSetting(name) == "true":
		return True
	return False
	
def canais():
	if entra_canais == "true": addDir(traducao(2004),'-',0,artfolder + 'menu.png')
	
	if _ch('brazzerstv'): addDir("Brazzers TV",'-',4,artfolder + "brazzers.png",False)
	if _ch('brasileirinhas'): addDir("Brasileirinhas",'-',5,artfolder + "brasileirinhas.png",False)
	if _ch('sexyhot'): addDir("SexyHot",'-',6,artfolder + "sexyhot.png",False)
	if _ch('pboytv'): addDir("Playboy TV",'-',7,artfolder + "playboy.png",False)
	if _ch('pboytvchat'): addDir("Playboy TV Chat",'-',8,artfolder + "playboyhd.png",False)
	if _ch('penthousehd'): addDir("Penthouse TV",'-',9,artfolder + "penthouse.png",False)
	if _ch('hot'): addDir("Hot",'-',10,artfolder + "hot.png",False)
	if _ch('hustlerhd'): addDir("Hustler HD",'-',11,artfolder + "hustlerhd.png",False)
	if _ch('viki'): addDir("Viki Enjoy Premium",'-',12,artfolder + "viki.png",False)
	if _ch('vietsex'): addDir("Viet Sex TV",'-',13,artfolder + "vietsextv.png",False)
	if _ch('bella'): addDir("Bella Club",'-',14,artfolder + "bellaclub.png",False)
	if _ch('bella2'): addDir("Bella Club 2",'-',15,artfolder + "bellaclub2.png",False)
	if _ch('butgo'): addDir("ButGO",'-',16,artfolder + "butgo.png",False)
	if _ch('filthon-adult'): addDir("Filthon Adult",'-',17,artfolder + "filthon.png",False)
	if _ch('filthon-adult-fetish'): addDir("Filthon Adult Fetish",'-',18,artfolder + "filthonfetish.png",False)
	if _ch('xxl'): addDir("XXL",'-',19,artfolder + "xxl.png",False)
	if _ch('frenchlover'): addDir("Frenchlover",'-',20,artfolder + "frenchlover.png",False)
	if _ch('dorceltv'): addDir("Dorcel TV",'-',23,artfolder + "dorceltv.png",False)
	if _ch('ipure'): addDir("iPure TV",'-',24,artfolder + "ipuretv.png",False)
	if _ch('private'): addDir("Private",'-',25,artfolder + "private.png",False)
	if _ch('privategold'): addDir("Private Gold",'-',26,artfolder + "privategold.png",False)
	if _ch('venus'): addDir("Venus",'-',27,artfolder + "venus.png",False)
	if _ch('xdesire'): addDir("XDesire",'-',28,artfolder + "xdesire.png",False)
	if _ch('blue-hustler'): addDir("Hustler Blue",'-',29,artfolder + "hustlerblue.png",False)
	if _ch('olala'): addDir("O-la-la",'-',30,artfolder + "olala.png",False)
	if _ch('eroxxx'): addDir("Ero XXX",'-',31,artfolder + "eroxxx.png",False)
	if _ch('amateritv'): addDir("Amateri TV",'-',32,artfolder + "amateritv.png",False)
	if _ch('russian-nights'): addDir("Russian Nights",'-',33,artfolder + "russiannights.png",False)
	if _ch('hustlertv'): addDir("Hustler TV",'-',34,artfolder + "hustlertv.png",False)
	if _ch('sexzonehd'): addDir("Sexzone HD",'-',35,artfolder + "sexzonehd.png",False)
	if _ch('redlighthd'): addDir("Redlight HD",'-',36,artfolder + "redlighthd.png",False)
	if _ch('hallotv'): addDir("Hallo TV",'-',37,artfolder + "hallotv.png",False)
	if _ch('platinumtv'): addDir("Platinum TV",'-',38,artfolder + "platinumtv.png",False)
	if _ch('sexprive'): addDir("Sexprive Brasileirinhas",'-',40,artfolder + "sexprive.png",False)
	if _ch('nightclub'): addDir("Nightclub TV",'-',41,artfolder + "nightclub.png",False)
	if _ch('temptation'): addDir("Temptation TV",'-',42,artfolder + "temptationtv.png",False)
	if _ch('sct'): addDir("SCT",'-',43,artfolder + "sct.png",False)
	if _ch('redlight_premium'): addDir("Redlight Premium",'-',44,artfolder + "red_premium.png",False)
	if _ch('bbtv'): addDir("Bluebird TV",'-',46,artfolder + "bluebird.png",False)
	if _ch('star'): addDir("Star 18+",'-',47,artfolder + "star18.png",False)
	if _ch('hotc'): addDir("Hot (China)",'-',48,artfolder + "hotc.png",False)
	#if _ch('paparazzo'): addDir("Paparazzo TV",'-',49,artfolder + "paparazzo.png",False)
	#if _ch('erox'): addDir("Erox HD",'-',50,artfolder + "erox.png",False)
	#if _ch('dusk'): addDir("Dusk TV",'-',51,artfolder + "dusk.png",False)
	if _ch('xxx1'): addDir("XXX1",'-',52,artfolder + "xxx1.png",False)
	if _ch('xxx2'): addDir("XXX2",'-',53,artfolder + "xxx2.png",False)
	if _ch('bungabunga'): addDir("Bunga Bunga",'-',54,artfolder + "bunga-bunga.png",False)
	if _ch('sathd'): addDir("Satisfaction HD",'-',55,artfolder + "sathd.png",False)
	if _ch('centox'): addDir("CentoXCento",'-',56,artfolder + "centoxcento.png",False)
	if _ch('exoticatv'): addDir("Exotica TV",'-',57,artfolder + "exoticatv.png",False)
	if _ch('pinkotv'): addDir("Pink O TV",'-',58,artfolder + "pinkotv.png",False)
	if selfAddon.getSetting('gay') == 'false':
		#Conteúdo gay
		if _ch('filthon-gay'): addDir("Filthon Gay",'-',39,artfolder + "filthongay.png",False)
		#if _ch('gboys'): addDir("G-Boys TV",'-',45,artfolder + "gboys.png",False)
	xbmc.executebuiltin("Container.SetViewMode(500)")
	xbmcplugin.setContent(int(sys.argv[1]), 'episodes')


###################################################################################
#LISTAS

def listas():
	addDir(traducao(2005)+" 1 - HasBahCa",'http://hasbahcaiptv.com/m3u/iptv/iptv/XXX.m3u',2,artfolder + "1.png")
	'''
	try:
		html = abrir_url('https://www.dropbox.com/s/h6ln6hb8l0hl4wo/userbouquet.ilu_xxx_adult.tv')
		data=re.compile('<div class="filename shmodel-filename"><span id=".+?"></span></div><div class="meta">(.+?)&nbsp;&middot;&nbsp;.+?</div>').findall(html)[0]
		data = ' - ' + data.replace('months',traducao(2045)).replace('ago',traducao(2046)).replace('day',traducao(2047))
	except: data = ''
	'''
	#http://axenttv.ru/forum/24-365-10
	addDir(traducao(2005)+" 2 - Nobody28",'-',3,artfolder + "2.png")
	addDir(traducao(2005)+" 3 - VOD",'http://hasbahcaiptv.com/m3u/movies/XXX-VOD.m3u',2,artfolder + "3.png")
	addDir(traducao(2005)+" 4 - tv-sv.com (p2p)",'-',108,artfolder + "4.png")
	addDir(traducao(2005)+" 5 - torrent-tv.ru (p2p)",'-',109,artfolder + "5.png")
	lista_bla()
	
def ttv():
	m3u = abrir_url(ttv_api).splitlines()
	for x in range(0,len(m3u)):
		if m3u[x].startswith('#EXTINF:') and '(Для взрослых)' in m3u[x]: 
			name = m3u[x].replace('(Для взрослых)','').replace("\r","").replace("\n","").split(',')[1]
			addDir(name,m3u[x+1],107,artfolder + "ttv.png",False)
	xbmc.executebuiltin("Container.SetViewMode(51)")
	
def tv_sv():
	html = abrir_url('http://www.tv-sv.com/2010/11/18.html')
	match = re.compile('<a href="(.+?)" target="myiframe" title="(.+?)"><img alt=".+?" class="c10"').findall(html)
	for url, name in match:
		try: ace = re.compile('this.loadPlayer\("(.+?)"').findall(abrir_url(url))[0]
		except: continue
		addDir(name,ace,107,artfolder + "tv-sv.jpg",False,total = len(match))
	xbmc.executebuiltin("Container.SetViewMode(51)")
	
def lista_bla(url = 'nada',name = 'nada'):
	try:
		from bla import bla
		if url=='nada':
			addDir(traducao(2005)+" 6 - "+bla.list1_s(),'list1',103,bla.icon())
			#addDir(traducao(2005)+" 9 - "+bla.list1_s(),'list2',103,bla.icon())
		elif url=='list1': bla.list1(); xbmc.executebuiltin("Container.SetViewMode(51)")
		elif url[:13]=='player_list2:': bla.player_list2(name,url.replace(url[:13],''))
		#elif url=='list2': bla.list2(); xbmc.executebuiltin("Container.SetViewMode(51)")
	except: pass
	
def lista_videos3(url):
	m3u = abrir_url(url).splitlines()
	for x in range(0,len(m3u)):
		if m3u[x].startswith('#EXTINF:') and '(Для взрослых)' in m3u[x]: 
			name = m3u[x].replace('(Для взрослых)','').replace("\r","").replace("\n","").split(',')[1]
			addLink(name,m3u[x+1].replace('rtmp://$OPT:rtmp-raw=',''),artfolder + "movie.png")
	xbmc.executebuiltin("Container.SetViewMode(51)")
	
def lista_videos(url):
	m3u = abrir_url(url).splitlines()
	for x in range(0,len(m3u)):
		if m3u[x].startswith('#EXTINF:'): 
			name = m3u[x].replace("\r","").replace("\n","").split(',')[1]
			addLink(name,m3u[x+1].replace('rtmp://$OPT:rtmp-raw=',''),artfolder + "movie.png")
	xbmc.executebuiltin("Container.SetViewMode(51)")
	
def lista_videos2():
	lista = abrir_url("https://dl.dropboxusercontent.com/s/h6ln6hb8l0hl4wo/userbouquet.ilu_xxx_adult.tv?dl=1&token_hash=AAGXNUUoQs_6kNFrZzSEo8OQjVwKSQcIrsgVM4VbsORgew&expiry=1400359776").splitlines()
	for x in range(0,len(lista)):
		if "#DESCRIPTION: " in lista[x]:
			name = lista[x].replace("#DESCRIPTION: ","").replace("\r","").replace("\n","")
			addLink(name,lista[x-1].replace('rtmp://$OPT:rtmp-raw=','').replace("#SERVICE 4097:0:1:0:0:0:0:0:0:0:","").replace("%3a",":").replace("...",""),artfolder + "movie.png")
	xbmc.executebuiltin("Container.SetViewMode(51)")
			
###############################################################
#CANAIS

'''
FONTES
http://tvmaniabg.com/category/18/
http://www.widih.org/tv-channel/all/adult
http://verdirectotv.com/
http://www.tvtuga.org/
http://live-cricketbd.blogspot.pt/p/blog-page_12.html
http://tvxat.org/tv-online/adulto/
http://tutvgratis.tv/
http://tvxlive.blogspot.pt/p/live-channels.html   http://tvxlive.ml/
http://www.portalzuca.net/canais/canal5.html   ---  Canal HOT
-http://www.lovetv.ml/
-http://peontv.com/
http://megatube.eu/
http://ero-tv.org/
http://www.hd-porn.tv/
http://torrent-tv.ru/
http://www.funmastii.com/search/label/Live%20Adult%20TV
'''

def brazzers_tv(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["Widih",'Torrent-TV'])
	if index==0: 
		#streamurl=widih_resolver("http://www.widih.org/watch-tv/1731/brazzers-18+live+tv+streaming")
		streamurl=widih_resolver("http://www.widih.org/watch-tv/5621/brazzers-tv-18-live-tv-streaming")
	elif index==1:
		ace = ttv_resolver(name)
		acestream(name,ace,iconimage)
		return
	else: return
	play(name,streamurl,iconimage)
	
def brasileirinhas(name,iconimage):
	url = "http://livestreamcast.org/embed.php?c=brasileirinhas"
	streamurl = livestreamcast_resolver(url)
	play(name,streamurl,iconimage)
	
def sexyhot(name,iconimage):
	url = "http://livestreamcast.org/embed.php?c=sexhothd"
	streamurl = livestreamcast_resolver(url)
	play(name,streamurl,iconimage)
	
def playboy(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["Livestreamcast","ponlatv", "TVtuga","ero-tv","TVxLive",'Torrent-TV'])
	if index == 0:
		url = "http://livestreamcast.org/embed.php?c=pboytv"
		streamurl = livestreamcast_resolver(url)
	elif index == 1:
		url = "http://verdirectotv.com/canales/playboy.html"
		streamurl = ponlatv_resolver(url)
	elif index == 2:
		url= "http://www.tvtuga.org/playboy-tv/"
		streamurl = tvtuga_resolver(url)
	elif index == 3:
		url= "http://ero-tv.org/playboytv_live/"
		streamurl = ero_tv_resolver(url)
	elif index==4:
		url = 'http://tvxlive.blogspot.pt/2014/11/playboyhd-19-hd.html'
		streamurl = tvxlive_resolver(url)
	elif index==5:
		ace = ttv_resolver(name)
		acestream(name,ace,iconimage)
		return
	else: return
	play(name,streamurl,iconimage)
	
def playboy_hd(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2007), ["Playboy HD 1", "Playboy HD 2", "Playboy HD 3", "Playboy HD 4", "Playboy HD 5"])
	if index == -1: return
	url = "http://livestreamcast.org/embed.php?c=playboyhd00" + str(index+1)
	streamurl = livestreamcast_resolver(url)
	play(name+' '+str(index+1),streamurl,iconimage)
	
def penthouse(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["ero-tv",'Torrent-TV'])
	if index==1:
		url = 'http://ero-tv.org/penthouse_online/'
		streamurl = ero_tv_resolver(url)
	elif index==2:
		ace = ttv_resolver(name)
		acestream(name,ace,iconimage)
		return
	else: return
	play(name,streamurl,iconimage)
	
def hot(name,iconimage):
	try:
		from bla import bla
		index = xbmcgui.Dialog().select(traducao(2006), ["portalzuca",bla.hot_s()])
	except: index = 0
	if index==0: 
		try:
			codigo_fonte = abrir_url('http://www.portalzuca.net/canais/canal5.html')
			file = re.compile("file='(.+?)'").findall(codigo_fonte)[0]
			link = 'http://abcast.biz/zuca.php?file=' + file 
			streamurl = abcast_resolver(link)
		except:
			xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
			return
	elif index==1:
		try:
			streamurl = bla.hot()
			if not streamurl: return 
		except: return
	else: return
	play(name,streamurl,iconimage)
	
def hustlerhd(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["ponlatv", "Torrent-TV"])
	if index == 0:
		url = "http://verdirectotv.com/canales/hustlertv.html"
		streamurl = ponlatv_resolver(url)
	elif index == 1:
		ace = ttv_resolver(name)
		acestream(name,ace,iconimage)
		return
	else: return
	play(name,streamurl,iconimage)
	
def viki_enjoy_premium(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["Widih", "ero-tv"])
	if index == 0:
		url = "http://www.widih.org/watch-tv/975/viki-enjoy-premium-hd%20live%20tv%20streaming"
		streamurl=widih_resolver(url)
	elif index == 1:
		url = "http://ero-tv.org/dorceltv_live/"
		streamurl=ero_tv_resolver(url)
	else: return
	play(name,streamurl,iconimage)
	
def vietsextv(name,iconimage):
	url = "http://www.tvtuga.org/viki-enjoy-premium/"
	streamurl = tvtuga_resolver(url)
	play(name,streamurl,iconimage)
	
def bella_club(name,iconimage):
	url = "http://live-cricketbd.blogspot.pt/2014/03/bellaclub.html"
	streamurl = livectv_resolver(url)
	play(name,streamurl,iconimage)
	
def bella_club2(name,iconimage):
	url = "http://live-cricketbd.blogspot.pt/2014/03/bella-club-2-18.html"
	streamurl = livectv_resolver(url)
	play(name,streamurl,iconimage)
	
def butgo(name,iconimage):
	url = "http://www.widih.org/watch-tv/1404/but-go-hd+live+tv+streaming"
	streamurl=widih_resolver(url)
	play(name,streamurl,iconimage)
	
def filthon_adult(name,iconimage):
	streamurl=widih_resolver("http://www.widih.org/watch-tv/3461/filthon-adult+live+tv+streaming")
	play(name,streamurl,iconimage)
	
def filthon_adult_fetish(name,iconimage):
	streamurl=widih_resolver("http://www.widih.org/watch-tv/2040/filthon-adult-fetish+live+tv+streaming")
	play(name,streamurl,iconimage)
	
def xxl(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["Widih", "ero-tv",'Torrent-TV'])
	if index==0: streamurl=widih_m3u("http://www.widih.org/watch-tv/4257/xxl-18+live+tv+streaming")
	elif index==1: streamurl = ero_tv_resolver('http://ero-tv.org/xxl-tv-live/')
	elif index==2:
		ace = ttv_resolver(name)
		acestream(name,ace,iconimage)
		return
	else: return
	play(name,streamurl,iconimage)
	
def french_lover(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["Widih",'TV Mania bg'])
	if index==0: streamurl=widih_resolver("http://www.widih.org/watch-tv/2400/french-lover+live+tv+streaming")
	elif index==1: streamurl=tvmaniabg_resolver('http://tvmaniabg.com/french-lover-tv/')
	else: return
	play(name,streamurl,iconimage)
	
def dorcel_tv(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["Widih",'Ero-TV'])
	if index==0:streamurl=widih_m3u("http://www.widih.org/watch-tv/1746/dorcel-tv-18+live+tv+streaming")
	elif index==1:streamurl=ero_tv_resolver('http://ero-tv.org/dorceltv_live/')
	else: return
	play(name,streamurl,iconimage)
	
def ipuretv(name,iconimage):
	m3u8=widih_m3u("http://www.widih.org/watch-tv/1722/ipure-tv-hd+live+tv+streaming")
	play(name,m3u8,iconimage)
	
def private(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["Livestreamcast", "ero-tv"])
	if index==0: streamurl=livestreamcast_resolver("http://livestreamcast.org/embed.php?c=privatee&vw=100%&vh=100%")
	elif index==1: streamurl = ero_tv_resolver('http://ero-tv.org/hallo-tv_online/')
	else: return
	play(name,streamurl,iconimage)
	
def private_gold(name,iconimage):
	url="http://tutvgratis.tv/adultos/private-gold"
	streamurl = tutv_resolver(url)
	play(name,streamurl,iconimage)
	
def venus(name,iconimage):
	url="http://tutvgratis.tv/adultos/venus/"
	streamurl = tutv_resolver(url)
	play(name,streamurl,iconimage)
	
def xdesire(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["TVxLive", "Torrent-TV",'Widih'])
	if index==0: streamurl = tvxlive_resolver("http://tvxlive.blogspot.pt/2014/07/daring.html")
	elif index==1:
		ace = ttv_resolver(name)
		acestream(name,ace,iconimage)
		return
	elif index==2: streamurl=widih_resolver('http://www.widih.org/watch-tv/1800/x-desire+live+tv+streaming')
	else: return
	play(name,streamurl,iconimage)
	
def hustler_blue(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["TVxLive", "Torrent-TV", 'Widih'])
	if index==0:
		streamurl = tvxlive_resolver("http://tvxlive.blogspot.pt/2014/09/blue-hustler.html")
		play(name,streamurl,iconimage)
	elif index==1:
		ace = ttv_resolver(name)
		acestream(name,ace,iconimage)
	elif index == 2:
		streamurl = widih_resolver('http://www.widih.org/watch-tv/5110/blue-hustler-live-tv-streaming')
		play(name,streamurl,iconimage)
	else: return

def olala(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["TVxLive", "Torrent-TV", 'Widih'])
	if index==0:
		streamurl = tvxlive_resolver("http://tvxlive.blogspot.pt/2014/07/o-la-la-18.html")
		play(name,streamurl,iconimage)
	elif index==1:
		ace = ttv_resolver(name)
		acestream(name,ace,iconimage)
	elif index == 2:
		streamurl = widih_resolver('http://www.widih.org/watch-tv/1975/o-lala-18-live-tv-streaming')
		play(name,streamurl,iconimage)
	else: return
	
def eroxxx(name,iconimage):
	streamurl = tvxlive_resolver("http://tvxlive.blogspot.pt/2014/07/eroxx-hd-18.html")
	play(name,streamurl,iconimage)
	
def amateritv(name,iconimage):
	try:
		url = "http://www.amateri.cz/?a=tv"
		streamurl = re.compile('"src" value="(.+?)">').findall(abrir_url(url))[0]
		play(name,streamurl,iconimage)
	except: xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
	
def russiannights(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["Widih","ero-tv"])
	if index==0: streamurl=widih_resolver("http://www.widih.org/watch-tv/1880/ruskaja-noc-russian-nights-18+live+tv+streaming")
	elif index==1: streamurl = ero_tv_resolver('http://ero-tv.org/russian_night_online/')
	else: return
	play(name,streamurl,iconimage)
	
def hustlertv(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["Livestreamcast","Widih","Torrent-TV"])
	if index==0: streamurl = livestreamcast_resolver("http://livestreamcast.org/embed.php?c=hustlerr&vw=100%&vh=100%")
	elif index==1: streamurl = widih_resolver('http://www.widih.org/watch-tv/5610/hustler-18-live-tv-streaming')
	elif index==2:
		ace = ttv_resolver(name)
		acestream(name,ace,iconimage)
		return
	else: return
	play(name,streamurl,iconimage)
	
def sexzonehd(name,iconimage):
	streamurl = livestreamcast_resolver("http://livestreamcast.org/embed.php?c=sexzonehd&vh=100%&vw=100%")
	play(name,streamurl,iconimage)
	
def redlighthd(name,iconimage):
	streamurl=ero_tv_resolver('http://ero-tv.org/redlight_online/')
	play(name,streamurl,iconimage)
	
def hallotv(name,iconimage):
	streamurl=ero_tv_resolver('http://ero-tv.org/hallo-tv_online/')
	play(name,streamurl,iconimage)
	
def platinum_tv(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ["ero-tv",'Widih','Torrent-TV'])
	if index==0: streamurl=ero_tv_resolver('http://ero-tv.org/platinum_tv_online/')
	elif index==1: streamurl = widih_resolver('http://www.widih.org/watch-tv/5773/platinum-18-live-tv-streaming')
	elif index==2:
		ace = ttv_resolver(name)
		acestream(name,ace,iconimage)
		return
	else: return
	play(name,streamurl,iconimage)
	
def filthon_gay(name,iconimage):
	streamurl = 'rtmp://live190.la3.origin.filmon.com:8086/live/246.high.stream'
	play(name,streamurl,iconimage)
	
def sexprive(name,iconimage):
	streamurl=ero_tv_resolver('http://ero-tv.org/brasileirinhas_tv_online/')
	play(name,streamurl,iconimage)
	
def nightclub(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ['Widih'])
	if index==0: streamurl=widih_resolver('http://id.widih.org/watch-tv/1873/nightclub-%D0%BD%D0%BE%D1%87%D0%BD%D0%BE%D0%B9-%D0%BA%D0%BB%D1%83%D0%B1+live+tv+streaming')
	else: return
	play(name,streamurl,iconimage)
	
def temptationtv(name,iconimage):
	#index = xbmcgui.Dialog().select(traducao(2006), ['Widih'])
	streamurl=widih_resolver('http://id.widih.org/watch-tv/1697/temptation-tv-%D0%B8%D1%81%D0%BA%D1%83%D1%88%D0%B5%D0%BD%D0%B8%D0%B5-%D1%82%D0%B2+live+tv+streaming')
	play(name,streamurl,iconimage)
	
def sct(name,iconimage):
	#index = xbmcgui.Dialog().select(traducao(2006), ['hd-porn.tv',traducao(2005)+' 2'])
	streamurl = widih_resolver('http://www.widih.org/watch-tv/2955/sct-18-live-tv-streaming')
	play(name,streamurl,iconimage)

def redlight_premium(name,iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ['hd-porn.tv'])
	if index==0: 
		hdporn_resolver(name,'http://www.hd-porn.tv/redlight-premium_df7e4fee2.html',iconimage)
		return
	else: return
	play(name,streamurl,iconimage)
	
def gboys(name,iconimage):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	try:
		url = 'http://g-boys.tk/'
		streamurl = re.compile("Link for live stream: <a href='(.+?)'").findall(abrir_url(url))[0]
		play(name,streamurl,iconimage)
	except: xbmcgui.Dialog().ok(traducao(2010), traducao(2011))

def bluebird(name,iconimage):
	streamurl = firestormmedia_resolver('http://api.firestormmedia.tv/iptv/iframes/player/?type=133&affid=1738889&channelName=Bluebird+1')
	play(name,streamurl,iconimage)
	
def star18(name,iconimage):
	streamurl = widih_resolver('http://www.widih.org/watch-tv/4764/xing-ying-star-%E6%98%9F%E9%A2%96star-18+live+tv+streaming')
	play(name,streamurl,iconimage)
	
def hotc(name,iconimage):
	streamurl = widih_resolver('http://www.widih.org/watch-tv/3399/hot-18+live+tv+streaming')
	play(name,streamurl,iconimage)
	
def paparazzo(name,iconimage):
	megatube_resolver(name,'http://megatube.eu/viewtopic.php?f=14&t=185',iconimage)
	
def dusk(name,iconimage):
	megatube_resolver(name,'http://megatube.eu/viewtopic.php?f=14&t=182',iconimage)
	
def erox(name,iconimage):
	megatube_resolver(name,'http://megatube.eu/viewtopic.php?f=14&t=180',iconimage)
	
def xxx1(name, iconimage):
	hdporn_resolver(name,'http://www.hd-porn.tv/tv.html',iconimage)
	
def xxx2(name, iconimage):
	streamurl = widih_resolver('http://www.widih.org/watch-tv/4257/anilos-adult-18-live-tv-streaming')
	play(name,streamurl,iconimage)
	
def bungabunga(name, iconimage):
	index = xbmcgui.Dialog().select(traducao(2006), ['Widih','Torrent-TV'])
	if index==0:
		streamurl = widih_resolver('http://www.widih.org/watch-tv/2489/bunga-bunga+live+tv+streaming')
		play(name,streamurl,iconimage)
	elif index==1:
		ace = ttv_resolver(name)
		acestream(name,ace,iconimage)
		return
	else: return
	
def satisfactionhd(name,iconimage):
	#streamurl = tvmaniabg_resolver('http://tvmaniabg.com/satisfaction-hd/')
	streamurl = widih_resolver('http://www.widih.org/watch-tv/2956/satisfaction-hd-live-tv-streaming')
	play(name,streamurl,iconimage)
	
def centoxcento(name, iconimage):
	streamurl = widih_resolver('http://www.widih.org/watch-tv/5772/centox-cento-18-live-tv-streaming')
	play(name,streamurl,iconimage)
	
def exoticatv(name, iconimage):
	streamurl = widih_resolver('http://www.widih.org/watch-tv/5775/exotica-plus-18-live-tv-streaming')
	play(name,streamurl,iconimage)
	
def pinkotv(name, iconimage):
	streamurl = widih_resolver('http://www.widih.org/watch-tv/5774/pink-o-18-live-tv-streaming')
	play(name,streamurl,iconimage)
	
########################################################################
#RESOLVERS
def livesteam_resolver(url):
	chid = url.split('/')[-1]
	m3u8 = 'http://x' + chid + 'x.api.channel.livestream.com/3.0/playlist.m3u8'
	rtsp = 'rtsp://mobilestr3.livestream.com/livestreamiphone/' + chid
	return rtsp

def tvmaniabg_resolver(url):
	try:
		html = abrir_url(url)
		file = re.compile("'file': '(.+?)'").findall(html)[0]
		return file
	except: pass
	xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
	return 'erro'
	
	
def ttv_resolver(name):
	try:
		mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
		m3u = abrir_url(ttv_api).splitlines()
		for x in range(0,len(m3u)):
			if re.search(name,m3u[x]) and m3u[x].startswith('#EXTINF:') and re.search('(Для взрослых)',m3u[x]): 
				return m3u[x+1]
	except: pass
	xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
	return 'erro'
	

def hdporn_resolver(name,url,iconimage):
	try:
		html = abrir_url(url)
		flashvars = re.compile('name="flashvars" value="(.+?)"').findall(html)[0] + '&'
		file = re.compile('file=(.+?)&').findall(flashvars)[0]
		streamurl = m3u8(file)
		play(name,streamurl,iconimage)
	except: xbmcgui.Dialog().ok(traducao(2010), traducao(2011))

'''
def hdporn_resolver(name,url,iconimage):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	try:
		id = re.compile('<input type="hidden" name="bin-rating-uniq_id" value="(.+?)">').findall(abrir_url(url))[0]
		ajax = 'http://www.hd-porn.tv/ajax.php?p=video&do=getplayer&vid='+id+'&aid=1&player=detail'
	except: 
		xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
		return
	try:
		flashvars = re.compile('flashvars="(.+?)"').findall(abrir_url(ajax))[0] + '&'
		file = re.compile('file=(.+?)&').findall(flashvars)[0]
		streamurl = m3u8(file)
		play(name,streamurl,iconimage)
		return
	except: pass
	try:
		iframe = re.compile('src="(.+?)"').findall(abrir_url(ajax))[0]
		ace = re.compile('this.loadPlayer\("(.+?)"').findall(abrir_url(iframe))[0]
		acestream(name,ace,iconimage)
		return
	except: pass
	xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
'''
	
def torrentv_ace(url):
	print abrir_url(url)
	return re.compile('this.loadPlayer\("(.+?)"').findall(abrir_url(url))[0]

def megatube_resolver(name,url,iconimage):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	try:
		embed = re.compile('<iframe src="(.+?)"').findall(abrir_url(url))[0]
		ip = embed.split('/')[2]
		headers = {'Host':ip,
				   'Connection':'keep-alive',
				   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				   'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
				   'Referer':url}
				   
		html = abrir_url_tommy(embed,headers)
		m3u = re.compile('<param name="MRL" value="(.+?)"').findall(html)[0]
		url_video = abrir_url(m3u).splitlines()[3]
		
		headers = {'Host':'megatube.eu',
				   'User-Agent':'VLC/2.1.5 LibVLC/2.1.5',
				   'Connection':'close',
				   'Range':'bytes=0-',
				   'Icy-MetaData':'1',
				   'Accept':'',
				   'Accept-Charset':''}
		
		mypath = os.path.join(pastaperfil,'temp.mp4')
		start = True
		with open(mypath, 'wb') as handle:
			response = requests.get(url_video, stream=True,headers=headers)
			if not response.ok: return
			i = 0
			liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
			player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
			for block in response.iter_content(1024):
				if not block: break
				handle.write(block)
				if i<2000: 
					i+=1
					if mensagemprogresso.iscanceled():
						break
				else:
					if start: 
						mensagemprogresso.close()
						player.play(mypath,liz)
						start = False
						j = 0
						while not player.isPlaying():
							if j == 30: break
							xbmc.sleep(100)
							j += 1
						continue
					if not player.isPlaying(): break
		while os.path.exists(mypath):
			try: os.remove(mypath)
			except: pass
	except: xbmcgui.Dialog().ok(traducao(2010), traducao(2011))

def firestormmedia_resolver(url):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	try:
		html = abrir_url(url)
		swf = re.compile('data="(.+?)"').findall(html)[0]
		config_url = re.compile('config_urls\[\"load_config\"\] \= \"(.+?)\"').findall(html)[0]
		html2 = abrir_url(config_url)
		
		servers = re.compile('servers="(.+?)"').findall(html2)
		s = []
		for server in servers:
			s.append(server.split(','))
		
		streamname = re.compile('streamName="(.+?)"').findall(html2)
		for i in range(0,len(streamname)):
			if i==0: streamname[i] = streamname[i].replace('_one','') + '1'
			else: streamname[i] = streamname[i].replace('_two','2').replace('_three','3').replace('_four','4')
		
		app = re.compile('application="(.+?)"').findall(html2)

		i = 0
		server_i = 0
		streamurl = 'rtmp://'+s[i][server_i]+'/'+app[i] + '/ playPath=' + streamname[i] + ' live=true swfVfy=true swfUrl=' + swf + ' pageUrl=' + url 
		return streamurl
	except: pass
	xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
	return 'erro'
	
def abcast_resolver(url):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	try:
		codigo_fonte = abrir_url(url)
		file =  re.compile('file=(.+?)&').findall(codigo_fonte)[0]
		rtmp =  re.compile('streamer=(.+?)&').findall(codigo_fonte)[0]
		swf =  'http://abcast.biz/' + re.compile('<object data="(.+?)"').findall(codigo_fonte)[0]
		#pageurl = url.replace(url.split('?')[0],'http://abcast.biz/embed.php')
		try: file = file.replace('.'+file.split('.')[-1],'')
		except: pass
		streamurl=rtmp + ' playPath=' + file  + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=true pageUrl='+url
		return streamurl
	except: pass
	xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
	return 'erro'	

def livectv_resolver(url):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	codigo_fonte = abrir_url(url)
	try:
		rtmp = re.compile('file: "(.+?)"').findall(codigo_fonte)[0]
		streamurl = rtmp + ' live=true swfVfy=1'
		return streamurl
	except: pass
	try:
		rtmp = re.compile("'file': '(.+?)'").findall(codigo_fonte)[0]
		streamurl = rtmp + ' live=true swfVfy=1'
		return streamurl
	except: pass
	xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
	return "erro"
		
def ero_tv_resolver(url):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	html = abrir_url(url)
	try:
		st = re.compile('st=(.+?)&').findall(html)[0]
		info = uppod.decode(abrir_url(uppod.decode(st)))
		try: stkey = re.compile('"stkey":"(.+?)"').findall(info)[0]
		except: stkey = ''
		rtmp_enc = re.compile('file=(.+?)"').findall(html)[0]
		file = uppod.decode(rtmp_enc.replace(stkey,''))
		if '.m3u8' in file: return m3u8(file)
		swf = re.compile('data="(.+?)"').findall(html)[0]
		streamurl=file + ' swfUrl=' + swf + ' swfVfy=1 live=1 pageUrl=' + url
		return streamurl
	except: pass
	try:
		file = re.compile('file=(.+?)"').findall(html)[0]
		if 'livestreamcast.org' in file:
			swf = "http://livestreamcast.org/jwplayer/jwplayer.flash.swf"
			streamurl = file + ' live=true swfVfy=1 swfUrl=' + swf 
			return streamurl.replace('  ',' ')
	except: pass
	try:
		file = re.compile('file: "(.+?)"').findall(html)[0]
		swf = "http://livestreamcast.org/jwplayer/jwplayer.flash.swf"
		streamurl = file + ' live=true swfVfy=1 swfUrl=' + swf 
		return streamurl
	except: pass
	xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
	return "erro"
		
def tvxlive_resolver(url):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	try:
		streamurl=re.compile('target="(.+?)"').findall(abrir_url(url))[0]
		return streamurl
	except: 
		xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
		return "erro"

def tutv_resolver(url):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	try:
		embed="http://tutvgratis.tv/embed/"+ re.compile('http://tutvgratis.tv/embed/(.+?)"').findall(abrir_url(url))[0]
		
		#code = urllib.unquote(re.compile("document.write\(unescape\('(.+?)'\)\)\;").findall(abrir_url(embed))[0])
		#url2 = re.compile('src="(.+?)"').findall(code)[0]
		#channelID = re.compile('channelid=(.+?)&').findall(url2)[0]
		
		channelID = re.compile('channelID:(.+?),').findall(abrir_url(embed))[0].replace(' ','')
		
		referer = 'http://tutvgratis.tv/embed/generaiframe?chid='+channelID+'&w=728&h=409'
		
		ref_data = {'Host':'tutvgratis.tv',
					'Connection':'keep-alive',
					'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
					'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
					'Referer': embed}
		
		code3=urllib.unquote(re.compile("document.write\(unescape\('(.+?)'\)\)\;").findall(abrir_url_tommy(referer,ref_data))[0])
		if 'ucaster.eu' in code3:
			ucaster_link = 'http://www.ucaster.eu/embedded/' + re.compile("channel='(.+?)'").findall(code3)[0] + '/1/600/430'
			streamurl = ucaster_resolver(ucaster_link,referer)
			return streamurl
		elif 'mips.tv' in code3:
			mipstv_link = 'http://www.mips.tv/embedplayer/' + re.compile("channel='(.+?)'").findall(code3)[0] + '/1/650/400'
			streamurl = mipstv_resolver(mipstv_link,referer)
			return streamurl
		elif 'shidurlive.com' in code3:
			shidurlive_link = re.compile("src='(.+?)'").findall(code3)[0]
			streamurl = shidurlive_resolver(shidurlive_link,referer)
			return streamurl
	except: pass
	xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
	return 'erro'
	
def shidurlive_resolver(embed, referer):
	ref_data = {'Host':'shidurlive.com',
				'Connection':'keep-alive',
				'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
				'Referer':referer}
				
	html= abrir_url_tommy(embed,ref_data)
	pageUrl = re.compile('src="(.+?)"').findall(html)[0]
	source = abrir_url_tommy(pageUrl,ref_data).replace('//so','')
	rtmp = re.compile("so.addVariable\('streamer', '(.+?)'").findall(source)[0]
	playPath = re.compile("so.addVariable\('file', unescape\('(.+?)'").findall(source)[0]
	playPath = urllib.unquote(playPath)
	swf = re.compile("new SWFObject\('(.+?)'").findall(source)[0]
	streamurl = rtmp + ' playPath=' + playPath + ' swfUrl=' + swf + ' pageUrl=' + pageUrl
	return streamurl

def mipstv_resolver(embed,referer):
	ref_data = {'Referer': referer,'User-Agent':user_agent}
	html= abrir_url_tommy(embed,ref_data)
	if re.search("The requested channel can't embedded on this domain name.",html):
		chname = re.compile("embedplayer/(.+?)/").findall(embed)[0]
		source='http://www.mips.tv/' + chname
		ref_data = {'Referer': source,'User-Agent':user_agent}
		html= abrir_url_tommy(embed,ref_data)
	####
	swf=re.compile('SWFObject.+?"(.+?)",').findall(html)[0]
	flashvars=re.compile("so.addParam.+?'FlashVars'.+?'(.+?)'").findall(html)[0]
	nocanal=re.compile("&s=(.+?)&").findall(flashvars)[0]
	chid=re.compile("id=(.+?)&").findall(html)[0]
	link=abrir_url('http://www.mips.tv:1935/loadbalancer')
	rtmp='rtmp://'+re.compile(".*redirect=([\.\d]+).*").findall(link)[0]+'/live'
	streamurl= rtmp + ' playPath=' + nocanal + '?id=' + chid + ' swfVfy=1 live=true timeout=15 conn=S:OK swfUrl=http://www.mips.tv' + swf + ' pageUrl=' + embed
	return streamurl
	
	
def ucaster_resolver(url,referer):
	try:
		ref_data = {'Referer': referer,'User-Agent':user_agent}
		html= abrir_url_tommy(url,ref_data)
		swf = 'http://www.ucaster.eu'+re.compile('SWFObject\("(.+?)"').findall(html)[0]
		ch = re.compile("so.addParam\('FlashVars', 'id=(.+?)&s=(.+?)&").findall(html)[0]
		playpath = "%s?id=%s" % (ch[1],ch[0])
		rtmp='rtmp://'+re.compile(".*redirect=([\.\d]+).*").findall(abrir_url('http://www.ucaster.eu:1935/loadbalancer'))[0]+'/live'
		streamurl=rtmp + ' playPath=' + playpath + ' swfVfy=1 conn=S:OK live=true swfUrl=' + swf + ' pageUrl=' + url
		return streamurl
	except:
		xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
		return "erro"

def widih_m3u(url):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	try:
		m3u=re.compile("'file': '(.+?)'").findall(abrir_url(url))[0]
		return m3u8(m3u)
	except:
		xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
		return 'erro'
	
def widih_resolver(url):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	codigo_fonte = abrir_url(url)
	try:
		rtmp=re.compile("'file': '(.+?)'").findall(codigo_fonte)[0]
		if "m3u8" in rtmp: return widih_m3u(url)
		swf = re.compile("'flash', src: '(.+?)'").findall(codigo_fonte)[0]
		streamurl=rtmp + ' swfUrl=' + swf + ' swfVfy=1 live=1 pageUrl=' + url
	except:
		try: streamurl="http://"+re.compile('target="http://(.+?)"').findall(codigo_fonte)[0]
		except: 
			xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
			return "erro"
	return streamurl

def ponlatv_resolver(url):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	referer = re.compile('src="(.+?)"></iframe>').findall(abrir_url(url))[0]
	ref2 = re.compile('src="(.+?)"></iframe>').findall(abrir_url(referer))[0]
	try:
		link="http://www.9stream.com/"+re.compile('src="http://www.9stream.com/(.+?)"').findall(abrir_url(ref2))[0]
		return ninestream(link,referer)
	except: 
		try:
			headers = {'Host':'tv.verdirectotv.org',
					   'Connection':'keep-alive',
					   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
					   'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
					   'Referer':ref2}
					   
			ref3 = "http://tv.verdirectotv.org/" + re.compile('src="http://tv.verdirectotv.org/(.+?)"').findall(abrir_url(ref2))[0]
			ref4 = re.compile('src="(.+?)"').findall(requests.get(ref3,headers=headers).text)[0]
				   
			html = requests.get(ref4,headers=headers).text
			import base64
			playPath = base64.b64decode(re.compile('id="ssx1" value="(.+?)"').findall(html)[0])
			rtmp = base64.b64decode(re.compile('id="ssx4" value="(.+?)"').findall(html)[0])
			
			streamurl = rtmp + '/' + playPath + ' swfUrl=http://www.businessapp1.pw/jwplayer5/addplayer/jwplayer.flash.swf pageUrl=' + ref4
			return streamurl
		except: pass
	xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
	return 'erro'
	
def ninestream(url,referer):
	embed_url = re.compile("src='(.+?)'").findall(abrir_url(url))[0]
	ref_data = {'Referer':referer,'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36','Host': 'www.9stream.com','Connection': 'Keep-Alive'}
	embed = abrir_url_tommy(embed_url,ref_data)
	if re.search('Page protected by ionCube',embed): embed = ioncube.open(embed)
	rtmp = re.compile('\'streamer\': "(.+?)"').findall(embed)[0].replace("\\","")
	if rtmp[-1] != "/": rtmp = rtmp + "/"
	playpath = re.compile("'file': '(.+?)'").findall(embed)[0]
	swf = re.compile("'flash', src: '(.+?)'").findall(embed)[0]
	urltoken = re.compile('getJSON\("(.+?)"').findall(embed)[0]
	token = re.compile('"token":"(.+?)"').findall(abrir_url_tommy(urltoken,ref_data))[0]
	streamurl=rtmp + playpath + ' swfUrl=' + swf + ' token='+ token +' swfVfy=1 live=1 pageUrl=' + embed_url
	return streamurl
	
def tvtuga_resolver(url):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	codigo_fonte = abrir_url(url)
	try: rtmp = "rtmp://" + re.compile('flashvars="file=rtmp://(.+?)"').findall(codigo_fonte)[0].replace("&#038;","").replace("id=","").replace("&amp;","").replace("autostart=true","")
	except:
		try:rtmp = "rtmpe://" + re.compile('flashvars="file=rtmpe://(.+?)"').findall(codigo_fonte)[0].replace("&#038;","").replace("id=","").replace("&amp;","").replace("autostart=true","")
		except: 
			xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
			return 'erro'
	swf = "http://www.tvtuga.org/asx/player.swf"
	streamurl = rtmp + ' live=true swfVfy=1 swfUrl=' + swf + ' pageUrl=' + url
	return streamurl
	
def livestreamcast_resolver(url):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	codigo_fonte = abrir_url(url)
	try:rtmp = "rtmp://" + re.compile('file: "rtmp://(.+?)"').findall(codigo_fonte)[0]
	except:
		try: return "http://" + re.compile('file: "http://(.+?)"').findall(codigo_fonte)[0]
		except:
			xbmcgui.Dialog().ok(traducao(2010), traducao(2011))
			return "erro"
	swf = "http://livestreamcast.org/jwplayer/jwplayer.flash.swf"
	streamurl = rtmp + ' live=true swfVfy=1 swfUrl=' + swf 
	return streamurl
	
###################################################################################
#FUNCOES
def acestream(name,something,iconimage):
	#plugin://plugin.video.p2p-streams/?url=_some_hash&mode=1&name=acestream+title
	#plugin://plugin.video.p2p-streams/?url=acestream://_some_hash&mode=1&name=acestream+title
	#plugin://plugin.video.p2p-streams/?url=http://something.torrent&mode=1&name=acestream+title
	#plugin://plugin.video.p2p-streams/?url=http://something.acelive&mode=1&name=acestream+title
	if something == 'erro': return
	if not xbmc.getCondVisibility('System.HasAddon(plugin.video.p2p-streams)'):
		xbmcgui.Dialog().ok(traducao(2010), traducao(2076),'http://forum.kodi.tv/showthread.php?tid=201894')
		return
	xbmc.executebuiltin('RunPlugin(plugin://plugin.video.p2p-streams/?url='+something+'&mode=1&name='+name+'&iconimage='+iconimage+')')

def headers_str(headers):
	start = True
	headers_str = ''
	for k,v in headers.items():
		if start:
			headers_str += '|'+urllib.quote_plus(k)+'='+urllib.quote_plus(v)
			start = False
		else: headers_str += '&'+urllib.quote_plus(k)+'='+urllib.quote_plus(v)
	return headers_str
	
def get_mediafire_url(url):
	mensagemprogresso.create('Adults TV', traducao(2008),traducao(2009))
	mensagemprogresso.update(0)
	url = url.replace('/view/','/download/')
	m_id = url.split('/')[-2]
	post_url = 'http://www.mediafire.com/?' + m_id
	codigo_fonte = google_captcha(url,post_url)
	mensagemprogresso.close()
	try: return re.compile('kNO = "(.+?)"').findall(codigo_fonte)[0]
	except: return "erro"
	
def google_captcha(url,post_url):
	import random
	from t0mm0.common.net import Net
	net = Net()
	
	html = abrir_url(url).replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
	if not 'recaptcha_challenge_field' in html: return html
	
	k = re.compile('http://www.google.com/recaptcha/api/noscript\?k\=(.+?)"').findall(html)[0]
	challenge = "http://www.google.com/recaptcha/api/challenge?k=%s&ajax=1&cahcestop=%.17f" % (k, random.random())
	challengehtml = abrir_url(challenge)
	challengeToken = re.compile("challenge : '(.+?)'").findall(challengehtml)[0]
	captcha_url = 'http://www.google.com/recaptcha/api/image?c=' + challengeToken
	captcha_img = os.path.join(pastaperfil, "captcha.jpg")
	open(captcha_img, 'wb').write( net.http_GET(captcha_url).content)
	solver = InputWindow(captcha=captcha_img)
	try:os.remove(captcha_img)
	except: pass
	puzzle = solver.get()
	if puzzle:
		form_values = {'recaptcha_challenge_field':challengeToken,'recaptcha_response_field':puzzle}
		html = net.http_POST(post_url, form_data=form_values).content
		if 'recaptcha_challenge_field' in html: 
			xbmcgui.Dialog().ok(traducao(2010), traducao(2069))
			return 'erro'
		return html
	return 'erro'
	
class InputWindow(xbmcgui.WindowDialog):# Cheers to Bastardsmkr code already done in Putlocker PRO resolver.
    
    def __init__(self, *args, **kwargs):
        self.cptloc = kwargs.get('captcha')
        xposition = 425
        yposition = 5
        hposition = 135
        wposition = 405
        self.img = xbmcgui.ControlImage(xposition,yposition,wposition,hposition,self.cptloc)
        self.addControl(self.img)
        self.kbd = xbmc.Keyboard('','Captcha:')

    def get(self):
        self.show()
        time.sleep(3)
        self.kbd.doModal()
        if (self.kbd.isConfirmed()):
            text = self.kbd.getText()
            self.close()
            return text
        else:
            self.close()
            sys.exit(0)
        self.close()
        return False
	
def check_version():
	try:
		codigo_fonte=abrir_url('https://anonymousrepo.svn.codeplex.com/svn/anonymous-repo-adults/plugin.video.adultstv/addon.xml')
		match=re.compile('version="(.+?)"').findall(codigo_fonte)[1]
	except: match='error'
	if match=='error': xbmc.executebuiltin('Notification("   '+traducao(2059)+'","   '+traducao(2060)+'",3000,"'+artfolder+'version.png")')
	elif match!=selfAddon.getAddonInfo('version'): xbmc.executebuiltin('Notification("   '+traducao(2061)+' ('+match+')","   '+traducao(2062)+'",3000,"'+artfolder+'version.png")')
	
def first_run():
	if not xbmcvfs.exists(pastaperfil): xbmcvfs.mkdir(pastaperfil)
	if not os.path.exists(os.path.join(pastaperfil,"passwd.txt")):
		savefile("passwd.txt","<flag='false'>")
	
def password():
	if selfAddon.getSetting('vista') == '0':
		if pass_status() == False: addDir(traducao(2013),'-',100,artfolder + 'password.png',False)
		else: addDir(traducao(2014),'-',100,artfolder + 'password.png',False)
	else:
		if pass_status() == False: addDir(traducao(2013),'-',100,artfolder + 'password_m.png',False)
		else: addDir(traducao(2014),'-',100,artfolder + 'password_m.png',False)
	
def pass_status():
	try:
		if re.compile("flag='(.+?)'").findall(openfile("passwd.txt"))[0] == "true": return True
	except: return True
	return False

def check_pass():
	if pass_status() == False: return
	try: check = re.compile("password='(.+?)'").findall(openfile("passwd.txt"))[0]
	except: sys.exit(0)
	keyb = xbmc.Keyboard('', traducao(2015)) 
	keyb.setHiddenInput(True)
	keyb.doModal()
	if (keyb.isConfirmed()): password = keyb.getText()
	else: sys.exit(0)
	if password != check:
		xbmcgui.Dialog().ok(traducao(2010), traducao(2016))
		sys.exit(0)
	
def change_pass_status():
	if pass_status() == False:
		keyb = xbmc.Keyboard('', traducao(2017)) 
		keyb.setHiddenInput(True)
		keyb.doModal()
		if (keyb.isConfirmed()): password = keyb.getText()
		else: return
		if password == '' or "'" in password:
			xbmcgui.Dialog().ok(traducao(2010), traducao(2018))
			return
		savefile("passwd.txt","<flag='true' password='%s'>" % password)
	else: 
		check = re.compile("password='(.+?)'").findall(openfile("passwd.txt"))[0]
		keyb = xbmc.Keyboard('', traducao(2015)) 
		keyb.setHiddenInput(True)
		keyb.doModal()
		if (keyb.isConfirmed()): password = keyb.getText()
		else: return
		if password == '':
			xbmcgui.Dialog().ok(traducao(2010), traducao(2018))
			return
		if password == check: savefile("passwd.txt","<flag='false'>")
		else: xbmcgui.Dialog().ok(traducao(2010), traducao(2016))	
	xbmc.executebuiltin("Container.Refresh")
	
def savefile(filename, contents,pastafinal=pastaperfil):
	try:
		destination = os.path.join(pastafinal,filename)
		fh = open(destination, 'wb')
		fh.write(contents)  
		fh.close()
	except: print "falhou a escrever txt"
	
def openfile(filename,pastafinal=pastaperfil):
	try:
		destination = os.path.join(pastafinal, filename)
		fh = open(destination, 'rb')
		contents=fh.read()
		fh.close()
		return contents
	except:
		print "Falhou a abrir txt"
		return None

def play(name,streamurl,iconimage = "DefaultVideo.png"):
	#streamurl += ' timeout=15'
	liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	'''
	liz.setInfo('video', {'Title': name })
	liz.setProperty('IsPlayable', 'true')
	liz.setPath(path=streamurl)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,liz)
	'''
	player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	player.play(streamurl,liz)
	
def abrir_url(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link
	except: return 'erro'

def addLink(name,url,iconimage,total=1):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,totalItems=total)
	return ok

def addDir(name,url,mode,iconimage,pasta = True,total=1,offset=1):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&offset="+str(offset)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok

############################################################################################################
#                                               GET PARAMS                                                 #
############################################################################################################
              
def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1] 
	return param

params=get_params()
url=None
name=None
mode=None
iconimage=None
offset=None
letra=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: offset=int(params["offset"])
except: pass
try: letra=urllib.unquote_plus(params["letra"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)
print "Offset: "+str(offset)
print "Letra: "+str(letra)

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################
	
if mode==None or url==None or len(url)<1: 
	first_run()
	check_pass()
	check_version()
	if entra_canais == "false": CATEGORIES()
	else: canais()
elif mode==0: CATEGORIES()
elif mode==1: listas()
elif mode==2: lista_videos(url)
elif mode==3: lista_videos2()
elif mode==21: canais()
elif mode==22: 
	selfAddon.openSettings()
	xbmcgui.Dialog().ok(traducao(2070), traducao(2071))
elif mode==103: lista_bla(url,name)
elif mode==104: lista_videos3(url)
elif mode==100: change_pass_status()
elif mode==101: videos()
elif mode==105: revistas(offset)
elif mode==106: 
	down_url = get_mediafire_url(url)
	if down_url != 'erro': 
		try: pdf.pdf_read(name,down_url,True)
		except: pass
elif mode==107: acestream(name,url,iconimage)
elif mode==108: tv_sv()
elif mode==109: ttv()
elif mode==110: abelhas()
#CANAIS
elif mode==4: brazzers_tv(name,iconimage)
elif mode==5: brasileirinhas(name,iconimage)
elif mode==6: sexyhot(name,iconimage)
elif mode==7: playboy(name,iconimage)
elif mode==8: playboy_hd(name,iconimage)
elif mode==9: penthouse(name,iconimage)
elif mode==10: hot(name,iconimage)
elif mode==11: hustlerhd(name,iconimage)
elif mode==12: viki_enjoy_premium(name,iconimage)
elif mode==13: vietsextv(name,iconimage)
elif mode==14: bella_club(name,iconimage)
elif mode==15: bella_club2(name,iconimage)
elif mode==16: butgo(name,iconimage)
elif mode==17: filthon_adult(name,iconimage)
elif mode==18: filthon_adult_fetish(name,iconimage)
elif mode==19: xxl(name,iconimage)
elif mode==20: french_lover(name,iconimage)
elif mode==23: dorcel_tv(name,iconimage)
elif mode==24: ipuretv(name,iconimage)
elif mode==25: private(name,iconimage)
elif mode==26: private_gold(name,iconimage)
elif mode==27: venus(name,iconimage)
elif mode==28: xdesire(name,iconimage)
elif mode==29: hustler_blue(name,iconimage)
elif mode==30: olala(name,iconimage)
elif mode==31: eroxxx(name,iconimage)
elif mode==32: amateritv(name,iconimage)
elif mode==33: russiannights(name,iconimage)
elif mode==34: hustlertv(name,iconimage)
elif mode==35: sexzonehd(name,iconimage)
elif mode==36: redlighthd(name,iconimage)
elif mode==37: hallotv(name,iconimage)
elif mode==38: platinum_tv(name,iconimage)
elif mode==39: filthon_gay(name,iconimage)
elif mode==40: sexprive(name,iconimage)
elif mode==41: nightclub(name,iconimage)
elif mode==42: temptationtv(name,iconimage)
elif mode==43: sct(name,iconimage)
elif mode==44: redlight_premium(name,iconimage)
elif mode==45: gboys(name,iconimage)
elif mode==46: bluebird(name,iconimage)
elif mode==47: star18(name,iconimage)
elif mode==48: hotc(name,iconimage)
elif mode==49: paparazzo(name,iconimage)
elif mode==50: erox(name,iconimage)
elif mode==51: dusk(name,iconimage)
elif mode==52: xxx1(name,iconimage)
elif mode==53: xxx2(name,iconimage)
elif mode==54: bungabunga(name,iconimage)
elif mode==55: satisfactionhd(name,iconimage)
elif mode==56: centoxcento(name, iconimage)
elif mode==57: exoticatv(name, iconimage)
elif mode==58: pinkotv(name, iconimage)
#Brazzers Videos
elif mode==200: brazzers.brazzers_menu()
elif mode==201: brazzers.listar_videos(url)
elif mode==202: brazzers.encontrar_fontes(name,url,iconimage)
elif mode==203: brazzers.pesquisa()
elif mode==204: brazzers.play_tv()
elif mode==205: brazzers.download(name,url)
elif mode==206: brazzers.selfAddon.openSettings()
elif mode==207: brazzers.cat()
#Free HD Porn
elif mode>=300 and mode <=399:
	fhdp.mode(mode,name,url,iconimage)
#Stream XXX
elif mode==400: streamxxx.menu()
elif mode==402: streamxxx.listar_videos(url)
elif mode==401: streamxxx.listar_fontes(name,url,iconimage)
elif mode==403: streamxxx.pesquisa()
elif mode==404: streamxxx.clips()
#Boa foda
elif mode==500: boaf.menu()
elif mode==501: boaf.recentes(url)
elif mode==502: boaf.listar_fontes(name,url,iconimage)
elif mode==503: boaf.listar_videos(url)
elif mode==504: boaf.pesquisa()
elif mode==505: boaf.pornstars()
elif mode==506: boaf.listar_pornstars(name,url,offset,letra)
elif mode==507: boaf.cat()
elif mode==508: boaf.estudios()
elif mode==509: boaf.listar_estudios(url)
elif mode==510: boaf.listar_estudios2(offset)
elif mode==511: boaf.videos_recentes(offset)
elif mode==512: boaf.listar_videos2(url,offset)
elif mode==513: boaf.settings()
elif mode==514: boaf.listar_videos_pornstars(url,offset)
elif mode==515: boaf.listar_videos_estudios(url,offset)
#Ero-tik
elif mode>=600 and mode <= 699: 
	erotik.mode(mode,name,url,iconimage,offset)
elif mode>=700 and mode <= 799: 
	xvideos.mode(mode,name,url,iconimage,offset)
elif mode>=800 and mode <= 899: 
	bla_video(mode,name,url,iconimage)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
