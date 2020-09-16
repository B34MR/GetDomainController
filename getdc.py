#!/usr/bin/python3
# A python utility that leverages DNS queries to discover an environment's domain controller(s).

import arguments
import dns.resolver
import logging
import json
import sys


def query(name, service='', protocol='', recordtype='', nameserver=''):
	'''Queries a Domain Name to resolve it's SRV records
	or queries a Hostname to resolve it's IP records.

	Keyword arguments:
	name -- DomainName or HostName (required, default none)
	service -- Service name (optional, accepted values _kerberos./_ldap./_autodiscover., default none)
	protocol -- Transport protocol of the service (optional, accepted values _tcp./_udp., default none)
	recordtype -- DNS Record type (optional, accepted values SRV/A, default SRV)
	nameserver -- Nameserver to query from (optional, default /etc/resolv.conf)
	'''
	
	# DomainController list
	dc_lst = []

	try:

		if recordtype == 'SRV':
			if nameserver: # custom nameserver selected
				custom_resolver = dns.resolver.Resolver(configure=False)
				custom_resolver.nameservers = [nameserver]
				answer = custom_resolver.query(service + protocol + name, recordtype, raise_on_no_answer=True)
			else: # default nameserver selected
				answer = dns.resolver.resolve(service + protocol + name, recordtype, raise_on_no_answer=True)

			for record in answer:
				hostname = str(record).lower()[9:] # parse out srv-record for hostname
				dc_lst.append(hostname) # populate dc_list with hostname
		else:
			if nameserver: # custom nameserver selected
				custom_resolver = dns.resolver.Resolver(configure=False)
				custom_resolver.nameservers = [nameserver]
				answer = custom_resolver.query(service + protocol + name, recordtype, raise_on_no_answer=True)
			else: # default nameserver selected
				answer = dns.resolver.resolve(service + protocol + name, recordtype, raise_on_no_answer=True)
			
			for record in answer:
				ipaddress = str(record)	# convert rdata to string
				dc_lst.append(ipaddress) # populate dc_list with ipaddress (IPAddress)

	except dns.resolver.NXDOMAIN as error:
		logging.debug(f'NXDOMAIN-{error}\n')
		pass
	except dns.resolver.NoAnswer as error:
		logging.debug(f'NoAnswer-{error}\n')
		pass
	except dns.resolver.YXDOMAIN as error:
		logging.debug(f'YXDOMAIN-{error}\n')
		pass
	except dns.resolver.NoNameservers as error:
		logging.debug(f'NoNameservers-{error}\n')
		pass
	except Exception as error:
		logging.debug(f'Script Error-{error}\n')
	
	return dc_lst


def main():
	'''Main function to be used when calling getdc.py 
	
	Keyword arguments:
	args.domain -- Domain Name (required, accepted list or single value, default none)
	args.nameserver -- NameServer (optional, accepted hostname/ipaddress, default none)
	args.format -- Format output type, (required, accepted values json/host/ip/hostip'NameServer, default json)
	args.verbose -- Toggle debug meesages to stdout (required, accepted values boolean)
	args.exchange -- Toggle whether to look up exchange records (required, default false)
	'''
	# Arguments from argparse
	args = arguments.parse_args()

	# python logger
	if args.verbose:
		logging.basicConfig(level=logging.DEBUG)
	else:
		pass

	# DomainController dictionary
	dc_dct = {
	}

	# Run func query()
	for domain in args.domain:
		dc_dct[domain] = {} # initiate nested dict(s) from args.domain
		answer_srv = query(domain, service='_kerberos.', protocol='_tcp.', recordtype='SRV', nameserver=args.nameserver) # call query(srv) to find dc hostname
		
		for hostname in answer_srv:
			dc_dct[domain][str(hostname)] = '' # populat dc_dict with hostname
			answer_a = query(hostname, service='', protocol='', recordtype='A', nameserver=args.nameserver) # call query(a) to find dc ipaddress
			ipaddress = '\n'.join(answer_a) # convert list to string
			dc_dct[domain][str(hostname)] = ipaddress # populate dc_dict with ipaddress
	
	# Dev exchange
	if args.exchange:
		print('[Dev] Exchange servers ')
		answer_srv = query(domain, service='_autodiscover.', protocol='_tcp.', recordtype='SRV', nameserver=args.nameserver) # call query(srv) to find exchange hostname
		print(answer_srv, '\n')
	
	# format type output json
	if args.format == 'json': # stdout json
		json_data = json.dumps(dc_dct, indent=4, sort_keys=True) # convert dc_dict to json
		print(json_data)
	# format type output
	for domain in args.domain:
		if args.format == 'host':
			for key in sorted(dc_dct[domain].keys()): # stdout hostname
				print(key)
		if args.format == 'ip': 
			for value in sorted(dc_dct[domain].values()): # stdout ipaddress
				print(value)
		if args.format == 'hostip':
			for key, value in sorted(dc_dct[domain].items()): # stdout hostname/ipaddress
				print(key, value)


if __name__ == "__main__":
	main()
