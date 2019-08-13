__author__ = 'R.Azh'


from celery import Celery

# todo: to run celery execute the following commands in your terminal :
# todo: 1- first cd to TestProject folder something like: cd /<path tho your projects folder>/TestProject
# todo:  ** on my pc the path is here /home/azh/Programming/Repositories/TestProjects
# todo: 2- celery -A parsadp worker --app=TestPython.test_celery.test_celery_rabbitmq -l debug
# todo: run this file


celery_app = Celery("tasks", broker='amqp://guest@localhost//')


@celery_app.task
def add(x, y):
    print("hello from test_celery_rabbitmq")
    print(x + y)
    return x + y


add(5, 3)
add.delay(8, 4)
