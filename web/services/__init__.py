def init_app(app):
    pass
tasks = Blueprint('task', __name__)

celery = Celery(tasks.name, broker=tasks.config['CELERY_BROKER_URL'])
celery.conf.update(tasks.config)