#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2015 AdrXbmc

import math,re,urllib

def open(html):
	if not re.search('Page protected by ionCube',html): return html
	try:
		d = ''
		c = re.compile('c="(.+?)"').findall(html)[0]
		for i in range(0,len(c)):
			if i%3==0: d+='%'
			else: d += c[i]
		func = urllib.unquote(d)
		Array = '"'+re.compile('Array\((.+?)\)').findall(func)[0].replace(',','" "')+'"'
		match = re.compile('"(.+?)"').findall(Array)
		x = re.compile('x\("(.+?)"\)').findall(html)[0]
		return _function(x,match)
	except: return 'erro'

def _function(x,t):
	l = len(x)
	b=1024; p=0; s=0; w=0;
	html = ''
	j = math.ceil(l/b)
	while j>0:
		r = ''
		i = min(l,b)
		while i>0:
			
			w |= int(t[ord(x[p])-48]) << s
			p+=1
			if(s):
				r+= chr(165^w&255)
				w >>= 8
				s -= 2
			else: s = 6
			i-=1
			l-=1
		j-=1
		html += r
	return html