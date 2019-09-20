from flask import Flask

def create_app():
    from . import models, routes, services
    app = Flask(__name__)
    app.register_blueprint(routes.main)
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    models.init_app(app)
    routes.init_app(app)
    services.init_app(app)
    return app
