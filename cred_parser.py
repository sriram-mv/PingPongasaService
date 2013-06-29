import os

def parse():
	creds={}
	with open('credentials.conf') as cred_open:
		lines = [line.strip() for line in cred_open]
		for line in lines:
			total_creds = line.split('=')
			creds[total_creds[0]] = total_creds[1]
	return creds

credentials = parse()