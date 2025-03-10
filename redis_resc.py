from redis import Redis
from rq import Queue

# Connect to Redis (Make sure Redis is running)
redis_conn = Redis(host='localhost', port=6379, decode_responses=True)

# Create an RQ queue
redis_queue = Queue(connection=redis_conn)
