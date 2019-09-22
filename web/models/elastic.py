# -*- coding: UTF-8
import elasticsearch
import datetime
import time
from elasticsearch import helpers

ES_HOST = 'sgk:9200'
es = elasticsearch.Elasticsearch([ES_HOST])

def time_me(fn):
    u'''
    函数耗时修饰器
    '''
    def _wrapper(*args, **kwargs):
        start = time.clock()
        ret = fn(*args, **kwargs)
        print(u"%s cost %s second"%(fn.__name__, time.clock() - start))
        return ret
    return _wrapper


def _es_chk_exist(_index, _title):
    """
        用来判断是否条目已存在的函数，这里会是一个性能瓶颈，需要进行单条的遍历
    """
    res = es.search(index=_index, q="title : \"{kword}\"".format(kword=_title))
    return False if res['hits']['total']['value'] == 0 else True

def es_index(_bodys, _index='test'):
    bodys = list(filter(lambda x: not _es_chk_exist(_index, x['title']), _bodys))
    print('add:' +str(len(bodys)))
    for body in bodys:
        body = dict(body ,**{"timestamp": datetime.datetime.utcnow()})
        rst = es.index(index=_index, body=body, id=None)
        print(rst['result'])

@time_me
def _es_chk_id_exist(_index, _id):
    """
        用来判断是否条目已存在的函数，现在直接使用 HEAD 比前面的轮询好一点
    """
    import requests
    res = requests.head("http://"+ES_HOST+'/'+_index+'/_doc/'+_id)
    return False if res.status_code == 404 else True

def gen_es_id(org_str):
    import hashlib
    hash_str = hashlib.md5(org_str.encode("utf-8")).hexdigest()
    return hash_str

@time_me
def es_bulk_index(_bodys, _index='test'):
    # 新函数使用ID作为唯一索引
    bodys = list(filter(lambda x: not _es_chk_id_exist(_index, gen_es_id(x['title'])), _bodys))
    print('add:' +str(len(bodys)))
    # 给每一项补充时间戳
    bodys = list(map(lambda x: dict(x ,**{"timestamp": datetime.datetime.utcnow()}), bodys))
    # 使用自定义的MD5ID
    actions = list(map(lambda x: {"_index": _index,"_id": gen_es_id(x['title']) ,"_source": x}, bodys))
    res = helpers.bulk(es, actions)
    print(res)

def es_index_search(_index,kword):
    import json
    #res = es.search(index="test", body={"query": {"match_all": {}}})
        
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
            # print(dict(hit["_source"], **{"_score" :hit["_score"]}))
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
            print(dict({'title':hit["_source"]['title']}, **{"_score" :hit["_score"]}))
            res_list.append(dict(hit["_source"], **{"_score" :hit["_score"]}))
        except KeyError as e:
            print(repr(e))
    return res_list
    #rst = es.get(index="test", id=1)
    #print(rst)

def es_rand():
    """
        随机返回部分的查询结果
    """
    res = es.search(index='test', body={"from": 0,"size": 20,"query": {"match_all": {}},"sort":{"_script": {"script": "Math.random()","type": "number", "order": "asc"}}})
    res_list = list()
    for hit in res['hits']['hits']:
        try:
            #print(dict(hit["_source"], **{"_score" :hit["_score"]}))
            res_list.append(dict(hit["_source"], **{"_score" :hit["_score"]}))
        except KeyError as e:
            print(repr(e))
    print(res_list)
    return res_list

def es_get_all_feed_src():
    body = {"size":0,"aggs" : {"rsss" : {"terms" : { "field" : "feed_src.keyword" }}}}
    res = es.search(index='test', body=body)
    print("Got %d Hits:" % res['hits']['total']['value'])
    print(res['es_get_all_feed_src']['rsss']['buckets'])



