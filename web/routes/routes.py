from ..models import elastic

from . import main
from flask import render_template
from flask import request
from flask import abort
from flask import current_app

import json



@main.route('/')
def hello_world():
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
            current_app.logger.info(repr(e))
            abort(500)
    return json.dumps(res_list)