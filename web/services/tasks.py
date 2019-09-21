from . import celery

@celery.task(name='service.123')
def my_background_task(arg1, arg2):
    import time
    # some long running task here
    open('test.tim','r+').write(str(time.time()))
    print(123)