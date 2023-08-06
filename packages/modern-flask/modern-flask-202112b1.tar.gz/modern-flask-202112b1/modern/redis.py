import redis
from flask import Flask, g
from opentelemetry.instrumentation.redis import RedisInstrumentor
from redis import Redis


def redis_client() -> redis.Redis:
    return g.redis_client


def setup_redis(app: Flask):
    RedisInstrumentor().instrument()

    args = app.config.get_namespace("REDIS_")
    client = Redis(**args)

    @app.before_request
    def do_before_request():
        g.redis_client = client
