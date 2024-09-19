import logging
import os

from pydantic import ValidationError
from queue_processor.QueueProcessor import QueueProcessor
from sentry_sdk import start_transaction
from sentry_sdk.integrations.redis import RedisIntegration
import sentry_sdk

from src.config import REDIS_HOST, REDIS_PORT, QUEUES_NAMES
from .models import Message, Task
from .convert_to_pdf import convert_to_pdf

SERVICE_URL = f"{os.environ.get('SERVICE_HOST')}:{os.environ.get('SERVICE_PORT')}"


def process(message):
    logger = logging.getLogger(__name__)
    with start_transaction(op="task", name="convert_to_pdf"):
        try:
            task = Task(**message)
        except ValidationError:
            logger.error(f"Not a valid message: {message}")
            return None

        logger.info(f"Valid message: {message}")

        try:
            logger.info(f"Converting to PDF {task.params.filename}")
            processed_pdf_filepath = convert_to_pdf(
                task.params.filename, task.params.namespace
            )

            logger.info(f"Converted to PDF {task.params.filename}")

            if not processed_pdf_filepath:
                message = Message(
                    namespace=task.params.namespace,
                    task=task.task,
                    params=task.params,
                    success=False,
                    error_message="Error during pdf convert",
                )
                logger.error(f"Error during pdf convert {task.params.filename}")
                logger.error(message.json())
                return message.dict()

            file_name = "".join(task.params.filename.split(".")[:-1])
            processed_pdf_url = (
                f"{SERVICE_URL}/processed_pdf/{task.params.namespace}/{file_name}.pdf"
            )

            message = Message(
                namespace=task.params.namespace,
                task=task.task,
                params=task.params,
                success=True,
                file_url=processed_pdf_url,
            )

            logger.info(message.json())
            return message.dict()
        except Exception as exception:
            logger.exception(exception)
            return None


if __name__ == "__main__":
    try:
        sentry_sdk.init(
            os.environ.get("SENTRY_CONVERT_TO_PDF_DSN"),
            traces_sample_rate=0.1,
            environment=os.environ.get("ENVIRONMENT", "development"),
            integrations=[RedisIntegration()],
        )
    except Exception:
        pass

    logger = logging.getLogger(__name__)
    queues_names = QUEUES_NAMES.split(" ")
    queue_processor = QueueProcessor(REDIS_HOST, REDIS_PORT, queues_names, logger)
    queue_processor.start(process)
