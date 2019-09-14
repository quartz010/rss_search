

def parse_rss(feed_url):
    import datetime
    import json
    import feedparser
    import ssl
    import re

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
        }
    except (KeyError,AttributeError) as e:
        print(repr(e))
        feed_info = {
            "feed_title": d.feed.title,
            "feed_link":  d.feed.link,
        }
        pass
    print('items length is %d' % (len(d['entries']),))
    rst = list()
    try:
        # 这里去除html标签 防止解析，并且限制字符长度
        for i in range(len(d.entries)):
            d.entries[i].description = re.compile(r'<[^>]+>',re.S).sub('',d.entries[i].description)[:64]

        rst = list(map( lambda x: dict({'title': x.title, 'link': x.link, 'author': x.author, 'description': x.description, 'tags': list(map(lambda y: y['term'] ,x.tags))}, **feed_info), d.entries))
    except (KeyError,AttributeError) as e:
        try:
            rst = list(map( lambda x: dict({'title': x.title, 'link': x.link, 'description': x.description}, **feed_info), d.entries))
        except (KeyError,AttributeError) as e:
            print(repr(e))

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


