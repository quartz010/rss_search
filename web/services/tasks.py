from . import celery
from ..models import elastic
from ..models import rss 

from celery.utils.log import get_task_logger
 
log = get_task_logger(__name__)

@celery.task
def my_background_task(arg1, arg2):
    import time
    # some long running task here
    open('test.tim','w+').write(str(time.time()))
    log.info('test')

@celery.task
def add_new_rss(feed_src):
    items = rss.parse_rss(feed_src)
    elastic.es_bulk_index(items, 'test')
    log.info('add_new_rss: %s' %feed_src)