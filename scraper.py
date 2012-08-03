#!/usr/bin/python
# -*- coding: utf-8 -*-

####################################################################################
#
# Basicly same idea as Passcracker.py, only this generates a baseword list. 
# Only reads 1MB from password.txt and choose a random word to search for. 
#
####################################################################################

import json
import urllib2
import re
import sys
import random
import subprocess
import unicodedata
import os

def unique(words):
	array = []
	[array.append(x.encode('utf-8')) for x in words if x not in array and (len(x) > 3 and len(x) < 16)]
	return array

def twitter(query):
	data = json.loads(urllib2.urlopen("http://search.twitter.com/search.json?q=%s&rpp=1000"%query).read())
	array = []

	for tweet in data['results']:
		filterurl = re.sub(r"""((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.‌​][a-z]{2,4}/)(?:[^\s()<>]+|(([^\s()<>]+|(([^\s()<>]+)))*))+(?:(([^\s()<>]+|(‌​([^\s()<>]+)))*)|[^\s'!()[]{};:'".,<>?«»""'']))""", ' ', tweet['text'])
		filterspecial = unicodedata.normalize('NFKD', re.sub(r"""[^\w]|_""", ' ',filterurl)).encode('ascii', 'ignore')
		array.extend(re.split(r"""\s+""", filterspecial))
	return array

def randomword():
	readfile = os.open('password.txt', os.O_RDONLY)
	words = random.choice(filter(None, [line.strip() for line in os.read(readfile, 100000).split('\n')]))
	return words

if __name__ == "__main__":	
		
		while 1:
			try:
				word = randomword()
				print "\nSearching for:",word
				wordlist = unique(twitter(word))
				print wordlist			
				
				for i in xrange(len(wordlist)):				
					open("password.txt", "a").write("%s\n"%wordlist[i])

			except (KeyboardInterrupt, SystemExit):
				sys.exit(sys.stderr.write("Bai Bai\n"))
			except:
				pass
