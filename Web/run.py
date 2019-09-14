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

if __name__ == '__main__':
    app.run(debug=True)