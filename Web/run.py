from flask import Flask
from flask import render_template
from flask import request
from flask import abort
from flask import current_app


def create_app():
    import models, routes, services
    app = Flask(__name__)
    models.init_app(app)
    routes.init_app(app)
    services.init_app(app)
    return app


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/v2')
def index():
    return render_template('JT.html')

@app.route('/v3')
def table():
    return render_template('table.html')

@app.route('/api')
def get_es():
    import json
    def es_rand():
        HOSTP = "sgk:9200"
        
        POST_COUNT = 10
        import elasticsearch
        es = elasticsearch.Elasticsearch([HOSTP])
        res = es.search(index='test', body={"from": 0,"size": POST_COUNT,"query": {"match_all": {}},"sort":{"_script": {"script": "Math.random()","type": "number", "order": "asc"}}})
        res_list = list()
        for hit in res['hits']['hits']:
            try:
                #print(dict(hit["_source"], **{"_score" :hit["_score"]}))
                res_list.append(dict(hit["_source"], **{"_score" :hit["_score"]}))
            except KeyError as e:
                print(repr(e))
        return res_list
    res_list = es_rand()
    return json.dumps(res_list)

@app.route('/api2',  methods=['POST', 'GET'])
def search_es():
    import json
    def es_search(kword):
        HOSTP = "sgk:9200"

        import elasticsearch
        es = elasticsearch.Elasticsearch([HOSTP])
        import json
        #res = es.search(index="test", body={"query": {"match_all": {}}})
        #res = es.search(index="test", q="author : *")
        res = es.search(index="test", q="author : {kword} or title : {kword} or description : {kword}".format(kword=kword))
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
    if request.method == 'GET':
        try:
            res_list = es_search(request.args.get('q', ''))
        except Exception as e:
            current_app.logger.info(repr(e))
            abort(500)

    return json.dumps(res_list)
    

if __name__ == '__main__':
    app.run(debug=True)