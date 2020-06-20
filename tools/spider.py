#imports
import re, requests, os
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
from lib.urlparsing import HTTPParse
from lib.spider_parse import Spider_parse

#START MAIN SCRIPT
class Spider:
	#Startup function
	def spiderinit(url, thread, loop, depth):
		#Attempt to get url
		requests.get(url).status_code
		#Settings
		global rawurl, dep, rawdomain, temp, check
		temp = []
		check = []
		dep = depth
		rawurl = ((re.split(r'\/', url))[0] + "//" + (re.split(r'\/', url))[2])
		rawdomain = HTTPParse.rawdomain_parse(url)
		url = rawurl
		print(rawdomain)
	
		#remove duplicate files
		#if os.path.exists("Logs/Spider_log_" + rawdomain):
			#os.remove("Logs/Spider_log_" + rawdomain)
		temp.append(url)
		Spider.crawl(url)
		for i in range(int(loop)):
			print("\x1b[1;32;40mStarting Loop : {}\x1b[0;38;40m".format(i + 1))
			Spider.threading_pool(int(thread))
		print("\x1b[1;36;40mFINISHED\x1b[0;38;40m")
	####################################################Functions####################################################
	def crawl(url):
		if url in check:
			return
		#Check if available and add to checks
		check.append(url)
		if requests.get(url).status_code == 404:
			return
		#Printing to console
		print(url + " : \x1b[1;33;40m" + str(requests.get(url).status_code) + "\x1b[0;38;40m")
		#Grabbing the text and parsing it
		for link in Spider_parse.tag(url, dep):
			if link not in temp:
				temp.append(link)

	#Threading
	def threading_pool(thread):
		'''try:
			pool = Pool(thread)
			for url in temp:
				if url in check:
					continue
				pool.apply_async(Spider.crawl, (url,))
			pool.close()
			pool.join()
		except KeyboardInterrupt:
			print("\n Interrupt")
			exit()'''
		pool = ThreadPool(thread)
		results = pool.map(Spider.crawl, temp)
		pool.close()
		pool.join()

