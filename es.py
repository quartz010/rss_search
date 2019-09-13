import elasticsearch as es
import datetime

body = dict({"test":"test"} ,**{"timestamp": datetime.datetime.utcnow()})
es = es.Elasticsearch(['sgk:9200'])
rst = es.index(index='test', body=body, id=None)
print(rst['result'])