#coding=utf-8
import sys
import urllib.request
import re
import webbrowser

file = None
auto_open = True
keys = []
topic_url_prefix=""
url_fmt= topic_url_prefix + "forum-230-%d.html"


def analysisOnePage(url):
    content = getPageContent(url)
    topics = getTopics(content)
    
    for topic in topics:
        url, title= getInfosFromTopic(topic)
        if hasKeyString(title):
            writeToFile(title, url)
            webOpen(url)
            
            
def getPageContent(url):
    wp = urllib.request.urlopen(url)
    all = wp.read()
    content = str(all.decode('gbk','ignore'))
    return content
    
def getTopics(content):
    start_from = '版块主题'
    start = content.index(start_from)
    start = -start
    content = content[-start:]
    
    pattern = re.compile('''<span id="thread_\d*"><a href="thread-\d*-\d*-\d*.html".*</a></span>''',re.I)
    return re.findall(pattern, content)

def getInfosFromTopic(topic):
    pattern = re.compile('''<span id="thread_\d*"><a href="(thread-\d*-\d*-\d*.html)".*>(.*)</a></span>''',re.I)
    res = pattern.search(topic).groups()
    return topic_url_prefix + res[0], res[1]
    
def hasKeyString(title):
    for key in keys:
        if title.find(key) > -1:
            return True
    return False
    
def writeToFile(title, url):
    file.write(title + '\n' + url + '\n\n')
    
def webOpen(url):
    if auto_open:
        webbrowser.open_new_tab(url)
    

if __name__ == '__main__':
    file = open("result.txt", 'w+')
    [analysisOnePage(url_fmt % i) for i in range(1,10)]
    file.close()

    