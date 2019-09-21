# -*- coding: UTF-8
import sys
from .. import models
import json
import sys

if __name__ == "__main__":
    # 用来解决编码问题
    if sys.version < "3":
        reload(sys)
        sys.setdefaultencoding('utf8')

    #items = rss.parse_rss('https://blog.12ms.xyz/feed')
    #items = rss.parse_rss('https://www.centos.bz/feed/')
    #items = rss.parse_rss('http://liyangliang.me/index.xml')
    #print(items)
    #items = rss.parse_rss('http://www.bjhee.com/index.xml')
    #items = rss.parse_rss("http://luokangyuan.com/rss/")
    if len(sys.argv) < 2:
        print(sys.argv[0] +' <url>')
        exit()
    items = models.rss.parse_rss(sys.argv[1])
    #items = rss.parse_rss('https://jerryzou.com/feed')
    #items = rss.parse_rss('https://www.centos.bz/feed/')
    
    models.elastic.es_index(items, 'test')
    #res_list = elastic.es_search("卡夫卡")
    #open('res.json', "w+").write(json.dumps(res_list))
    #elastic._es_chk_exist(u'Kafka 简单部署使用sdsdsd指北')
    #elastic.es_rand()
