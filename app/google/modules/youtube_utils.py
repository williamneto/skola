#
# Functions of utils.py adapted for
# search Youtube
#

from __future__ import unicode_literals

import time
from selenium import webdriver
import urllib2
from functools import wraps
# import requests
from urllib import urlencode



def _get_search_url(query):
	params = {
		"search_query": query.encode('utf8')
	}
	params = urlencode(params)

	url = u"https://www.youtube.com/results?" + params

	return url