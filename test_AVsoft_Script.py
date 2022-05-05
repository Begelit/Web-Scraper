import urllib.request
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import socket
import multiprocessing
import time
import os
import pandas as pd
import json
import shutil
from urllib3.exceptions import ProtocolError
import http.client
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'


manager = multiprocessing.Manager()
sum_url = 1

class Web_Crawler(object):
	@staticmethod
	def getRequest(url):
		listLinks = []
		i=0
		resp = urllib.request.urlopen(url, timeout=10)
		soup = BeautifulSoup(resp,'lxml', from_encoding=resp.info().get_param('charset'))
		for link in soup.find_all('a',href=True):
			listLinks+=[link['href']]
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
		except http.client.IncompleteRead as er_4:
			print(er_4,'----->',url)
			return er_4
	@staticmethod
	def return_absoluteURL(parentURL,url,set_url_Dir):
		df = pd.read_csv(set_url_Dir)
		list_df = df['set_url'].tolist()
		set_url = set(list_df)
		#На вход функции поступает ссылка url. Определим на раннем этапе её абсолютность.
		if (bool(urlparse(url).scheme) and bool(urlparse(url).netloc)) == True:
			#if url.find('www') < 0:
				#absoluteURL = urlparse(url).scheme+'://www.'+urlparse(url).netloc
			#Если ссылка абсолютна, проверим её на наличие в проверочном множестве посещенных ссылок set_url
			if  (url in set_url) == False:
				#Заносим ссылку в множество set_url посещенных ссылок 
				os.remove(set_url_Dir)
				set_url.add(url)
				df_=pd.DataFrame({'set_url':list(set_url)})
				df_.to_csv(set_url_Dir)
				return url
			else :
				return 'visited_site'
		#Проверим ссылку на её относительность
		else:
			if url == '/':
				url = parentURL
			if (urljoin(parentURL,url) in set_url) == True:
				return ' visited_site'
			else :
				os.remove(set_url_Dir)
				set_url.add(urljoin(parentURL,url))
				df_=pd.DataFrame({'set_url':list(set_url)})
				df_.to_csv(set_url_Dir)
				return urljoin(parentURL,url)
	
	@staticmethod
	def recUrl_(url,mainURL,parentURL,level,set_url_Dir,tree_jsonPath,parent_id,id_,lock):

		lock.acquire()
		url = url.replace(' ','')
		absoluteURL = Web_Crawler.return_absoluteURL(parentURL,url,set_url_Dir)	
		#print('=========',absoluteURL,'=========')
		lock.release()
		if absoluteURL != 'visited_site':
			#Теперь проверим принадлежит ли имя главного домена с именем посещаемого домена.
			parsed_mainURL = urlparse(mainURL)
			parsed_absoluteURL = urlparse(absoluteURL)
			replace_main_www = (urlparse(mainURL).netloc).replace('www.','')
			if (parsed_mainURL.netloc == parsed_absoluteURL.netloc):
				#or (replace_main_www == urlparse(absoluteURL).netloc)):
				#Если принадлежит, то можно совершать HTTP запрос
				parentURL = absoluteURL
				if absoluteURL.rfind('http') <= 0 and absoluteURL.rfind('https') <= 0:
					linkList = Web_Crawler.getListLinks(parentURL)
					#print(linkList)
					if str(type(linkList)) == "<class 'list'>":
					
						lock.acquire()
						#print('\n-----',parentURL,'-----')
						with open(tree_jsonPath) as f:
							vocab_tree = json.load(f)

						vocab_tree[str(level)+'_level'][parentURL] = {}
						vocab_tree[str(level)+'_level'][parentURL]['list'] = linkList
						vocab_tree[str(level)+'_level'][parentURL]['id'] = id_
						vocab_tree[str(level)+'_level'][parentURL]['parent_id'] = parent_id

						os.remove(tree_jsonPath)
						with open(tree_jsonPath,'w') as f:
							json.dump(vocab_tree,f,sort_keys = True,indent = 3)
							f.close()
						lock.release()

	@staticmethod
	def multiproc_method(url,mainURL,parentURL,path):
		if __name__ == "__main__":

			t_start = time.time()
			level = 1
			vocab_tree = dict()
			vocab_tree['1_level'] = {}
			lock = manager.RLock()
			id_ = '1'
			parent_id = '0'
			
			nameMainDir = urlparse(mainURL).netloc.split('.')[0]
			print(nameMainDir)
			if bool(os.path.exists(path+'/'+nameMainDir)) == False:
				os.mkdir(path+'/'+nameMainDir)
			mainDirPath = path+'/'+nameMainDir
			if bool(os.path.exists(mainDirPath+'/set_url.csv')) == False:
				df_set = pd.DataFrame(columns=['set_url'])
				df_set.to_csv(mainDirPath+'/set_url.csv')
			else:
				os.remove(mainDirPath+'/set_url.csv')
				df_set = pd.DataFrame(columns=['set_url'])
				df_set.to_csv(mainDirPath+'/set_url.csv')	
			set_url_Dir = mainDirPath+'/set_url.csv'
			if bool(os.path.exists(mainDirPath+'/tree_json.json')) == False:
				with open(mainDirPath+'/tree_json.json','w') as f:
					json.dump(vocab_tree,f,sort_keys = True)
					f.close()
			else:
				os.remove(mainDirPath+'/tree_json.json')
				with open(mainDirPath+'/tree_json.json','w') as f:
					json.dump(vocab_tree,f,sort_keys = True)
					f.close()
			tree_jsonPath = mainDirPath+'/tree_json.json'
			if bool(os.path.exists(mainDirPath+'/copy')) == True:
				shutil.rmtree(mainDirPath+'/copy')
			os.mkdir(mainDirPath+'/copy')
			
			with multiprocessing.Pool(multiprocessing.cpu_count()*3) as p:
				p.starmap(Web_Crawler.recUrl_,[(url,mainURL,parentURL,level,set_url_Dir,tree_jsonPath,parent_id,id_,lock)])
				p.close()
				p.join()
			
			shutil.copyfile(r''+tree_jsonPath,r''+mainDirPath+'/copy/tree_json_'+str(level)+'_level.json')
			
			while True:
				level+=1
				with open(tree_jsonPath) as f:
					vocab_tree = json.load(f)
				vocab_tree[str(level)+'_level'] = {}
				if not vocab_tree[str(level-1)+'_level']:
					if os.path.getsize(r''+mainDirPath+'/copy/tree_json_'+str(level-1)+'_level.json') <= os.path.getsize(r''+mainDirPath+'/copy/tree_json_'+str(level-2)+'_level.json'):
						os.remove(mainDirPath+'/tree_json.json')
						shutil.copyfile(r''+mainDirPath+'/copy/tree_json_'+str(level-2)+'_level.json',r''+tree_jsonPath)
					break
				else:
					with open(mainDirPath+'/tree_json.json','w') as f:
						json.dump(vocab_tree,f,sort_keys = True)
					id_ = 1
					#print(vocab_tree[str(level-1)+'_level'],)
					for link in vocab_tree[str(level-1)+'_level'].keys():
						print('\n-----',link,'-----','time:',time.time()-t_start,'seconds','-----')
						arg_list = []
						lock = manager.Lock()
						for url in vocab_tree[str(level-1)+'_level'][link]['list']:
							arg_list+=[(url,mainURL,link,level,set_url_Dir,tree_jsonPath,vocab_tree[str(level-1)+'_level'][link]['id'],id_,lock)]
							#Web_Crawler.recUrl_(url,mainURL,link,level,set_url_Dir,tree_jsonPath,vocab_tree[str(level-1)+'_level'][link]['id'],id_,lock)
							id_+=1
						with multiprocessing.Pool(multiprocessing.cpu_count()*3) as p:
							p.starmap(Web_Crawler.recUrl_,arg_list)
							p.close()
							p.join()
						
					shutil.copyfile(r''+tree_jsonPath,r''+mainDirPath+'/copy/tree_json_'+str(level)+'_level.json')
					with open(mainDirPath+'/copy/time_'+str(level)+'_level.txt','w') as time_f:
						time_f.write(str(time.time()-t_start))
						time_f.close()
if __name__ == "__main__":
	mainURL = 'http://crawler-test.com'
	url = 'http://crawler-test.com'
	parentURL = 'http://crawler-test.com'
	path = '/home/koza/projects/testABS'
	Web_Crawler.multiproc_method(url,mainURL,parentURL,path)
	mainURL = 'http://www.vk.com'
	url = 'http://www.vk.com'
	parentURL = 'http://www.vk.com'
	path = '/home/koza/projects/testABS'
	Web_Crawler.multiproc_method(url,mainURL,parentURL,path)
	mainURL = 'http://yandex.ru'
	url = 'http://yandex.ru'
	parentURL = 'http://yandex.ru'
	path = '/home/koza/projects/testABS'
	Web_Crawler.multiproc_method(url,mainURL,parentURL,path)
	mainURL = 'http://stackoverflow.com'
	url = 'http://stackoverflow.com'
	parentURL = 'http://stackoverflow.com'
	path = '/home/koza/projects/testABS'
	Web_Crawler.multiproc_method(url,mainURL,parentURL,path)
	mainURL = 'http://google.com'
	url = 'http://google.com'
	parentURL = 'http://google.com'
	path = 'http://google.com'
	Web_Crawler.multiproc_method(url,mainURL,parentURL,path)
