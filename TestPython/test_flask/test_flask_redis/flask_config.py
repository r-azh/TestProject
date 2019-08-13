# REDIS_URL = "redis://:password@localhost:6379/0"

# To create the redis instance within your application

from flask import Flask
from flask_redis import FlaskRedis


app = Flask(__name__)
app.config['REDIS_URL'] = "redis://localhost:6379/0"

redis_store = FlaskRedis(app)
# or
# redis_store = FlaskRedis()
# redis_store.init_app(app)


