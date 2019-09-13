import feedparser
import ssl
import json

ssl._create_default_https_context = ssl._create_unverified_context

# d = feedparser.parse('https://blog.12ms.xyz/feed/')
d = feedparser.parse('https://rsshub.app/dysfz')

# print(json.dumps(dict(d)))
print(d.feed.title)
print(d.channel.title)
print(d.feed.link)
print(d.feed.subtitle)
print(d.channel.description)

print('items length is %d' % (len(d['entries']),))

try:
    print(list(map( lambda x: {'title': x.title, 'link': x.link, 'author': x.author, 'description': x.description, 'tags': list(map(lambda y: y['term'] ,x.tags))}, d.entries)))
except (KeyError,AttributeError) as e:
    try:
        print(list(map( lambda x: {'title': x.title, 'link': x.link, 'description': x.description}, d.entries)))
    except (KeyError,AttributeError) as identifier:
        print(repr(e))
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


