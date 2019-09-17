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
 







def search_for_cross(url):
    import requests
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    def find_cross_url(html_str, site_url): 
        """
            拿到网站的所有非同源链接
        """
        import re
        soup = BeautifulSoup(html_str, 'html.parser')   #文档对象
        # 找不到通用方法出此下策
        if site_url.count('.') == 2:
            site_kword = re.findall(re.compile(r'[.](.*)[.]', re.S) , site_url)[0]
        else:
            site_kword = re.findall(re.compile(r'^(.*)[.]', re.S) , site_url)[0]
        # print(html_str)
        hrefs = list()
        for k in soup.find_all('a'):
            try:
                hrefs.append(k['href'])
            except KeyError as e:
                # print(repr(e), k)
                pass
        # print(list(map(lambda x: x['href'], soup.find_all('a'))))
        return filter(lambda y: re.findall(re.compile(r'^(?!/)(.*)[.]', re.S), y) ,filter(lambda x: not re.findall(re.compile(site_kword), x), hrefs))
    r = requests.get(url, headers=headers)
    res = list(find_cross_url(r.text, r.url))
    return res

# rst = search_for_cross('http://wwxiong.com/')
# print(len(rst), rst)

res_list = ['http://wwxiong.com/']
res_list = ['https://blog.12ms.xyz/']

i = 0

while True:
    # res_list += map(lambda x: dict({'url':x, 'status':False}) ,search_for_cross(res_list[i]))
    res_list += search_for_cross(res_list[i])
    print(res_list)

    res_list = list(set(res_list))
    print(res_list)
    i = i + 1
    print(i)
    if i > 10:
        print("11")
        break

print(res_list, len(res_list))


