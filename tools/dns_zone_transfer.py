import dns.resolver, dns.query, dns.zone, re
from lib.urlparsing import HTTPParse

class DNSAttacks:
	def nslookup(domain):
		#Set RawDomain
		domain = HTTPParse.rawdomain_parse(domain)
		#Attempt to resolve dns
		try:
			resol = dns.resolver.Resolver()
			answers = resol.query(domain, "NS")
		except:
			raise
			pass
		#Start to filter the data
		for rdata in answers:
			dnsserver = re.sub(r"\.$", "", str(rdata.target))
			print(dnsserver)
			#Attempt Zone Transfer
			try:
				z = dns.zone.from_xfr(dns.query.xfr(dnsserver, domain))
				print(z.to_text())
				names = z.nodes.keys()
				#Start writing to a log file
				f = open('Logs/' + domain + '-dns_transfer.log', 'w')
				for n in names:
					print(str(n) + "." + domain)
					f.write(str(n) + "." + domain + "\n")
				f.write("\n\n")
				f.write(z.to_text())
				f.close()
				break
			except:
				print("error")
				pass
		print("FINISHED")

