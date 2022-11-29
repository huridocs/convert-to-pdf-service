import io
import json
import time
import unittest
import requests
from pathlib import Path

from PyPDF2 import PdfReader
from rsmq import RedisSMQ


class EndToEnd(unittest.TestCase):
    def test_test(self):
        namespace = "tenant-name"
        file_name = "file-sample_1MB.docx"
        service_url = "http://127.0.0.1:5060"
        file_path = f"{Path(__file__).parent.absolute()}/test_files/{file_name}"

        with open(file_path, "rb") as file:
            files = {"file": file}
            requests.post(f"{service_url}/upload/{namespace}", files=files)

        message = self.get_redis_message()
        if message.get('error_message'):
            self.fail(message)
        response = requests.get(message["file_url"])

        self.assertEqual(200, response.status_code)

        pdf = PdfReader(io.BytesIO(response.content))
        text = pdf.pages[0].extract_text()

        self.assertEqual(message['namespace'], 'tenant-name')
        self.assertIsNotNone(pdf)
        self.assertIn("Lorem ipsum", text)

    @staticmethod
    def get_redis_message():
        queue = RedisSMQ(
            host="127.0.0.1", port="6379", qname="convert-to-pdf_results", quiet=True
        )

        for _ in range(50):
            time.sleep(1)
            message = queue.receiveMessage().exceptions(False).execute()
            if message:
                queue.deleteMessage(id=message["id"]).execute()
                return json.loads(message["message"])

        return json.loads('{}')


if __name__ == "__main__":
    unittest.main()
