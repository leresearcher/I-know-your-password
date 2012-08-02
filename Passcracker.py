#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import urllib2
import re
import sys
import random
import subprocess
import unicodedata
import os

def sizepasswordfile():

	filesize = os.stat('password.txt').st_size
	return filesize

def unique(words):
	array = []
	[array.append(x.encode('utf-8')) for x in words if x not in array and (len(x) > 4 and len(x) < 16)]
	return array

def twitter(query):
	data = json.loads(urllib2.urlopen("http://search.twitter.com/search.json?q=%s&rpp=1000"%query).read())
	array = []

	for tweet in data['results']:
		filterurl = re.sub(r"""((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.‌​][a-z]{2,4}/)(?:[^\s()<>]+|(([^\s()<>]+|(([^\s()<>]+)))*))+(?:(([^\s()<>]+|(‌​([^\s()<>]+)))*)|[^\s'!()[]{};:'".,<>?«»""'']))""", ' ', tweet['text'])
		filterspecial = unicodedata.normalize('NFKD', re.sub(r"""[^\w]|_""", ' ',filterurl)).encode('ascii', 'ignore')
		array.extend(re.split(r"""\s+""", filterspecial))
	return array

if __name__ == "__main__":

	err = sys.stderr.write

	if len(sys.argv) != 2:
    		sys.exit(err("Usage: python %s <hash list> \n" % (sys.argv[0],)))
  	else:

		while 1:
			try:
				words = [line.strip() for line in open('keywords.txt')]
			   	wordlist = unique(twitter(random.choice(words)))			

				print wordlist
				print "Filesize:", sizepasswordfile()
				for i in xrange(len(wordlist)):				
					f = open("password.txt", "a").write("%s\n"%wordlist[i])

				if sizepasswordfile() > 200000:

############################################################optional##############################################################
					print "Running Passwordpro & combinator rules...."
					hashcat = subprocess.Popen(["optirun","./hashcat/cudaHashcat-plus64.bin","--remove","--rules-file","hashcat/rules/passwordspro.rule", "--rules-file","hashcat/rules/combinator.rule","--outfile", "crackme.out", sys.argv[1], "password.txt"], stdout=subprocess.PIPE).communicate()[0]
					print hashcat
					print "Running Leetspeak & Best64 rules...."
					hashcat = subprocess.Popen(["optirun","./hashcat/cudaHashcat-plus64.bin","--remove","--rules-file","hashcat/rules/best64.rule", "--rules-file","hashcat/rules/leetspeak.rule", "--outfile", "crackme.out", sys.argv[1], "password.txt"], stdout=subprocess.PIPE).communicate()[0]
					print hashcat
					print "Running generated Rules...."
					hashcat = subprocess.Popen(["optirun","./hashcat/cudaHashcat-plus64.bin","--remove","--rules-file","hashcat/rules/generated.rule", "--outfile", "crackme.out", sys.argv[1], "password.txt"], stdout=subprocess.PIPE).communicate()[0]
					print hashcat
					f = open("password.txt", "w").write("")
############################################################optional##############################################################
			except:
				pass

