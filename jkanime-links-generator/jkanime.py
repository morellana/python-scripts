# -*- coding: utf-8 -*-

# Script para aumatizar la extracción de links de descarga
# desde el sitio http://jkanime.net
# Uso:	python jkanime.py http://jkanime.net/<anime_name>/ inicio fin > links.txt


import sys
import os
import requests
from bs4 import BeautifulSoup

baseURL = "http://jkanime.net/"
serieName = sys.argv[1]
start 	= int(sys.argv[2])
end		= int(sys.argv[3])

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'}
c = requests.session()

for episode in range(start,end+1):
	request = c.get(baseURL+serieName+"/"+str(episode), headers=headers)
	soup = BeautifulSoup(request.content)
	linkSection = soup.find('div', {'id': 'basic-modal-content'})
	downloadLink = linkSection.find('a')['href'] # tomar el primer link
	downloadLink = downloadLink.replace('https://anon.click/?', '')
#	print downloadLink

	cmd = "phantomjs zippyshare.js {0:s}".format(downloadLink)
	os.system(cmd)
