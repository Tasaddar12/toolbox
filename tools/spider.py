#imports
import re, requests, os
from multiprocessing.pool import ThreadPool as Pool
from bs4 import BeautifulSoup
#START MAIN SCRIPT
#Some settings
temp = []
check = []
#Startup function
def spider_start(url, thread, loop, depth):
	try:
		#Attempt to get url
		requests.get(url).status_code
		#Settings
		global rawurl, dep, rawdomain
		dep = depth
		url = re.sub(r"\/$", "", url)
		rawurl = url
		rawdomain = re.sub(r"^(https://|http://)", "", url)
		print(rawdomain)
		#remove duplicate files
		if os.path.exists("Logs/Spider_log_" + rawdomain):
			os.remove("Logs/Spider_log_" + rawdomain)
		temp.append(url)
		crawl(url)
		for i in range(int(loop)):
			print("\x1b[1;32;40mStarting Loop : {}\x1b[0;38;40m".format(i + 1))
			threading_pool(int(thread))
		print("\x1b[1;36;40mFINISHED\x1b[0;38;40m")
	except:
		print("URL Not Available")
####################################################Functions####################################################
def crawl(url):
	#Check if available and add to checks
	check.append(url)
	if requests.get(url).status_code == 404:
		return
	#add to log file
	spider_log = open("Logs/Spider_log_" + rawdomain, 'a')
	if re.search(r"(\?|\=)", url):
		spider_log.write(url + " : " +  str(requests.get(url).status_code) + " DYNAMIC\n")
	else:
		spider_log.write(url + " : " + str(requests.get(url).status_code) + "\n")
	spider_log.close()
	#Printing to console
	print(url + " : \x1b[1;33;40m" + str(requests.get(url).status_code) + "\x1b[0;38;40m")
	#Grabbing the text and parsing it
	soup = BeautifulSoup(requests.get(url).text, 'html.parser')
	#Crawl Links
	for link in soup.find_all('a'):
		#Check if part of domain
		if not link.get('href'):
			continue
		if (re.search(r"^(https://|http://)", link.get('href')) and not re.search("^.{5,15}" + rawdomain, link.get('href'))):
			continue
		#Check if starts with http or https
		if re.search(r"(http://|https://)", link.get('href')):
			if link.get('href') not in temp:
				temp.append(link.get('href'))
		if not re.search(r"(https://|http://)", link.get('href')):
			if (rawurl + link.get('href')) not in temp and re.search(r"^\/", link.get('href')):
				temp.append(rawurl + link.get('href'))
			elif not re.search(r"^\/", link.get('href')) and (rawurl + "/" + link.get('href')) not in temp:
				temp.append(rawurl + "/" + link.get('href'))
	#Checking the depth
	if int(dep) >= 2:
		#Crawl scripts
		for link in soup.find_all('script'):
			if not link.get('src'):
				continue
			if (re.search(r"^(https://|http://)", link.get('src')) and not re.search("^.{5,15}" + rawdomain, link.get('src'))):
				continue
			if re.search(r"(http://|https://)", link.get('src')):
				if link.get('src') not in temp:
					temp.append(link.get('src'))
			if not re.search(r"(https://|http://)", link.get('src')):
				if (rawurl + link.get('src')) not in temp and re.search(r"^\/", link.get('src')):
					temp.append(rawurl + link.get('src'))
				elif not re.search(r"^\/", link.get('src')) and (rawurl + "/" + link.get('src')) not in temp:
					temp.append(rawurl + "/" + link.get('src'))
#Threading
def threading_pool(thread):
	try:
		pool = Pool(thread)
		for url in temp:
			if url in check:
				continue
			pool.apply_async(crawl, (url,))
		pool.close()
		pool.join()
	except KeyboardInterrupt:
		print("\n Interrupt")
		exit()

