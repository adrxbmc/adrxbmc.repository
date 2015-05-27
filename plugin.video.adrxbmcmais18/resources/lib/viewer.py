#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2015 AdrXbmc

import xbmc
import xbmcgui
import sys
import os
import xbmcaddon
import urllib2
import re

addon_id = 'plugin.video.adultstv'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
addon_name = selfAddon.getAddonInfo('name')

def traducao(texto):
	return selfAddon.getLocalizedString(texto).encode('utf-8')

class Viewer:
	def __init__( self, *args, **kwargs ):
		if sys.argv[1] == "changelog":
			changelog = self.openfile('changelog.txt')
			self.text(changelog,'Changelog')
		elif sys.argv[1] == "license":
			texto = self.openfile('LICENSE.txt')
			self.text(texto,traducao(1004))
		elif sys.argv[1] == "version":
			try:
				codigo_fonte=self.abrir_url('http://anonymous-repo.googlecode.com/svn/trunk/anonymous-repo-adults/plugin.video.adultstv/addon.xml')
				match=re.compile('version="(.+?)"').findall(codigo_fonte)[1]
			except: match='error'
			if match=='error': xbmcgui.Dialog().ok(traducao(2010),traducao(2059),traducao(2060))
			elif match!=selfAddon.getAddonInfo('version'):xbmcgui.Dialog().ok(traducao(2061)+' ('+match+')',traducao(2062))
			else: xbmcgui.Dialog().ok('Adults TV', traducao(2063))
		elif sys.argv[1] == "xbmctools": xbmcgui.Dialog().ok('XBMC Tools',traducao(2065),traducao(2064))
		elif sys.argv[1] == "disclaimer": self.text(traducao(1003),'Disclaimer')
		elif sys.argv[1] == "help": self.text(traducao(2066)+'\n\ni96751414\nAnonymous',traducao(2067))
		elif sys.argv[1] == "import":
			dir = xbmcgui.Dialog().browse(1,traducao(2072),"myprograms").replace('\\','/')
			if dir == '': return
			if self.file_name(dir) != 'bla.zip':
				xbmcgui.Dialog().ok(traducao(2010),traducao(2073))
				return
			dest = os.path.join(addonfolder,'resources','lib')
			xbmc.executebuiltin('XBMC.Extract('+dir+','+dest+')')
			xbmcgui.Dialog().ok(traducao(2070),traducao(2075))
			
	def file_name(self,path):
		import ntpath
		head, tail = ntpath.split(path)
		return tail or ntpath.basename(head)
	
	def abrir_url(self,url):
		try:
			req = urllib2.Request(url)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
			response = urllib2.urlopen(req)
			link=response.read()
			response.close()
			return link
		except: return 'erro'
	
	def openfile(self,filename,pastafinal=addonfolder):
		try:
			destination = os.path.join(pastafinal, filename)
			fh = open(destination, 'rb')
			contents=fh.read()
			fh.close()
			return contents
		except:
			print "Error on opening file"
			return None

	def text(self,text,name=''):
		try:
			xbmc.executebuiltin("ActivateWindow(10147)")
			window = xbmcgui.Window(10147)
			xbmc.sleep(100)
			titulo = addon_name
			if name != '': titulo += ' - ' + name
			window.getControl(1).setLabel(titulo)
			window.getControl(5).setText(text)
		except: pass
		
def Main():
	Viewer()

if ( __name__ == "__main__" ):
	Main()