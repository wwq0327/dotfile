#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import urllib2
from BeautifulSoup import BeautifulSoup

DICT_URL = 'http://3g.dict.cn/s.php?q=%s'

def read_http(url, word):
    sock = urllib2.urlopen(url%word)
    return sock.read()

def dictd(word):
    doc = read_http(DICT_URL, word)
    soup = BeautifulSoup(''.join(doc))
    return soup.findAll('div')[3]

def html2txt(html):
    p = re.compile(r'<.*?>')
    m = p.sub(r'\n', html)
    if m:
    	return m
    else:
	    return html

def main():
    word = sys.argv[1]
    html = dictd(word)
    #print html
    print html2txt(str(html))

if __name__ == '__main__':
    main()

