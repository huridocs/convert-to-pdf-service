from rsmq import RedisSMQ
import os

host = os.environ.get("REDIS_HOST", "localhost")

queue = RedisSMQ(host=host, port=6379, qname="convert-to-pdf_tasks", quiet=True)
message_json = '{"tenant": "new-namespace", "task": "convert-to-pdf", "params": {"filename": "form.png", "namespace": "document"}}'
queue.sendMessage().message(message_json).execute()
