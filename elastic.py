import elasticsearch
import datetime
def es_index(bodys):
    for body in bodys:
        body = dict(body ,**{"timestamp": datetime.datetime.utcnow()})
        es = elasticsearch.Elasticsearch(['sgk:9200'])
        rst = es.index(index='test', body=body, id=None)
        print(rst['result'])
        rst = es.get(index="test", id=1)
        print(rst)

def es_search(kword):
    es = elasticsearch.Elasticsearch(['sgk:9200'])
    #res = es.search(index="test", body={"query": {"match_all": {}}})
    #res = es.search(index="test", q="author : *")
    res = es.search(index="test", q="author : {kword} or title : {kword} or description : {kword}".format(kword=kword))
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        try:
            #print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
            print(hit["_source"])
        except KeyError as e:
            print(repr(e))