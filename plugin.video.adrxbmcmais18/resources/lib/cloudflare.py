#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2015 AdrXbmc

import urllib2,re

user_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2049.0 Safari/537.36'

def jsdec(conta):
    conta = conta.replace('!+[]','1').replace('+!![]','+1').replace('+[]','+0')
    conta = conta.replace('(','str(').replace('(+','(')
    if conta[0]=='+': conta = conta[1:]
    return int(eval(conta))

def calc_jschl_answer(url,html):
	s = url.split('/')[2].replace('www.','')
	a_start = html.find('a.value')
	idexpr = html[a_start + 10:html.find(';', a_start)].split('(')[1].split(',')[0]
	part1 = idexpr.split('.')[0]
	part2 = idexpr.split('.')[1]
	expr = str(jsdec(re.compile('{"'+part2+'":(.+?)}').findall(html)[0]))
	rest = re.compile(part1+'.'+part2+'(.+?)=(.+?);').findall(html)
	for op,numb in rest:
		expr = '(' + expr + op + str(jsdec(numb)) + ')'
	return eval(expr) + len(s)

def get_form_values(html):
    action_url_start = html.find("action=\"") + 8
    action_url_end = html.find("\"", action_url_start + 1)
    action_url = html[action_url_start:action_url_end]

    a = 'name="jschl_vc" value="'
    vc_value_start = html.find(a) + len(a)
    vc_value_end = html.find('"', vc_value_start)
    vc_value = html[vc_value_start:vc_value_end]

    return action_url, vc_value


def cf_get_url(url, js_answer, vc_value):
    return '%s?jschl_vc=%s&jschl_answer=%s' % (url, vc_value, js_answer)


class NoRedirectHandler(urllib2.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, hdrs, newurl):
        pass  # Disable redirect


def cloudflare_clearance(urlfirst,cf_content, cfduid_cookie):
    js_answer = calc_jschl_answer(urlfirst,cf_content)
    url, vc = get_form_values(cf_content)
    url_with_query = cf_get_url(url, js_answer, vc)
    url_para_clearance='/'.join(urlfirst.split('/')[:3])

    headers = {
        'Cookie': cfduid_cookie,
        'User-Agent': user_agent
    }
    req = urllib2.Request(url_para_clearance + url_with_query,
                          headers=headers)
    try:
        opener = urllib2.build_opener(NoRedirectHandler)
        opener.open(req).read()
    except Exception, e:
        cookie = e.headers.getheader('Set-Cookie').split(';')[0]
        return cookie


def _webpage_request(url, data=None, cookie_string=None):
    headers = {
        'User-agent': user_agent,
        'Cookie': cookie_string
    }
    req = urllib2.Request(url, headers=headers)
    if data:
        req.add_data(data)

    return urllib2.urlopen(req).read()


def webpage_request(url, data=None, cookie_string=None):
    headers = {
        'User-Agent': user_agent
    }
    if cookie_string:
        headers['Cookie'] = cookie_string
    try:
        req = urllib2.Request(url, headers=headers)
        if data:
            req.add_data(data)
        return urllib2.urlopen(req).read()
    except urllib2.HTTPError, e:
        if e.code != 503:
            return ('Devolveu erro de codigo: %d' % e.code)

        cfduid_cookie = e.headers.getheaders('Set-Cookie')[0].split(';')[0]

        clearance_cookie = cloudflare_clearance(url,e.read(), cfduid_cookie)
        cookie_string = '%s;%s' % (cfduid_cookie, clearance_cookie)

        return _webpage_request(url, data, cookie_string)
