from rsmq import RedisSMQ

queue = RedisSMQ(host='localhost', port=6379, qname='convert-to-pdf_tasks', quiet=True)
message_json = '{"tenant": "new-namespace", "task": "convert-to-pdf", "params": {"filename": "Staff Input - Executive Director - HURIDOCS.docx", "namespace": "document"}}'
queue.sendMessage().message(message_json).execute()