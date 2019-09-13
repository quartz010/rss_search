import elasticsearch as es

body = {"test":"test"}
es = Elasticsearch(['localhost:9200'])
es.index(index='indexName', doc_type='typeName', body, id=None)
