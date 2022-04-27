import urllib.request
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import socket
				
def getRequest(url):
	listLinks = []
	i=0
	resp = urllib.request.urlopen(url, timeout=10)
	soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
	for link in soup.find_all('a',href=True):
#		if (bool(urlparse(link['href']).scheme) and bool(urlparse(link['href']).netloc)) == True:
		listLinks+=[link['href']]
		print(i,link['href'])
		i+=1
	return listLinks

def getListLinks(url):
	try:
		return getRequest(url)
	except urllib.error.URLError as er:
		print(er)
		return er
	except ConnectionResetError as er_1:
		print(er_1)
		return er_1
	except socket.timeout as er_2:
		print(er_2)
		return er_2
		
def parentDomain(url):
	parentURL = urlparse(url)
	vocabDomain = {'netlocdURL': parentURL.netloc,'schemeURL': parentURL.scheme,
			'domain_1Level': parentURL.netloc.split('.')[0],'domain_2Level': parentURL.netloc.split('.')[1],
			'domain_3Level': parentURL.netloc.split('.')[2]}
	return vocabDomain
		
	
def recUrl(url,set_url,depth,parentDomain_):
	if  (url in set_url) == False:
		set_url.add(url)
		listLinks = getListLinks(url)
		if str(type(listLinks)) == "<class 'list'>":
			i=0
			for link in listLinks:
				print(i,url,'depth: '+str(depth),link)
				if (bool(urlparse(link).scheme) and bool(urlparse(link).netloc)) == True:
					print(link)
					link_Domains = parentDomain(link)
					if (link_Domains['domain_1Level']+'.'+link_Domains['domain_2Level']) == (parentDomain_['domain_1Level']+'.'+parentDomain_['domain_2Level']):
						recUrl(link,set_url,depth+1,parentDomain_)
				elif link[0] == '/' and len(link) > 1:
					absoluteURL = parentDomain_['schemeURL']+'://'+parentDomain_['netlocdURL']+link
					link_Domains = parentDomain_(absoluteURL)
					if (link_Domains['domain_1Level']+'.'+link_Domains['domain_2Level']) == (parentDomain_['domain_1Level']+'.'+parentDomain_['domain_2Level']):
						recUrl(absoluteURL,set_url,depth+1,parentDomain_)
				
url = 'http://www.google.com'
parent_Domain =  parentDomain(url)
print(parent_Domain)
recUrl(url,set(),0,parent_Domain)
"""
url = 'http://www.google.com'
#url = 'http://www.crawler-test.com'
parsedURL = urlparse(url)
vocabDomain = {'netlocdURL': parsedURL.netloc,'schemeURL': parsedURL.scheme,
		'domain_1Level': parsedURL.netloc.split('.')[0],'domain_2Level': parsedURL.netloc.split('.')[1],
		'domain_3Level': parsedURL.netloc.split('.')[2]}
#getListLinks('/intl/ru/policies/terms',vocabDomain)	
getListLinks('/intl/ru/policies/privacy/',vocabDomain)	
"""


#recUrl('http://www.crawler-test.com',set(),0,10)
#print(getListLinks('http://www.crawler-test.com'))
#print(getListLinks('https://www.crawler-test.com//urls/double_slash/disallowed_start'))
#print(getListLinks('http://www.google.com'))
#print(urlparse('http://www.google.com').scheme, urlparse('http://www.google.com').netloc)
#print(str(type(getListLinks('http://www.google.com'))) == "<class 'list'>")
#print('https://www.youtube.com/?gl=RU&tab=w1'=='https://www.youtube.com/?gl=RU&tab=i1')

#parsedURL = urlparse('http://www.crawler-test.com')
#vocabDomain = {'netlocdURL': parsedURL.netloc,'schemeURL': parsedURL.scheme,
#		'domain_1Level': parsedURL.netloc.split('.')[0],'domain_2Level': parsedURL.netloc.split('.')[1],
#		'domain_3Level': parsedURL.netloc.split('.')[2]}
#
#getListLinks('/link_on_nofollowed_2',vocabDomain)

"""
resp = urllib.request.urlopen('http://www.crawler-test.com/links/nofollowed_page', timeout=10)
soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
#print(soup.find_all('a',href=True))
for row in soup.find_all('a',href=True):
	print(row['href'])
print(soup.find_all('a',href=True))
"""
