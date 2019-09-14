from flask import Flask
from flask import render_template


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
    return render_template('index.html')

@app.route('/v3')
def table():
    return render_template('table.html')

@app.route('/api')
def get_es():
    import json
    def es_rand():
        import elasticsearch
        es = elasticsearch.Elasticsearch(['sgk:9200'])
        res = es.search(index='test', body={"from": 0,"size": 1,"query": {"match_all": {}},"sort":{"_script": {"script": "Math.random()","type": "number", "order": "asc"}}})
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
if __name__ == '__main__':
    app.run(debug=True)