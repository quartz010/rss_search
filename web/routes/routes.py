from ..models import elastic
from ..services import tasks

from . import main
from flask import render_template
from flask import request
from flask import abort
from flask import current_app

import json



@main.route('/')
def hello_world():
    tasks.my_background_task.apply_async(args=[10, 20])
    return 'Hello World!'


@main.route('/v2')
def index():
    return render_template('JT.html')

@main.route('/api')
def get_es():
    res_list = elastic.es_rand()
    return json.dumps(res_list)

@main.route('/api2',  methods=['POST', 'GET'])
def search_es():
    
    if request.method == 'GET':
        try:
            res_list = elastic.es_search(request.args.get('q', ''))
        except Exception as e:
            current_app.logger.error(repr(e))
            abort(500)
    return json.dumps(res_list)

@main.route('/rss',  methods=['POST','GET'])
def add_rss():
    if request.method == 'GET':
        try:
            res_list = elastic.es_search(request.args.get('q', ''))
        except Exception as e:
            current_app.logger.error(repr(e))
            abort(500)
        res = json.dumps(res_list)
    
    if request.method == 'POST':
        try:
            import redis  
            feed_src = request.form['feed_src']
            r = redis.Redis(host='localhost', port=6379, decode_responses=True, db=1) 
            r.rpush('feed_list',feed_src)

        except Exception as e:
            current_app.logger.error(repr(e))
            abort(500)
        res = json.dumps({"ok": True})
    return res