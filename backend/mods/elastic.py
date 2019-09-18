# -*- coding: UTF-8
import elasticsearch
import datetime
import time
from elasticsearch import helpers
es = elasticsearch.Elasticsearch(['sgk:9200'])

def _es_chk_exist(title):
    """
        用来判断是否条目已存在的函数，这里会是一个性能瓶颈，需要进行单条的遍历
    """
    res = es.search(index="test", q="title : \"{kword}\"".format(kword=title))
    return False if res['hits']['total']['value'] == 0 else True

def es_index(bodys):

    bodys = list(filter(lambda x: not  _es_chk_exist(x['title']), bodys))
    print('add:' +str(len(bodys)))
    for body in bodys:
        body = dict(body ,**{"timestamp": datetime.datetime.utcnow()})
        rst = es.index(index='test', body=body, id=None)
        print(rst['result'])

def es_bulk_index(bodys):
        print('add:' +str(len(bodys)))
        start_time = time.time()
        actions = list(map(lambda x: {"timestamp": datetime.datetime.utcnow(), "_index": "rss_by_crawler","_source": x}, bodys))
        res = helpers.bulk(es, actions)
        end_time = time.time()
        print("{} {}s".format(res, end_time - start_time))

def es_index_search(_index,kword):
    import json
    #res = es.search(index="test", body={"query": {"match_all": {}}})
    #res = es.search(index="test", q="author : *")
    
    # 查询语句需要修改一下，很傻
    # res = es.search(index="test", q="author : {kword} or title : {kword} or description : {kword}".format(kword=kword))
        
    #res = es.search(index=_index, body={"query": {"multi_match" : {"query" : kword,"fields": ["_all"],"fuzziness": "AUTO"}}})
    res = es.search(index=_index, body={"query": {"multi_match" : {"query" : kword, "fuzziness": "AUTO"}}})
    
    print("Got %d Hits:" % res['hits']['total']['value'])
    #open('es.json', "w+").write(json.dumps(res))
    res_list = list()
    for hit in res['hits']['hits']:
        try:
            #print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
            print(dict(hit["_source"], **{"_score" :hit["_score"]}))
            res_list.append(dict(hit["_source"], **{"_score" :hit["_score"]}))
        except KeyError as e:
            print(repr(e))
    return res_list

def es_search(kword):
    import json
    #res = es.search(index="test", body={"query": {"match_all": {}}})
    #res = es.search(index="test", q="author : *")
    
    # 查询语句需要修改一下，很傻
    # res = es.search(index="test", q="author : {kword} or title : {kword} or description : {kword}".format(kword=kword))
        
    res = es.search(index="test", body={"query": {"multi_match" : {"query" : kword,"fuzziness": "AUTO"}}})
    
    print("Got %d Hits:" % res['hits']['total']['value'])
    #open('es.json', "w+").write(json.dumps(res))
    res_list = list()
    for hit in res['hits']['hits']:
        try:
            #print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
            print(dict(hit["_source"], **{"_score" :hit["_score"]}))
            res_list.append(dict(hit["_source"], **{"_score" :hit["_score"]}))
        except KeyError as e:
            print(repr(e))
    return res_list
    #rst = es.get(index="test", id=1)
    #print(rst)

def es_rand():
    res = es.search(index='test', body={"from": 0,"size": 1,"query": {"match_all": {}},"sort":{"_script": {"script": "Math.random()","type": "number", "order": "asc"}}})
    res_list = list()
    for hit in res['hits']['hits']:
        try:
            #print(dict(hit["_source"], **{"_score" :hit["_score"]}))
            res_list.append(dict(hit["_source"], **{"_score" :hit["_score"]}))
        except KeyError as e:
            print(repr(e))
    print(res_list)
    return res_list