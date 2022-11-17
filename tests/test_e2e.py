import json
import time
import unittest
from pathlib import Path

import requests
from rsmq import RedisSMQ


class EndToEnd(unittest.TestCase):
    def test_test(self):
        namespace = "documents"
        file_name = "file-sample_1MB.docx"
        service_url = "http://127.0.0.1:5050"
        file_path = f'{Path(__file__).parent.absolute()}/test_files/{file_name}';

        with open(file_path, "rb") as file:
            files = {"file": file}
            requests.post(f"{service_url}/upload/{namespace}", files=files)

        queue = RedisSMQ(host="127.0.0.1", port="6379", qname="convert-to-pdf_tasks")
        # task = json.loads('{"task": "convert-to-pdf", "params": {"filename": file-sample_1MB.docx, "namespace": documents}}')

        queue.sendMessage().message(
            '{"task": "convert-to-pdf", "params": {"filename": "file-sample_1MB.docx", "namespace": "documents"}}'
        ).execute()

        message = self.get_redis_message()
        print(message);

        response = requests.get(f"{service_url}/processed_pdf/documents/file-sample_1MB.pdf")

        # response = requests.get(message['file_url'])
        self.assertEqual(200, response.status_code)
        # self.assertEqual(task.params, message.params)

        # with pdfplumber.open(io.BytesIO(response.content)) as pdf:
        #     first_page = pdf.pages[0]
        #     return first_page.extract_text()

        self.assertIsNotNone(file)


    @staticmethod
    def get_redis_message():
        queue = RedisSMQ(host="127.0.0.1", port="6379", qname="convert-to-pdf_results")

        for i in range(50):
            time.sleep(0.5)
            message = queue.receiveMessage().exceptions(False).execute()
            if message:
                queue.deleteMessage(id=message["id"]).execute()
                return json.loads(message["message"])



if __name__ == '__main__':
    unittest.main()
