#Parsing spider stuff
import re, requests
from bs4 import BeautifulSoup
from lib.urlparsing import HTTPParse

class Spider_parse:
	def tag(url, depth):
		#Settings
		tags = [['a', 'href'],['script', 'src']]
		rawurl = ((re.split(r'\/', url))[0] + "//" + (re.split(r'\/', url))[2])
		rawdomain = HTTPParse.rawdomain_parse(url)
		soup = BeautifulSoup(requests.get(url).text, 'html.parser')
		urllist = []
		#Grabber
		for i in range(int(depth)):
			for link in soup.find_all(tags[i][0]):
				#Checks for if within scope. Can have a false positive
				if not link.get(tags[i][1]):
					continue
				if (re.search(r"^(https://|http://)", link.get(tags[i][1])) and not re.search("^.{5,15}" + rawdomain, link.get(tags[i][1]))):
					continue
				#Start search
				if re.search(r"(http://|https://)", link.get(tags[i][1])):
					if link.get(tags[i][1]) not in urllist:
						urllist.append(link.get(tags[i][1]))
				if not re.search(r"(https://|http://)", link.get(tags[i][1])):
					if (rawurl + link.get(tags[i][1])) not in urllist and re.search(r"^\/", link.get(tags[i][1])):
						urllist.append(rawurl + link.get(tags[i][1]))
					elif not re.search(r"^\/", link.get(tags[i][1])) and (rawurl + "/" + link.get(tags[i][1])) not in urllist:
						urllist.append(rawurl + "/" + link.get(tags[i][1]))
		#Return found list
		return(urllist)

