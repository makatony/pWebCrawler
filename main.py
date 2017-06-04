import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *
from linkFinder import LinkFinder

PROJECTNAME = 'thenewboston'
HOMEPAGE = 'http://thenewboston.com/'
DOMAINNAME = getDomainName(HOMEPAGE)
QUEUEFILE = PROJECTNAME + '/queue.txt'
CRAWLEDFILE = PROJECTNAME + '/crawled.txt'
NUMBEROFTHREADS = 8

threadQueue = Queue()
Spider(PROJECTNAME, HOMEPAGE, DOMAINNAME)


# create worker threads (will die when main exists)
def createWorkers():
    for _ in range(NUMBEROFTHREADS):
        t = threading.Thread(target=work)  # start 8 threads that run the "work()" function
        t.daemon = True  # dies when main exists
        t.start()


# do next job in the queue
def work():
    while True:
        url = threadQueue.get()
        Spider.crawlPage(threading.current_thread().name, url)
        threadQueue.task_done()


# each queued link is a new job
def createJobs():
    for link in fileToSet(QUEUEFILE):
        threadQueue.put(link)
    threadQueue.join()
    crawl()


# check if there are items in queue and crawl them
def crawl():
    queuedLinks = fileToSet(QUEUEFILE)
    if len(queuedLinks) > 0:
        print(str(len(queuedLinks)) + ' links in the queue')
        createJobs()


createWorkers()
crawl()
