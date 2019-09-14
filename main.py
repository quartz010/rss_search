import rss
import elastic 
if __name__ == "__main__":
    #items = rss.parse_rss('https://blog.12ms.xyz/feed')
    #items = rss.parse_rss('https://www.centos.bz/feed/')
    #elastic.es_index(items)
    elastic.es_search("卡夫卡")
    #elastic._es_chk_exist(u'Kafka 简单部署使用sdsdsd指北')