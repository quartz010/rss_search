# -*- coding: UTF-8
def parse_rss(feed_url):
    import datetime
    import json
    import feedparser
    import ssl
    import re
    def rm_not_exist(code_str, err_item):
        """
            用于自动的尝试哪些字段需要解析，
            比较Hack的方法
        """
        from functools import reduce
        err_item = re.compile("'(.*)'").findall(repr(e))[0]
        #err_end = code_str.find(err_item)
        #err_pos = code_str.rfind("  ", err_end)
        #print(err_item, err_pos, err_end)
        #code_str = code_str[:err_end-1]+code_str[err_pos+1:]
        items = code_str.split('  ')
        items = list(filter(lambda x: err_item not in x, items))
        #print(items)
        # 这里需要使用双空格，加至原形态
        return reduce(lambda x, y: x+'  '+y, items)
    
    # 这里需要设置ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    d = feedparser.parse(feed_url)
    # d = feedparser.parse('https://rsshub.app/dysfz')
    # print(json.dumps(dict(d)))
    try:
        #print(d.feed.title)
        #print(d.channel.title)
        #print(d.feed.link)
        #print(d.feed.subtitle)
        #print(d.channel.description) 

        feed_info = {
            "feed_title": d.feed.title,
            "feed_link":  d.feed.link,
            "feed_desc":  d.feed.description,
            "feed_src": feed_url,
            "author": d.feed.author
        }
    except (KeyError,AttributeError) as e:
        print('no such key:' + re.compile("'(.*)'").findall(repr(e))[0])
        err_item = re.compile("'(.*)'").findall(repr(e))[0]
        code_str = '{"feed_title":d.feed.title,  "feed_link":d.feed.link,  "feed_desc":d.feed.description,  "author": d.feed.author,  }'

        for _ in range(len(code_str.split('  '))):
            try:
                code_str = rm_not_exist(code_str, err_item)
                feed_info = eval(code_str)                
            except AttributeError as e:
                    err_item = re.compile("'(.*)'").findall(repr(e))[0]
                    continue
            break

        pass
    print('feed_info')
    print('items length is %d' % (len(d['entries']),))
    rst = list()
    try:
        # 这里去除html标签 防止解析，并且限制字符长度
        for i in range(len(d.entries)):
            # 保留完全desc 提高搜索精度 
            feed_info['details'] = re.compile(r'<[^>]+>',re.S).sub('',d.entries[i].description)    
            d.entries[i].description = feed_info['details'][:64]

        rst = list(map( lambda x: dict({'title': x.title, 'link': x.link, 'author': x.author, 'description': x.description, 'tags': list(map(lambda y: y['term'] ,x.tags))}, **feed_info), d.entries))
    except (KeyError,AttributeError) as e:
        print('no such key:' + re.compile("'(.*)'").findall(repr(e))[0])

        err_item = re.compile("'(.*)'").findall(repr(e))[0]
        code_str = "{'title':x.title,  'link':x.link,  'author':x.author,  'description':x.description,  'tags':list(map(lambda y:y['term'],x.tags))  }"

        for _ in range(len(code_str.split('  '))):
            try:
                code_str = rm_not_exist(code_str, err_item)
                # 判断逻辑
                if err_item == "author" and feed_info.get('author') == '': 
                    feed_info['author'] = "unknown"

                rst = list(map( lambda x: dict(eval(code_str), **feed_info), d.entries))
                    
            except AttributeError as e:
                    err_item = re.compile("'(.*)'").findall(repr(e))
                    continue
            break

        # print(rst)

    return rst
    # for item in d.entries:
    #     print('item title = %s' % (item.title,))
    #     print('item link = %s' % (item.link,))
    #     print('item author = %s' % (item.author,))
    #     print('item summary = %s' % (item.summary,))

    #     tags = []
    #     for tag in item.tags:
    #         tags.append(tag.term)
    #     print('item\'s tags = %s ' % (','.join(tags),))

    #     print('item\'s updated time = ',item.updated_parsed)


