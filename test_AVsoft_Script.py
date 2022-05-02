import urllib.request
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import socket
import multiprocessing
set_url = set()
vocab_tree = {}

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
	except UnicodeEncodeError as er_3:
		print(er_3)
		return er_3

def return_absoluteURL(parentURL,url):
	global set_url
		#На вход функции поступает ссылка url. Определим на раннем этапе её абсолютность.
	if (bool(urlparse(url).scheme) and bool(urlparse(url).netloc)) == True:
		#Если ссылка абсолютна, проверим её на наличие в проверочном множестве посещенных ссылок set_url
		if  (url in set_url) == False:
			#Заносим ссылку в множество set_url посещенных ссылок 
			set_url.add(url)
			return url
		else :
			return 'visited_site'
	#Проверим ссылку на её относительность
	else:
		if (urljoin(parentURL,url) in set_url) == True:
			return ' visited_site'
		else :
			set_url.add(urljoin(parentURL,url))
			return urljoin(parentURL,url)


def create_tree(response):
	global vocab_tree
#	vocab_tree[str(response[0][2])+'_level'].append({response[0][1]:list(set(response[0][0]))})
	for row in response:
		if row != None:
			vocab_tree[str(row[2])+'_level'].append({row[1]:list(set(row[0]))})
#			print(row)
#	print(response,'\n')
	
def recUrl_(url,mainURL,parentURL,level):
	global set_url
	global vocab_tree
	absoluteURL = return_absoluteURL(parentURL,url)	
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
#					print(linkList)
#					vocab_tree[str(level)+'_level'].append({absoluteURL:list(set(linkList))})
#					print(linkList)
#					print()
					return list(set(linkList)), absoluteURL, level
#					for link in linkList:
#						print(depth,parentURL,link)
#						recUrl_(link,depth+1,mainURL,parentURL)
		
if __name__ == "__main__":
	mainURL = 'http://www.google.com'
	url = 'http://www.google.com'
	parentURL = 'http://www.google.com'
	level = 1
	vocab_tree['1_level'] = []
	with multiprocessing.Pool(multiprocessing.cpu_count()*3) as p:
		p.starmap_async(recUrl_,[('http://www.google.com','http://www.google.com','http://www.google.com',level)],callback=create_tree)
		p.close()
		p.join()
	print(vocab_tree)
	secon_list = vocab_tree['1_level'][0]['http://www.google.com']
	print(secon_list)
	
	arg_list = []
	vocab_tree['2_level'] = []
	for url_flist in secon_list:
		arg_list+=[(url_flist,mainURL,url,level+1)]
	print(arg_list)
	with multiprocessing.Pool(multiprocessing.cpu_count()*3) as p:
		p.starmap_async(recUrl_,arg_list,callback=create_tree)
		p.close()
		p.join()
	print(vocab_tree)
	
