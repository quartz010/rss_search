# -*- coding:utf-8 -*-
 
from bs4 import BeautifulSoup
import urllib.request
import re

"""
  简单的一个爬虫，很简单，抓取页面a标签，判断是否同源
  把不同源入队，搜索 feed等路径。
"""
 
#如果是网址，可以用这个办法来读取网页
#html_doc = "http://tieba.baidu.com/p/2460150866"
#req = urllib.request.Request(html_doc)  
#webpage = urllib.request.urlopen(req)  
#html = webpage.read()


html="""
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="xiaodeng"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
<a href="http://example.com/lacie" class="sister" id="xiaodeng">Lacie</a>
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
# soup = BeautifulSoup(html, 'html.parser')   #文档对象
# print(html) 
 
#查找a标签,只会查找出一个a标签
#print(soup.a)#<a class="sister" href="http://example.com/elsie" id="xiaodeng"><!-- Elsie --></a>
 


'''
本来考虑是使用树状自建来进行爬取的，不过，发现没那个必要。
'''




def search_for_cross(url):
    import requests

    def find_cross_url(html_str, site_url): 
        """
            拿到网站的所有非同源链接
        """
        import re
        soup = BeautifulSoup(html_str, 'html.parser')   #文档对象
        if site_url == "http://":
            return []
        # 找不到通用方法出此下策
        if site_url.count('.') == 2:
            site_kword = re.findall(re.compile(r'[.](.*)[.]', re.S) , site_url)[0]
        else:
            site_kword = re.findall(re.compile(r'^(.*)[.]', re.S) , site_url)[0]
        # print(html_str)
        hrefs = list()
        for k in soup.find_all('a'):
            try:
                excluding = ['weibo', 'github', 'twitter', 'google', 'youtube', 'linkedin', 'facebook','csdn','aliyun', 'hexo' ,'gov', '163'
                        'oschinas', 'gitee', 'beian', 'zhihu', 'git'
                ]
                if list(filter(lambda x: x in k['href'], excluding)) == []:
                    hrefs.append(k['href'])
            except KeyError as e:
                # print(repr(e), k)
                pass
        # print(list(map(lambda x: x['href'], soup.find_all('a'))))
        return filter(lambda y: re.findall(re.compile(r'^(?!/)(.*)[.]', re.S), y) ,filter(lambda x: not re.findall(re.compile(site_kword), x), hrefs))
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    try:
        r = requests.get(url, headers=headers, timeout=5)
        html = r.text
        url = r.url
    except Exception as e:
        print(repr(e))
        html = ''
    res = list(find_cross_url(html, url))

    return res

# rst = search_for_cross('http://wwxiong.com/')
# print(len(rst), rst)
def get_domain(url):
    import sys
    if sys.version < '3':
        from urlparse import urlparse
    else:
        from urllib.parse import urlparse
    url = url
    parse_result = urlparse(url)
    return parse_result.netloc

res_list = ['https://carey.akhack.com/']
# res_list = ['https://blog.12ms.xyz/']

i = 0

def try_feed_link(domain):
    import requests
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    try:
        r = requests.get(domain, headers=headers, timeout=5)
        html = r.text
    except Exception as e:
        print(repr(e))
        html = ''
    soup = BeautifulSoup(html, 'html.parser')   #文档对象
    hrefs = list()
    for k in soup.find_all('a'):
        try:
            hrefs.append(k['href'])
            # print(hrefs)
        except KeyError as e:
            # print(repr(e), k)
            pass
    res = list(filter(lambda x: re.match(r".*\.xml$", x), hrefs))
    # feed_urls = ['/feed', '/atom.xml', 'rss', '']
    return res[0] if res != [] else ""


def fetch_xml(res_list):
    for i in res_list:
        feed_str = try_feed_link(i)
        if feed_str:
            if 'http://' not in feed_str and 'https://' not in feed_str:
                print(i+feed_str)
                f.write(i+feed_str+'\n')
            else:
                print(feed_str)
                f.write(feed_str+'\n')
        else:
            pass

f = open('out.log','a+') 
while True:
    # res_list += map(lambda x: dict({'url':x, 'status':False}) ,search_for_cross(res_list[i]))
    res_list += list(map(lambda x: 'http://'+get_domain(x), search_for_cross(res_list[i])))
    # res_list += list(search_for_cross(res_list[i]))
    res_list = list(set(res_list))
    print(res_list, len(res_list))
    i = i + 1
    print(i)
    if i % 10 == 0:
        fetch_xml(res_list)
        # 释放内存防止oom
        res_list = res_list[10:] 
    if i >= len(res_list):
        break
    # if len(res_list)>10:
    #     break
print(res_list, len(res_list))

# print(list(map(lambda x: x+try_feed_link(x), res_list)))
