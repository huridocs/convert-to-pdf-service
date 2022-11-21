import os

import redis
from pydantic import ValidationError
from rsmq.consumer import RedisSMQConsumer
from rsmq import RedisSMQ
from sentry_sdk.integrations.redis import RedisIntegration
import sentry_sdk

from ServiceConfig import ServiceConfig
from Message import Message

from Task import Task
from convert_to_pdf import convert_to_pdf


class QueueProcessor:
    def __init__(self):
        self.config = ServiceConfig()
        self.logger = self.config.get_logger("queue_processor")

        self.results_queue = RedisSMQ(
            host=self.config.redis_host,
            port=self.config.redis_port,
            qname=self.config.results_queue_name,
        )

    def process(self, id, message, rc, ts):
        try:
            task = Task(**message)
        except ValidationError:
            self.logger.error(f"Not a valid message: {message}")
            return True

        self.logger.info(f"Valid message: {message}")

        try:
            self.logger.info(f"Converting to PDF {task.params.filename}")
            processed_pdf_filepath = convert_to_pdf(
                task.params.filename, task.params.namespace
            )

            self.logger.info(f"Converted to PDF {task.params.filename}")

            if not processed_pdf_filepath:
                message = Message(
                    tenant=task.params.namespace,
                    task=task.task,
                    params=task.params,
                    success=False,
                    error_message="Error during pdf convert",
                )
                self.logger.error(f"Error during pdf convert {task.params.filename}")

                self.results_queue.sendMessage().message(
                    message.dict()
                ).execute()
                self.logger.error(message.json())
                return True

            file_name = "".join(task.params.filename.split(".")[:-1])
            processed_pdf_url = f"{self.config.service_url}/processed_pdf/{task.params.namespace}/{file_name}.pdf"

            message = Message(
                tenant=task.params.namespace,
                task=task.task,
                params=task.params,
                success=True,
                file_url=processed_pdf_url,
            )

            self.logger.info(message.json())
            self.results_queue.sendMessage(delay=3).message(
                message.dict()
            ).execute()
            return True
        except Exception:
            self.logger.error("error", exc_info=1)
            return True

    def subscribe_to_tasks_queue(self):
        self.results_queue.createQueue().vt(120).exceptions(False).execute()
        tasks_queue = RedisSMQ(
            host=self.config.redis_host,
            port=self.config.redis_port,
            qname=self.config.tasks_queue_name,
        )

        tasks_queue.createQueue().vt(120).exceptions(False).execute()

        self.logger.info(
            f"Connecting to Redis: {self.config.redis_host}:{self.config.redis_port}"
        )
        try:
            redis_smq_consumer = RedisSMQConsumer(
                qname=self.config.tasks_queue_name,
                processor=self.process,
                host=self.config.redis_host,
                port=self.config.redis_port,
            )
            self.logger.info("Connected to Redis.")
            redis_smq_consumer.run()
        except redis.exceptions.ConnectionError:
            self.logger.error(
                f"Error connecting to Redis: {self.config.redis_host}:{self.config.redis_port}"
            )


if __name__ == "__main__":
    try:
        sentry_sdk.init(
            os.environ.get("SENTRY_PDF_CONVERT_DSN"),
            traces_sample_rate=0.1,
            environment=os.environ.get("ENVIRONMENT", "production"),
            integrations=[RedisIntegration()],
        )
    except Exception:
        pass

    redis_tasks_processor = QueueProcessor()
    redis_tasks_processor.subscribe_to_tasks_queue()
