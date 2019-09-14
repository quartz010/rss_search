import elasticsearch
import datetime

es = elasticsearch.Elasticsearch(['sgk:9200'])

def _es_chk_exist(title):
    """
        用呀判断是否条目已存在的函数，这里会是一个性能瓶颈，需要进行单条的遍历
    """
    res = es.search(index="test", q="title : \"{kword}\"".format(kword=title))
    return False if res['hits']['total']['value'] == 0 else True

def es_index(bodys):

    es = elasticsearch.Elasticsearch(['sgk:9200'])
    bodys = list(filter(lambda x: not  _es_chk_exist(x['title']), bodys))
    print(bodys)
    for body in bodys:
        body = dict(body ,**{"timestamp": datetime.datetime.utcnow()})
        rst = es.index(index='test', body=body, id=None)
        print(rst['result'])


def es_search(kword):
    import json
    es = elasticsearch.Elasticsearch(['sgk:9200'])
    #res = es.search(index="test", body={"query": {"match_all": {}}})
    #res = es.search(index="test", q="author : *")
    res = es.search(index="test", q="author : {kword} or title : {kword} or description : {kword}".format(kword=kword))
    print("Got %d Hits:" % res['hits']['total']['value'])
    #open('es.json', "w+").write(json.dumps(res))
    for hit in res['hits']['hits']:
        try:
            #print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
            print(hit["_source"], hit["_score"])
        except KeyError as e:
            print(repr(e))

    #rst = es.get(index="test", id=1)
    #print(rst)