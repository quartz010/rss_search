

def parse_rss(feed_url):
    import datetime
    import json
    import feedparser
    import ssl

    ssl._create_default_https_context = ssl._create_unverified_context
    d = feedparser.parse('https://blog.12ms.xyz/feed/')
    # d = feedparser.parse('https://rsshub.app/dysfz')



    # print(json.dumps(dict(d)))
    print(d.feed.title)
    print(d.channel.title)
    print(d.feed.link)
    print(d.feed.subtitle)
    print(d.channel.description)
    feed_info = {
        "feed_title":  d.feed.title,
        "feed_link":  d.feed.link,
        "feed_desc": d.feed.description,
        "timestamp": datetime.now()
    }
    print('items length is %d' % (len(d['entries']),))
    rst = list()
    try:
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


print(parse_rss("sa"))