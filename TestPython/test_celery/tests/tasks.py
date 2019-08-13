from celery import Celery

# broker_url = 'redis://localhost:6379/0'
# result_backend = 'redis://localhost/0'

broker_url = 'amqp://localhost:5672/'
result_backend = 'rpc://'
celery_app = Celery("tasks", broker=broker_url, backend=result_backend)


@celery_app.task(name="add")
def add(x, y):
    print("add from tasks")
    print(x + y)
    return x + y


@celery_app.task(name="mul")
def mul(x, y):
    print("mul from tasks")
    print(x * y)
    return x * y