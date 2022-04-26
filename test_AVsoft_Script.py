import urllib.request
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def getListLinks(url):
	try:
		if (bool(urlparse(url).scheme) and bool(urlparse(url).scheme)) == True:
			resp = urllib.request.urlopen(url, timeout=5)
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
		return str(er)
	
def recUrl(url,set_url,depth,depthParam):
	if depth < depthParam and (url in set_url) == False:
		set_url.add(url)
		listLinks = getListLinks(url)
		print(listLinks)
		if listLinks != '<urlopen error _ssl.c:1114: The handshake operation timed out>':
			i=0
			for link in listLinks:
				print(i,url,'depth: '+str(depth),link)
				recUrl(link,set_url,depth+1,depthParam)
		
recUrl('http://www.google.com',set(),0,3)
	
#print('https://www.youtube.com/?gl=RU&tab=w1'=='https://www.youtube.com/?gl=RU&tab=i1')
