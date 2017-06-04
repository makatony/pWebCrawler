from urllib.request import urlopen
from linkFinder import LinkFinder
from general import *
import sys
import traceback


class Spider:

    # Class variables (shared amongst all instances of this class)
    projectName = ''
    baseUrl = ''
    domainName = ''
    crawledFile = ''
    queueFile = ''  # on HD queue

    queue = set()  # in memory queue
    crawled = set()

    def __init__(self, projectName, baseUrl, domainName):
        Spider.projectName = projectName  # defining the class variable for all spiders
        Spider.baseUrl = baseUrl
        Spider.domainName = domainName
        Spider.queueFile = Spider.projectName + '/queue.txt'
        Spider.crawledFile = Spider.projectName + '/crawled.txt'

        # this __init__ only runs once when the class is loaded to memory
        # i.e. the boot and the crawlpage is only done once for the first spider
        Spider.boot()
        # send first spider to crawl
        Spider.crawlPage('First Spider', Spider.baseUrl)  # will be multithreaded later

    @staticmethod  # means this is a method for the class, not used for the instances
    def boot():
        createProjectDir(Spider.projectName)
        createDataFiles(Spider.projectName, Spider.baseUrl)
        Spider.queue = fileToSet(Spider.queueFile)
        Spider.crawled = fileToSet(Spider.crawledFile)

    @staticmethod
    def crawlPage(threadName, pageUrl):
        if pageUrl not in Spider.crawled:  # making sure that the pageURl wasnt yet crawled
            print(threadName + ' crawling ' + pageUrl)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled ' + str(len(Spider.crawled)))
            Spider.addLinksToQueue(Spider.gatherLinks(pageUrl))  # adds link to the waiting list that all spiders can see

            # move next page to the crawled list as we are now crawling it
            Spider.queue.remove(pageUrl)
            Spider.crawled.add(pageUrl)
            Spider.updateFiles()

    @staticmethod
    def addLinksToQueue(links):
        for url in links:
            # check that the link is not yet in crawled or queue
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            if Spider.domainName not in url:  # not crawling the links in the website pointing to youtube etc
                continue
            Spider.queue.add(url)  # adds this link to the queue

    @staticmethod
    def gatherLinks(pageUrl):
        htmlString = ''
        try:
            response = urlopen(pageUrl)
            if response.getheader('Content-type') == 'text/html':
                htmlBytes = response.read()  # raw response
                htmlString = htmlBytes.decode('utf-8')
            finder = LinkFinder(Spider.baseUrl, pageUrl)
            finder.feed(htmlString)
        except:
            print('Error: cant crawl page ' + pageUrl)
            print("Oops!", sys.exc_info()[0], "occured.")
            print(traceback.format_exc())
            return set()
        return finder.pageLinks()

    @staticmethod
    def updateFiles():
        setToFile(Spider.queue, Spider.queueFile)
        setToFile(Spider.crawled, Spider.crawledFile)
