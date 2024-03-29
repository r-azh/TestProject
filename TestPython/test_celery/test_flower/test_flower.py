# pip install flower
# Launch the server and open http://localhost:5555
#
# flower -A proj --port=5555
# Or, launch from Celery
#
# celery flower -A proj --address=127.0.0.1 --port=5555
# Broker URL and other configuration options can be passed through the standard Celery options
#
# celery flower -A proj --broker=amqp://guest:guest@localhost:5672//
