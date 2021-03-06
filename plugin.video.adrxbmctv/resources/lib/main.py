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
from utilis import *


h = HTMLParser.HTMLParser()

addon_id = 'plugin.video.adrxbmctv'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
user_agent = 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36'
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
if xbmc.getCondVisibility('system.platform.windows'): pastaperfil = pastaperfil.replace('\\','/')
mensagemprogresso = xbmcgui.DialogProgress()
entra_canais = selfAddon.getSetting('entra_canais')

def traducao(texto):
	return selfAddon.getLocalizedString(texto).encode('utf-8')

#MENUS############################################

def CATEGORIES():
	if selfAddon.getSetting('vista') == '0':
		addDir('AdrXbmc (Abelhas)','-',100,artfolder + 'logo.png', pasta=False)
		addDir('Novelas','-',170,artfolder + 'novelas.png', pasta=False)
		addDir('Teatro Tv','-',180,artfolder + 'teatrotv.png', pasta=False)
		addDir('Filmes','-',110,artfolder + 'filmes.png', pasta=False)
		addDir('Filmes HD','-',111,artfolder + 'filmeshd.png', pasta=False)
		addDir('Filmes UHD','-',112,artfolder + 'filmesuhd.png', pasta=False)
		addDir('Filmes Pt','-',113,artfolder + 'filmespt.png', pasta=False)
		addDir('Filmes Pl','-',114,artfolder + 'filmespl.png', pasta=False)
		addDir('Filmes 3D','-',115,artfolder + 'filmes3d.png', pasta=False)
		addDir('Series','-',120,artfolder + 'series.png', pasta=False)
		addDir('Series Completas','-',121,artfolder + 'seriescompletas.png', pasta=False)
		addDir('Documentarios','-',130,artfolder + 'documentarios.png', pasta=False)
		addDir('Fitness','-',140,artfolder + 'fitness.png', pasta=False)
		addDir('Humor','-',150,artfolder + 'humor.png', pasta=False)
		addDir('Concertos','-',160,artfolder + 'concertos.png', pasta=False)
		
		
		if selfAddon.getSetting('pass') == "false": password()
	

	
def abelhas():
	addon = 'plugin.video.abelhas'
	if not xbmc.getCondVisibility('System.HasAddon('+addon+')'):
		xbmcgui.Dialog().ok(traducao(2010), traducao(2077))
		return
	
	url = urllib.quote_plus('http://abelhas.pt/adrxbmc')
	name = 'Ir para uma Abelha'
	xbmc.executebuiltin('XBMC.Container.Update(plugin://%s?mode=3&url=%s&name=%s)' % (addon, url,name))
	
def filmes():
	addon = 'plugin.video.abelhas'
	if not xbmc.getCondVisibility('System.HasAddon('+addon+')'):
		xbmcgui.Dialog().ok(traducao(2010), traducao(2077))
		return
	
	url = urllib.quote_plus('http://abelhas.pt/AdrXbmc/Filmes+*26+S*c3*a9ries/Filmes/SD')
	name = 'Ir para uma Abelha'
	xbmc.executebuiltin('XBMC.Container.Update(plugin://%s?mode=3&url=%s&name=%s)' % (addon, url,name))	

def filmeshd():
	addon = 'plugin.video.abelhas'
	if not xbmc.getCondVisibility('System.HasAddon('+addon+')'):
		xbmcgui.Dialog().ok(traducao(2010), traducao(2077))
		return
	
	url = urllib.quote_plus('http://abelhas.pt/AdrXbmc/Filmes+*26+S*c3*a9ries/Filmes/HD')
	name = 'Ir para uma Abelha'
	xbmc.executebuiltin('XBMC.Container.Update(plugin://%s?mode=3&url=%s&name=%s)' % (addon, url,name))	
	
def filmesuhd():
	addon = 'plugin.video.abelhas'
	if not xbmc.getCondVisibility('System.HasAddon('+addon+')'):
		xbmcgui.Dialog().ok(traducao(2010), traducao(2077))
		return
	
	url = urllib.quote_plus('http://abelhas.pt/AdrXbmc/Filmes+*26+S*c3*a9ries/Filmes/UHD+*5b1080p*5d')
	name = 'Ir para uma Abelha'
	xbmc.executebuiltin('XBMC.Container.Update(plugin://%s?mode=3&url=%s&name=%s)' % (addon, url,name))	
	
def filmespt():
	addon = 'plugin.video.abelhas'
	if not xbmc.getCondVisibility('System.HasAddon('+addon+')'):
		xbmcgui.Dialog().ok(traducao(2010), traducao(2077))
		return
	
	url = urllib.quote_plus('http://abelhas.pt/AdrXbmc/Filmes+*26+S*c3*a9ries/Filmes/Pt*2c+Made+in')
	name = 'Ir para uma Abelha'
	xbmc.executebuiltin('XBMC.Container.Update(plugin://%s?mode=3&url=%s&name=%s)' % (addon, url,name))	
	
def filmespl():
	addon = 'plugin.video.abelhas'
	if not xbmc.getCondVisibility('System.HasAddon('+addon+')'):
		xbmcgui.Dialog().ok(traducao(2010), traducao(2077))
		return
	
	url = urllib.quote_plus('http://abelhas.pt/AdrXbmc/*e2*97*84Filmy+w+j*c4*99zyku+polskim*e2*96*ba+*e2*94*80*e2*94*80*e2*94*80*e2*94*80*e2*94*80*e2*94*80*e2*94*80*e2*94*80*e2*94*80*e2*94*80*e2*94*80*e2*94*80*e2*94*80*e2*94*80*e2*94*80*e2*94*80*e2*94*80*e2*94*80')
	name = 'Ir para uma Abelha'
	xbmc.executebuiltin('XBMC.Container.Update(plugin://%s?mode=3&url=%s&name=%s)' % (addon, url,name))		
	
def filmes3d():
	addon = 'plugin.video.abelhas'
	if not xbmc.getCondVisibility('System.HasAddon('+addon+')'):
		xbmcgui.Dialog().ok(traducao(2010), traducao(2077))
		return
	
	url = urllib.quote_plus('http://abelhas.pt/AdrXbmc/Filmes+*26+S*c3*a9ries/Filmes/3D')
	name = 'Ir para uma Abelha'
	xbmc.executebuiltin('XBMC.Container.Update(plugin://%s?mode=3&url=%s&name=%s)' % (addon, url,name))			
	
def series():
	addon = 'plugin.video.abelhas'
	if not xbmc.getCondVisibility('System.HasAddon('+addon+')'):
		xbmcgui.Dialog().ok(traducao(2010), traducao(2077))
		return
	
	url = urllib.quote_plus('http://abelhas.pt/AdrXbmc/Filmes+*26+S*c3*a9ries/S*c3*a9ries+(Em+Exibi*c3*a7*c3*a3o)')
	name = 'Ir para uma Abelha'
	xbmc.executebuiltin('XBMC.Container.Update(plugin://%s?mode=3&url=%s&name=%s)' % (addon, url,name))			
	
def seriescompletas():
	addon = 'plugin.video.abelhas'
	if not xbmc.getCondVisibility('System.HasAddon('+addon+')'):
		xbmcgui.Dialog().ok(traducao(2010), traducao(2077))
		return
	
	url = urllib.quote_plus('http://abelhas.pt/AdrXbmc/Filmes+*26+S*c3*a9ries/S*c3*a9ries+Completas')
	name = 'Ir para uma Abelha'
	xbmc.executebuiltin('XBMC.Container.Update(plugin://%s?mode=3&url=%s&name=%s)' % (addon, url,name))		
	
def documentarios():
	addon = 'plugin.video.abelhas'
	if not xbmc.getCondVisibility('System.HasAddon('+addon+')'):
		xbmcgui.Dialog().ok(traducao(2010), traducao(2077))
		return
	
	url = urllib.quote_plus('http://abelhas.pt/AdrXbmc/Filmes+*26+S*c3*a9ries/Document*c3*a1rios')
	name = 'Ir para uma Abelha'
	xbmc.executebuiltin('XBMC.Container.Update(plugin://%s?mode=3&url=%s&name=%s)' % (addon, url,name))

def fitness():
	addon = 'plugin.video.abelhas'
	if not xbmc.getCondVisibility('System.HasAddon('+addon+')'):
		xbmcgui.Dialog().ok(traducao(2010), traducao(2077))
		return
	
	url = urllib.quote_plus('http://abelhas.pt/AdrXbmc/Fitness')
	name = 'Ir para uma Abelha'
	xbmc.executebuiltin('XBMC.Container.Update(plugin://%s?mode=3&url=%s&name=%s)' % (addon, url,name))

def humor():
	addon = 'plugin.video.abelhas'
	if not xbmc.getCondVisibility('System.HasAddon('+addon+')'):
		xbmcgui.Dialog().ok(traducao(2010), traducao(2077))
		return
	
	url = urllib.quote_plus('http://abelhas.pt/AdrXbmc/Humor+*ef*bc*bc(*5e-*5e)*ef*bc*8f')
	name = 'Ir para uma Abelha'
	xbmc.executebuiltin('XBMC.Container.Update(plugin://%s?mode=3&url=%s&name=%s)' % (addon, url,name))

def concertos():
	addon = 'plugin.video.abelhas'
	if not xbmc.getCondVisibility('System.HasAddon('+addon+')'):
		xbmcgui.Dialog().ok(traducao(2010), traducao(2077))
		return
	
	url = urllib.quote_plus('http://abelhas.pt/AdrXbmc/M*c3*basica+*e2*99*ac+*e2*99*aa+*e2*99*ab+*e2*99*a9/*e2*98*aaoncertos')
	name = 'Ir para uma Abelha'
	xbmc.executebuiltin('XBMC.Container.Update(plugin://%s?mode=3&url=%s&name=%s)' % (addon, url,name))

def novelas():
	addon = 'plugin.video.abelhas'
	if not xbmc.getCondVisibility('System.HasAddon('+addon+')'):
		xbmcgui.Dialog().ok(traducao(2010), traducao(2077))
		return
	
	url = urllib.quote_plus('http://abelhas.pt/AdrXbmc/Novelas')
	name = 'Ir para uma Abelha'
	xbmc.executebuiltin('XBMC.Container.Update(plugin://%s?mode=3&url=%s&name=%s)' % (addon, url,name))

def teatrotv():
	addon = 'plugin.video.abelhas'
	if not xbmc.getCondVisibility('System.HasAddon('+addon+')'):
		xbmcgui.Dialog().ok(traducao(2010), traducao(2077))
		return
	
	url = urllib.quote_plus('http://abelhas.pt/AdrXbmc/Teatro+Tv')
	name = 'Ir para uma Abelha'
	xbmc.executebuiltin('XBMC.Container.Update(plugin://%s?mode=3&url=%s&name=%s)' % (addon, url,name))

def _ch(name):
	if selfAddon.getSetting(name) == "true":
		return True
	return False

###################################################################################
#LISTAS

	
def check_version():
	try:
		codigo_fonte=abrir_url('http://pastebin.com/raw.php?i=qh575L2t')
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
elif mode==100: abelhas()
elif mode==110: filmes()
elif mode==111: filmeshd()
elif mode==112: filmesuhd()
elif mode==113: filmespt()
elif mode==114: filmespl()
elif mode==115: filmes3d()
elif mode==120: series()
elif mode==121: seriescompletas()
elif mode==130: documentarios()
elif mode==140: fitness()
elif mode==150: humor()
elif mode==160: concertos()
elif mode==170: novelas()
elif mode==180: teatrotv()


xbmcplugin.endOfDirectory(int(sys.argv[1]))
