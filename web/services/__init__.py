from flask import Blueprint
from celery import Celery

#celery = object()
def init_app(app):
    pass

# tasks = Blueprint('task', __name__)

# print(tasks.config)
celery = Celery('services', broker='redis://sgk:6379/0')
celery.conf.update({
    'CELERY_BROKER_URL':'redis://sgk:6379/0',
    'CELERY_RESULT_BACKEND':'redis://sgk:6379/0'
})