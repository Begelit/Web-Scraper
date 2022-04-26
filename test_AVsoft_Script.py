import urllib.request
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import socket

def getListLinks(url):
	try:
		if (bool(urlparse(url).scheme) and bool(urlparse(url).scheme)) == True:
			resp = urllib.request.urlopen(url, timeout=10)
			soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
			listLinks = []
			i=0
			for link in soup.find_all('a',href=True):
				if (bool(urlparse(link['href']).scheme) and bool(urlparse(link['href']).scheme)) == True:
					listLinks+=[link['href']]
					#print(i,link['href'])
					i+=1
		return listLinks
	except urllib.error.URLError as er:
		print(er)
		return str(er)
	except ConnectionResetError as er_1:
		print(er_1)
		return str(er_1)
	except socket.timeout as er_2:
		print(er_2)
		return str(er_2)
		
	
def recUrl(url,set_url,depth,depthParam):
	if depth < depthParam and (url in set_url) == False:
		set_url.add(url)
		listLinks = getListLinks(url)
		if str(type(getListLinks(url))) == "<class 'list'>":
			i=0
			for link in listLinks:
				print(i,url,'depth: '+str(depth),link)
				recUrl(link,set_url,depth+1,depthParam)
		
recUrl('http://www.google.com',set(),0,3)
	
