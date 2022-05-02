import urllib.request
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import socket
import multiprocessing
set_url = set()
vocab_tree = {}

class Web_Crawler(object):
	@staticmethod
	def getRequest(url):
		listLinks = []
		i=0
		resp = urllib.request.urlopen(url, timeout=10)
		soup = BeautifulSoup(resp,'lxml', from_encoding=resp.info().get_param('charset'))
		for link in soup.find_all('a',href=True):
			listLinks+=[link['href']]
			#print(i,link['href'])
			i+=1
		return listLinks
	@staticmethod
	def getListLinks(url):
		try:
			return Web_Crawler.getRequest(url)
		except urllib.error.URLError as er:
			print(er,'----->',url)
			return er
		except ConnectionResetError as er_1:
			print(er_1,'----->',url)
			return er_1
		except socket.timeout as er_2:
			print(er_2,'----->',url)
			return er_2
		except UnicodeEncodeError as er_3:
			print(er_3,'----->',url)
			return er_3
	@staticmethod
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
	@staticmethod
	def create_tree(response):
		global vocab_tree
		for row in response:
			if row != None:
				vocab_tree[str(row[2])+'_level'][row[1]] = list(set(row[0]))
	@staticmethod
	def recUrl_(url,mainURL,parentURL,level):
		global set_url
		global vocab_tree
		absoluteURL = Web_Crawler.return_absoluteURL(parentURL,url)	
		if absoluteURL != 'visited_site':
			#Теперь проверим принадлежит ли имя главного домена с именем посещаемого домена.
			parsed_mainURL = urlparse(mainURL)
			parsed_absoluteURL = urlparse(absoluteURL)
			if parsed_mainURL.netloc == parsed_absoluteURL.netloc:
				#Если принадлежит, то можно совершать HTTP запрос
				parentURL = absoluteURL
				if absoluteURL.rfind('http') <= 0 and absoluteURL.rfind('https') <= 0:
					linkList = Web_Crawler.getListLinks(parentURL)
					if str(type(linkList)) == "<class 'list'>":
						return list(set(linkList)), absoluteURL, level
	@staticmethod
	def multiproc_method(url,mainURL,parentURL,path):
		if __name__ == "__main__":
			global vocab_tree
			level = 1
			vocab_tree['1_level'] = {}
			with multiprocessing.Pool(multiprocessing.cpu_count()*3) as p:
				p.starmap_async(Web_Crawler.recUrl_,[(url,mainURL,parentURL,level)],callback=Web_Crawler.create_tree)
				p.close()
				p.join()
			while True:
				level+=1
				if not vocab_tree[str(level-1)+'_level']:
					break
				else:
					vocab_tree[str(level)+'_level'] = {}
					for link in vocab_tree[str(level-1)+'_level'].keys():
						print('-----',link,'-----')
						print('-----',str(level-1)+'_level','-----')
						print(vocab_tree[str(level-1)+'_level'][link])
						arg_list = []
						for url in vocab_tree[str(level-1)+'_level'][link]:
							arg_list+=[(url,mainURL,link,level)]
						with multiprocessing.Pool(multiprocessing.cpu_count()*3) as p:
							p.starmap_async(Web_Crawler.recUrl_,arg_list,callback=Web_Crawler.create_tree)
							p.close()
							p.join()
	
if __name__ == "__main__":
	mainURL = 'http://www.google.com'
	url = 'http://www.google.com'
	parentURL = 'http://www.google.com'
	path = '/home/koza/projects/testABS'
	print(Web_Crawler.multiproc_method(url,mainURL,parentURL,path))
