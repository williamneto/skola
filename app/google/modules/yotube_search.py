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
		name = self._limit_str_size(self.name, 55)

		list_youtube = ["YoutubeResult(",
						"name={}".format(name), "\n", " " * 13] 

		return "".join(list_youtube)

    def _limit_str_size(self, str_element, size_limit):
        """Limit the characters of the string, adding .. at the end."""
        if not str_element:
            return None

        elif len(str_element) > size_limit:
            return unidecode(str_element[:size_limit]) + ".."

        else:
            return unidecode(str_element)

# PUBLIC
def search(query, void=True):
	""" Return a list of YoutubeResult """

	results = []
	url = _get_search_url(query)
	html = get_html(url)

	if html:
		soup = BeautifulSoup(html, "html.parser")
		ol = soup.findAll("ol", attrs={"class": "item-section"})

		for li in divs:
			res = YoutubeResult()

			res.name = _get_name(li)
			# res.link = _get_link(li)
			# res.thumb = _get_thumb(li)

			results.append(res)

	return results

# PRIVATE
def _get_name(li):
	a = li.find("span", attrs={"class": "accessible-description"})

	if a is not None:
		return a.text.strip()
	return None


