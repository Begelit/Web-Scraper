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
		listLinks+=[link['href']]
		#print(i,link['href'])
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
	
def findUrlInSet(url,set_url):
	for link in set_url:
		findIndex = link.find(url)
		if findIndex > -1:
			return 'visited_site'
	return findIndex

def recUrl_(url,set_url,depth,mainURL,parentURL):
	#На вход функции поступает ссылка url. Определим на раннем этапе её абсолютность.
	if (bool(urlparse(url).scheme) and bool(urlparse(url).netloc)) == True:
		#Если ссылка абсолютна, проверим её на наличие в проверочном множестве посещенных ссылок set_url
		if  (url in set_url) == False:
			#Заносим ссылку в множество set_url посещенных ссылок 
			set_url.add(url)
			absoluteURL = url
		else :
			absoluteURL = 'visited_site'
	#Проверим ссылку на её относительность
	elif url[0] == '/' and len(url) > 1:
		if findUrlInSet(url,set_url) == -1:
			absoluteURL = parentURL+url
			set_url.add(absoluteURL)
		else :
			absoluteURL = findUrlInSet(url,set_url)
	else:
		return
			
	if absoluteURL != 'visited_site':
		#Теперь проверим принадлежит ли имя главного домена с именем посещаемого домена.
		parsed_mainURL = urlparse(mainURL)
		parsed_absoluteURL = urlparse(absoluteURL)
		if parsed_mainURL.netloc == parsed_absoluteURL.netloc:
			#Если принадлежит, то можно совершать HTTP запрос
			parentURL = absoluteURL
			if absoluteURL.rfind('http') <= 0 and absoluteURL.rfind('https') <= 0:
				linkList = getListLinks(parentURL)
				if str(type(linkList)) == "<class 'list'>":
					for link in linkList:
						print(depth,parentURL,link)
						recUrl_(link,set_url,depth+1,mainURL,parentURL)
		
mainURL = 'http://www.google.com'
url = 'http://www.google.com'
parentURL = 'http://www.google.com'
recUrl_(url,set(),0,mainURL,parentURL)	
