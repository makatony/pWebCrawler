from html.parser import HTMLParser
from urllib import parse


class LinkFinder(HTMLParser):  # linkFinder inherits from HTMLparser$

    def __init__(self, base_url, page_url):
        super().__init__()
        self.baseUrl = base_url
        self.pageUrl = page_url
        self.links = set()

    def handle_starttag(self, tag, attrs):  # overwriting the handle_startta from superclass
        if tag == 'a':
            for (attribute, value) in attrs:  # tuple with attr and value
                if attribute == 'href':
                    url = parse.urljoin(self.baseUrl, value)  # if value is already a full URL (http....), it keeps. otherwise it adds the http
                    self.links.add(url)

    def pageLinks(self):
        return self.links

    def error(self, message):
        pass
