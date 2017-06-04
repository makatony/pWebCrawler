import os  # allows to work with folder


def createProjectDir(directory):
    if not os.path.exists(directory):
        print('creating project ' + directory)
        os.makedirs(directory)


# create queue and crawled files (if not created)
def createDataFiles(projectName, baseUrl):
    queue = projectName + '/queue.txt'
    crawled = projectName + '/crawled.txt'
    if not os.path.isfile(queue):
        writeFile(queue, baseUrl)
    if not os.path.isfile(crawled):
        writeFile(crawled, '')


# create new file
def writeFile(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()


# add data onto an existing file
def appendToFile(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')
    # documentation on "with": http://effbot.org/zone/python-with-statement.htm
    # it performs __enter__ code in "open()", thne the body below, then the __exit__ code inside "open()"
    # i.e. the __exit__ method in open() just closes the file


def deleteFileContents(path):
    with open(path, 'w'):
        pass  # opening the file, then doing nothing. i.e. clears the file


# set vs list: set can only have unique elements
# Read a file and conert each line to set items
def fileToSet(fileName):
    results = set()
    with open(fileName, 'rt') as f:
        for line in f:
            # removing the newLine \n char
            results.add(line.replace('\n', ''))
    return results


# iterate through a set, each tem will be a new line in the file
def setToFile(links, targetFile):
    deleteFileContents(targetFile)
    for link in sorted(links):
        appendToFile(targetFile, link)
