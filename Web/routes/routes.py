from flask import render_template
from flask import app

@app.route('/')
def hello_world():
    return 'Hello World!'