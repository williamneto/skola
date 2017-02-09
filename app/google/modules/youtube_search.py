from __future__ import unicode_literals

from utils import get_html
from youtube_utils import _get_search_url
from bs4 import BeautifulSoup
import urlparse
from urllib2 import unquote
from unidecode import unidecode
from re import match

class YoutubeResult:

	""" Represents a youtube search result """

	def __init__(self):
		self.name = None  # The title of the youtube video 
		self.link = None  # The link of the youtube video
		self.thumb = None  # The thumbnail of the youtube video

	def __repr__(self):
		name = unidecode(self.name)

		list_youtube = ["YoutubeResult(",
						"name={}".format(name), "\n", " " * 13] 

		return "".join(list_youtube)


# PUBLIC
def search(query, void=True):
	""" Return a list of YoutubeResult """

	results = []
	url = _get_search_url(query)
	html = get_html(url)

	if html:
		soup = BeautifulSoup(html, "html.parser")
		ol = soup.find_all("div", attrs={"class": "yt-lockup"})
		
		for li in ol:
			res = YoutubeResult()

			res.name = _get_name(li)
			res.link = _get_link(li)
			res.thumb = _get_thumb(li)

			results.append(res)

	return results

# PRIVATE
def _get_name(li):
	a = li.find("a", attrs={"class": "yt-uix-tile-link"})

	if a is not None:
		return a.text.strip()
	return None

def _get_link(li):
	a = li.find("a", attrs={"class": "yt-uix-tile-link"})
	link = a["href"]

	return link

def _get_thumb(li):
	a = li.find("span", attrs={"class": "yt-thumb-simple"})
	img = a.find("img")["src"]

	return img
	


