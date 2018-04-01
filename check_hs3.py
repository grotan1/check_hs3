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
						help="HS3 device ref (ex: -d 70)",
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
						help="Device type. (ex: -dt °C)",
						default="")						
						
	results = parser.parse_args(args)
    
	return (results.host,
            results.devref,
            results.jsonstr,
			results.warn,
			results.crit,
			results.devtype)


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
		
	h,d,j,w,c,dt = check_arg(sys.argv[1:])
	
	try:
		r = requests.get(h+j+d)
	except requests.exceptions.RequestException as e:
		note = e
		status = UNKNOWN
	
	if status is None:
		try:
			j = r.json()
		except ValueError:
			note = 'Decoding JSON has failed'
			status = UNKNOWN
	
	if status is None:
		try:
			value = float(j["Devices"][0]["value"])
			name = j["Devices"][0]["name"].encode('utf-8')
		except IndexError:
			note = "Reference ID",d,"not found"
			status = UNKNOWN
	
	try: 
		crit = float(c)
	except ValueError:
		crit = ""
		
	try: 
		warn = float(w)
	except ValueError:
		warn = ""
		
	if value >= crit:
		status = CRITICAL
	
	elif value >= warn:
		status = WARNING	
	
	if status is None:
		status = OK
		
	if status != UNKNOWN:
		note = '%s: %s %s' % (name, value, dt)
		perf_data = '%s=%s;%s;%s' % (name, value, w, c)
	
	if status != UNKNOWN and perf_data:
		print '%s %s | %s' % (short_status[status], note, perf_data)
	else:
		print '%s %s' % (short_status[status], note)
	sys.exit(status)	
	
#	print value


if __name__ == '__main__':
	main()


