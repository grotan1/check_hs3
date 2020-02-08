#!/usr/bin/env python
# encoding=utf8
############################## check_hs3 ########################
# Date: Feb 02 2020
# Author: Geir Rune Grøtan
# Help: https://github.com/grotan1/check_hs3
# Licence: MIT License - https://tldrlegal.com/license/mit-license
#################################################################
#
# Help : ./check_hs3.py -h
#
# Dependencies: pip install requests


import json
import requests
import sys
import argparse


def check_arg(args=None):
	parser = argparse.ArgumentParser(description="Check plugin to get device values from Homeseer 3")
	parser.add_argument("-H", "--host",
						 action='store',
						 dest="host",
						 help="HS3 host",
						 required='True')
	parser.add_argument("-d", "--devref",
						dest="devref",
						help="Comma-separated device ref (i.e: -d 70,181)",
						required='True',)
	parser.add_argument("-j", "--jsonstr",
						dest="jsonstr",
						help="HS3 JSON string (default: -j /JSON?request=getstatus&ref=)",
						default="/JSON?request=getstatus&ref=")
	parser.add_argument("-w", "--warn",
						dest="warn",
						help="Comma-separated Warning value (i.e: -w 22,23)",
						default="")
	parser.add_argument("-c", "--crit",
						dest="crit",
						help="Comma-separated Critical value (i.e: -c 25,26)",
						default="")
	parser.add_argument("-mx", "--max",
						dest="max",
						help="Comma-separated Max value (i.e: -mx 40,45)",
						default="")
	parser.add_argument("-mn", "--min",
						dest="min",
						help="Comma-separated Minimum value (i.e: -c 25,26)",
						default="")
	parser.add_argument("-sym", "--symbol",
						dest="symbol",
						help="Device type (i.e: -sym ºC)",
						default="")
	parser.add_argument("-s", "--ssl",
						action='store_true',
						help="Use ssl")
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
			results.max,
			results.min,
			results.symbol,
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
	value = 0.0
	name = ''
	graphitepath = ''
	url = 'HTTP://'
	h,d,j,w,c,mx,mn,sym,ssl,u,p = check_arg(sys.argv[1:])




	if ssl is True:
		url = "HTTPS://"

	try:
		r = requests.get(url+h+j+d,auth=(u,p))
		if r.status_code != 200:
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
	warnlist = w.split(",")
	critlist = c.split(",")
	maxlist = mx.split(",")
	minlist = mn.split(",")

	if status is None:
		for x in range(0,len(devlist)):
			try:
				value = float(j["Devices"][x]["value"])
				name = str(j["Devices"][x]["name"].encode('utf-8'))
			except IndexError:
				note = "Reference ID",devlist[x],"not found"
				status = UNKNOWN
				break

			try:
				crit = float(critlist[x])
			except:
				crit = ""

			try:
				warn = float(warnlist[x])
			except:
				warn = ""

			try:
				max = float(maxlist[x])
			except:
				max = ""
			try:
				min = float(minlist[x])
			except:
				min = ""

			if value != "" and crit != "":
				if value >= crit:
					status = CRITICAL

			if value != "" and warn != "":
				if value >= warn:
					status = WARNING

			if status is None:
				status = OK

			if status != UNKNOWN:
				note += '%s: %s%s ' % (name, value, sym)
				if perf_data is None:
					perf_data = "%s=%s;%s;%s;%s;%s" % (graphitepath+name, value, warn, crit,min,max)
				elif perf_data is not None:
					perf_data += (' %s=%s;%s;%s;%s;%s' % (graphitepath+name, value, warn, crit,min,max))

	if status != UNKNOWN and perf_data:
		print ('HS3 %s %s | %s' % (short_status[status], note, perf_data))
	else:
		print ('HS3 %s %s' % (short_status[status], note))
	sys.exit(status)

if __name__ == '__main__':
	main()


