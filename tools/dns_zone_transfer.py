import dns.resolver, dns.query, dns.zone, re

def nslookup(domain):
	answers = dns.resolver.resolve(domain, "NS")
	for rdata in answers:
		dnsserver = re.sub(r"\.$", "", str(rdata.target))
		print(dnsserver)
		try:
			z = dns.zone.from_xfr(dns.query.xfr(dnsserver, domain))
			print(z.to_text())
			names = z.nodes.keys()
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

