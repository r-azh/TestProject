def test_create_task(celery_app, celery_worker):
    @celery_app.task
    def mul2(x, y):
        return x * y

    celery_worker.reload()
    assert mul2.delay(4, 4).get(timeout=50) == 16