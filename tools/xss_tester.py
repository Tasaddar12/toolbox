import re, os, requests, sys
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool as Pool

def xss_start(url, thread):
	#Setting Some Variables
	global rawdomain, url_paths, xss_file, checker, attack
	url_paths = []
	xss_file = []
	checker = []
	attack = []
	
	
	#Set rawdomain
	tempurl = re.sub(r"\/$", "", url)
	rawdomain = re.sub(r"^(https://|http://)", "", tempurl)
	
	#Check There is a Dynamic URL File
	if not os.path.exists("Logs/Dynamic_URL_" + rawdomain):
		print("\x1b[1;34;40mPerform a Spider First \nOR \nMay not have found any dynamic URLs.\x1b[0;38;40m")
		return()
		
	#Get Dynamic URLs and Sort Them Out
	with open("Logs/Dynamic_URL_" + rawdomain, "r") as f:
		temp = f.readlines()
		for i in temp:
			url_paths.append(i.rstrip("\n"))
			
	#Get XSS Payloads
	with open("Lists/xss.txt", "r") as f:
		xss_file = f.readlines()
		
	#Start Preparing
	for url in url_paths:	
		test = re.split(r"\?(.*)\=.*", url)
		if test in checker:
			continue
		checker.append(test)
	for url_path in checker:
		attack.append(url_path)

	#Start Attacking
	threading_pool(int(thread))
	print("\x1b[1;36;40mFINISHED\x1b[0;38;40m")
	
#Locate injectables
def xss_do(url, thread):
	soup = BeautifulSoup(requests.get(url[0] + "?" + url[1] + "=XsSTeStInGHelLO", timeout=5).text, 'html.parser')
	if re.search(r"XsSTeStInGHelLO", requests.get(url[0] + "?" + url[1] + "=XsSTeStInGHelLO", timeout=5).text):
		xss_pool(int(thread), url)
		
#Attack the possible injectable parameter
def xss_attack(url, inject):
	if re.search(inject, requests.get(url[0] + "?" + url[1] + "=" + inject, timeout=5).text):
		print(url[0] + "?" + url[1] + "=" + inject + " : Might Be Injectable", end="\n")
	else:
		#Progress as well :)
		print("Progress : ", end='')
		print("{0}\r".format(xss_file.index(inject)), end='')
		print(" / {0}".format(len(xss_file)))
#Main Threading
def threading_pool(thread):
	try:
		pool = Pool(thread)
		for url in attack:
			pool.apply_async(xss_do, (url, thread,))
		pool.close()
		pool.join()
	except KeyboardInterrupt:
		print("\n Interrupt")
		exit()
	except:
		print("error")

#XSS Threading
def xss_pool(thread, url):
	try:
		xss_pool = Pool(thread)
		for inject in xss_file:
			xss_pool.apply_async(xss_attack, (url, inject,))
		xss_pool.close()
		xss_pool.join()
	except KeyboardInterrupt:
		print("\n Interrupt")
		exit()
	except:
		print("error")
