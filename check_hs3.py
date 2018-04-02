#!/usr/bin/env python
# encoding=utf8

import json
import requests
import sys
import argparse


def check_arg(args=None):
	parser = argparse.ArgumentParser(description="Check plugin to get device values from Homeseer 3")
	parser.add_argument("-H", "--host",
						 action='store',
						 dest="host",
						 help="HS3 host (ex: -H http://10.0.0.40)",
						 required='True')
	parser.add_argument("-d", "--devref",
						dest="devref",
						help="HS3 comma-separated device ref (ex: -d 70,181)",
						required='True')
	parser.add_argument("-j", "--jsonstr",
						dest="jsonstr", 
						help="HS3 JSON string (ex: -j /JSON?request=getstatus&ref=)",
						default="/JSON?request=getstatus&ref=")
	parser.add_argument("-w", "--warn",
						dest="warn",
						help="Warning value",
						default="")	
	parser.add_argument("-c", "--crit",
						dest="crit",
						help="Critical value",
						default="")
	parser.add_argument("-dt", "--devtype",
						dest="devtype",
						help="Device type (ex: -dt °C)",
						default="")
	parser.add_argument("-s", "--ssl",
						action='store_true',
						help="Use ssl (HTTPS://)")
	parser.add_argument("-u", "--username",
						dest="username",
						help="Username",
						default="")
	parser.add_argument("-p", "--password",
						dest="password",
						help="Password",
						default="")
						
	results = parser.parse_args(args)
    
	return (results.host,
            results.devref,
            results.jsonstr,
			results.warn,
			results.crit,
			results.devtype,
			results.ssl,
			results.username,
			results.password)


def main():	
	OK = 0
	WARNING = 1
	CRITICAL = 2
	UNKNOWN = 3
	short_status = {OK: 'OK',
					WARNING: 'WARN',
					CRITICAL: 'CRIT',
					UNKNOWN: 'UNK'}
					
	status = None
	note = ''
	perf_data = None
	value = ''
	name = ''
	url = 'HTTP://'	
	h,d,j,w,c,dt,ssl,u,p = check_arg(sys.argv[1:])
	
	if ssl is True:
		url = "HTTPS://"
	
	try:
		r = requests.get(url+h+j+d,auth=(u,p))
		if r.status_code is not 200:
			def userpass():
				return "Error 401: Wrong username or password"
			def notfound():
				return "Error 404: Not found"
			def forbidden():
				return "Error 403: Forbidden"		
			def timeout():
				return "Error 408: Request Timeout"				
			statuscode = {
				401 : userpass,
				404 : notfound,
				403 : forbidden,
				408 : timeout,
			}		
			note = statuscode.get(r.status_code, lambda : r.status_code)()
			status = UNKNOWN
					
	except requests.exceptions.RequestException as e:
		note = e
		status = UNKNOWN
	
	if status is None:
		try:
			j = r.json()
		except ValueError:
			note = 'Decoding JSON has failed'
			status = UNKNOWN
	
	devlist = d.split(",")
	if status is None:
		for x in range(0,len(devlist)):		
			try:
				value = float(j["Devices"][x]["value"])
				name = j["Devices"][x]["name"].encode('utf-8')
			except IndexError:
				note = "Reference ID",devlist[x],"not found"
				status = UNKNOWN
				break
	
			try: 
				crit = float(c)
			except ValueError:
				crit = ""
		
			try: 
				warn = float(w)
			except ValueError:
				warn = ""
		
			if value >= crit and value != '':
				status = CRITICAL
	
			elif value >= warn and value != '':
				status = WARNING	
	
			if status is None:
				status = OK
		
			if status != UNKNOWN:
				note += '%s: %s %s' % (name, value, dt)
				if perf_data is None:
					perf_data = '%s=%s;%s;%s' % (name, value, w, c)
				elif perf_data is not None:
					perf_data += ' %s=%s;%s;%s' % (name, value, w, c)
	
	if status != UNKNOWN and perf_data:
		print '%s %s | %s' % (short_status[status], note, perf_data)
	else:
		print '%s %s' % (short_status[status], note)
	sys.exit(status)	
	
if __name__ == '__main__':
	main()


