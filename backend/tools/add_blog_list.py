# -*- coding: UTF-8
import sys
sys.path.append("..")
from mods import rss
from mods import elastic
import json
import sys
import queue
import threading
import time


exitFlag = 0
 
class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
   
 
    def process_data(self, threadName, q):
        while not exitFlag:
            queueLock.acquire()
            if not workQueue.empty():
                data = q.get()
                queueLock.release()
                rss2es(data)
                print("%s processing %s" % (threadName, data))
            else:
                queueLock.release()
            time.sleep(1)

    def run(self):
            print("Starting " + self.name)
            self.process_data(self.name, self.q)
            print("Exiting " + self.name)

def rss2es(rss_url):
    items = rss.parse_rss(rss_url)
    elastic.es_bulk_index(items)


if __name__ == "__main__":
    # 用来解决编码问题
    if sys.version < "3":
        reload(sys)
        sys.setdefaultencoding('utf8')

    if len(sys.argv) < 2:
        print(sys.argv[0] +' <url>')
        exit()
    rss_urls = open(sys.argv[1], 'r').readlines()

    threadList = ["Thread-1", "Thread-2", "Thread-3"]
    nameList = rss_urls
    # nameList = ['2' , '3' , '500','500']

    queueLock = threading.Lock()
    workQueue = queue.Queue()
    threads = []
    threadID = 1
    
    # 创建新线程
    for tName in threadList:
        thread = myThread(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1
    
    # 填充队列
    queueLock.acquire()
    for word in nameList:
        workQueue.put(word)
    queueLock.release()
    
    # 等待队列清空
    while not workQueue.empty():
        pass
    
    # 通知线程是时候退出
    exitFlag = 1
    
    # 等待所有线程完成
    for t in threads:
        t.join()
    print("Exiting Main Thread")

            #elastic.es_index(items)
    #res_list = elastic.es_search("卡夫卡")
    #open('res.json', "w+").write(json.dumps(res_list))
    #elastic._es_chk_exist(u'Kafka 简单部署使用sdsdsd指北')
    #elastic.es_rand()


