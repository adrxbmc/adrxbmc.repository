#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 2015 AdrXbmc

def decode(string):
	import base64
	s = ''
	str = _reverse(string)
	for x in range(0,len(str)):
		s += _decode_char(str[x])
	return base64.b64decode(s)
	
def _reverse(s):
	string = ''
	length = len(s)-3
	while length > 2:
		string += s[length]
		length = length - 1
	length = len(string)
	num2 = int(s[1]+s[0])/2
	if num2 < length:
		i = num2
		while i < length:
			if len(string) <= i: return string
			if (i+1) < length: string = string[0:i] + string[i+1:]
			i += num2
	return string
	
def _decode_char(c):
    array1 = ["0", "1", "2", "3", "4", "5", "6", "7", "9", "H", "M", "D", "X", "V", "J", "Q", "U", "G", "E", "T", "N", "o", "v", "y", "w", "k"]
    array2 = ["c", "I", "W", "m", "8", "L", "l", "g", "R", "B", "a", "u", "s", "p", "z", "Z", "e", "d", "=", "x", "Y", "t", "n", "f", "b", "i"]
    for i in range(0,len(array1)):
        if c == array1[i]: return array2[i][0]
        if c == array2[i]: return array1[i][0]
    return c