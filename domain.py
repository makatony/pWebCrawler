# trying to handle subdomains like a.b.c.page.com
from urllib.parse import urlparse


# get domain na,e (example.com)
def getDomainName(url):
    try:
        results = getSubDomainName(url).split('.')
        # results[-2] returns second to last item in array
        return results[-2] + '.' + results[-1]
    except:
        return ''


# Get sub domain name (name.example.com)
def getSubDomainName(url):
    try:
        return urlparse(url).netloc  # net loc = network location
    except:
        return ''
