__author__ = 'R.Azh'

import logging

from celery import Celery

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

app = Celery('tasks', broker='redis://localhost:6379/0')
app.conf.CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# for fibo tasks
input_list = [4, 3, 8, 6, 10]

# for web crawler tasks
url_list = ['http://www.google.com',
            'http://www.bing.com',
            # 'http://duckduckgo.com',
            # 'http://github.com',
            'http://search.yahoo.com']

# todo: to run celery execute the following commands in your terminal :
# todo: 1- run redis server with command: redis-server
# todo: 2- cd to TestProject folder something like: cd /<path tho your projects folder>/TestProject
# todo:  ** on my pc the path is /home/azh/Programming/Repositories/TestProjects/TestPython/parallel_programming_in_python/celery_ch7
# todo: 3- celery -A tasks worker -Q sqrt_queue,fibo_queue,webcrawler_queue --loglevel=info
# The preceding command initiates a Celery server, and by means of the -A parameter
# informs where the instance of application Celery is defined, and the implementation
# of the tasks.
# We did specify queues for each type of task.
# At the moment we start the Celery server in the server side, it will establish
# three different queues. These will now be seen and consumed by the workers.
# todo: run this file


def manage_sqrt_task(value):
    result = app.send_task('tasks.sqrt_task', args=(value,),
        queue='sqrt_queue', routing_key='sqrt_queue')
    res = result.get()
    print(res)
    logger.info(res)


def manage_fibo_task(value_list):
    async_result_dict = {x: app.send_task('tasks.fibo_task',
        args=(x,), queue='fibo_queue', routing_key='fibo_queue')
            for x in value_list}

    for key, value in async_result_dict.items():
        if value.ready():
            logger.info("Value [%d] -> %s" % (key, value.get()[1]))
        else:
            logger.info("The task [%s] is not ready" % value.task_id)


def manage_crawl_task(url_list):
    async_result_dict = {url: app.send_task('tasks.crawl_task',
        args=(url,), queue='webcrawler_queue', routing_key='webcrawler_queue')
            for url in url_list}

    for key, value in async_result_dict.items():
        logger.info("%s -> %s" % (key, value.get()))


if __name__ == '__main__':
    # manage_sqrt_task(4)
    manage_fibo_task(input_list)
    # manage_crawl_task(url_list)
