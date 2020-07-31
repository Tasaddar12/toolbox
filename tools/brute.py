from multiprocessing import Process, Lock
from multiprocessing.dummy import Pool as ThreadPool
from lib.urlparsing import HTTPParse
import socket

class subBrute:
	def Start(url, thread):
		#Process count
		global proc, urls
		urls = url
		proc = 10
		lock = Lock()
		#Start processes
		print("Starting subBruteforce")
		for i in range(proc):
			Process(target=subBrute.subthreader, args=(lock, i, int(thread), "Lists/subdomains.txt")).start()

	def subthreader(l, num, thread, wordlist):
		l.acquire()
		try:
			#Getting from a wordlist
			with open(wordlist) as f:
				lists = f.read().splitlines()
			curr_list = lists[int(((len(lists)/proc) * num)):int(((len(lists)/proc) * (num + 1)))]
			pool = ThreadPool(thread)
			pool.map(subBrute.subthreading, curr_list)
			pool.close()
			pool.join()
			print("FINISHED THIS CURRENT LOOP OF PROCESS {0}".format(num))
		finally:
			l.release()
			
	def subthreading(lists):
		try:
			ip = socket.gethostbyname(lists + '.' + HTTPParse.rawdomain_parse(urls))
			print("{0} : {1}".format(ip, (lists + '.' + HTTPParse.rawdomain_parse(urls))))
			with open("Logs/subdomains_" + HTTPParse.rawdomain_parse(urls), "a") as log:
				log.write(lists + '.' + HTTPParse.rawdomain_parse(urls) + " : " + ip + "\n")
		except:
			pass

