import os, socket, re
from multiprocessing.pool import ThreadPool as Pool
#DNS GET SUBDOMAINS
def dns_start(url, thread):
	#Set raw domain and other stuff
	global rawdomain
	rawdomain = re.sub(r"^(https://|http://)", "", url)
	rawdomain = re.sub(r"\/*", "", rawdomain)
	rawdomain = re.sub(r"^(www[a-zA-Z0-9]{0,2}\.)", "", rawdomain)
	#Remove duplicate files
	if os.path.exists("Logs/dns_forward.txt"):
		os.remove("Logs/dns_forward.txt")
	elif os.path.exists("Logs/" + rawdomain):
		os.remove("Logs/" + rawdomain)
	#Use my bash script. Need sublist3r
	os.system('bash tools/dns_subdomain_search.sh ' + rawdomain)
	listdomains(thread)
	
#Put domains into a list
def listdomains(thread):
	global list_of_lists
	a_file = open("tools/temp", "r")
	list_of_lists = [(line.strip()).split() for line in a_file]
	a_file.close()
	threading_pool(int(thread))
	
#Check if DNS server
def dns_test(domain):
	try:
		ip = socket.gethostbyname(domain[0])
		sublist = open("Logs/" + rawdomain, 'a')
		sublist.write(domain[0] + "\n")
		sublist.close()
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			#Set Timeout
			sock.settimeout(3)
			result = sock.connect_ex((ip,53))
			if result == 0:
				print("Open : " + ip)
				dns_forward_event(domain)
			else:
				return
	except:
		print("error can not find : " + domain[0])
		pass
		
#Attempt DNS Forward
def dns_forward_event(domain):
	#DNS Forwarding Check
	os.system('host -t axfr ' + rawdomain + ' ' + domain[0] + ' >> Logs/dns_forward.txt')
	
#Threading
def threading_pool(thread):
	try:
		pool = Pool(thread)
		for domain in list_of_lists:
			pool.apply_async(dns_test, (domain,))
		pool.close()
		pool.join()
		print("\x1b[1;36;40mFINISHED\x1b[0;38;40m")
	except KeyboardInterrupt:
		print("\n Interrupt")
		exit()
