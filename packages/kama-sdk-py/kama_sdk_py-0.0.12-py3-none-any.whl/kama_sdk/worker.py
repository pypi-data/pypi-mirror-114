import os

import redis
from rq import Worker, Connection

from kama_sdk.core.core import consts

redis_url = os.getenv('WORK_REDIS_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

def start_main():
  _start(consts.MAIN_WORKER, consts.TELEM_WORKER)


def start_telem():
  _start(consts.TELEM_WORKER)


def _start(*queue_names: str):
  with Connection(conn):
    worker = Worker(
      queues=queue_names,
      connection=conn
    )
    worker.work()
