##  worker.py
##
##  This establishes the redis queue server to run the background processing
##  for the flask server.
##

#   Import os.
import os
#   Import redis for asynchronous tasks.
import redis
#   Import modules from rq.
from rq import Worker, Queue, Connection


#   Enables worker to always listen.
listen = ['default']

#   Sets where the worker will listen.
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
#   Sets the connection location.
conn = redis.from_url(redis_url)

#   Main method for the worker.
if __name__ == '__main__':
    # Establishes the connection.
    with Connection(conn):
        # Enables worker with queue and set to listen.
        worker = Worker(list(map(Queue, listen)))
        # Starts the worker.
        worker.work()

