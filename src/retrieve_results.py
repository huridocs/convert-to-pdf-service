from rsmq import RedisSMQ

import os

host = os.environ.get('REDIS_HOST', 'localhost')
queue = RedisSMQ(host=host, port=6379, qname='convert-to-pdf_results', quiet=True)
results_message = queue.receiveMessage().exceptions(False).execute()
print(results_message)
results_message = queue.receiveMessage().exceptions(False).execute()
print(results_message)
results_message = queue.receiveMessage().exceptions(False).execute()
print(results_message)
results_message = queue.receiveMessage().exceptions(False).execute()
print(results_message)
results_message = queue.receiveMessage().exceptions(False).execute()
print(results_message)
results_message = queue.receiveMessage().exceptions(False).execute()
print(results_message)
results_message = queue.receiveMessage().exceptions(False).execute()
print(results_message)
