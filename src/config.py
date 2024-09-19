import logging
import graypy
import os
from pathlib import Path

APP_PATH = Path(__file__).parent.absolute()
DATA_PATH = f"{APP_PATH}/../data"
DOCUMENT_SOURCES_PATH = f"{DATA_PATH}/source_documents"
PDF_PROCESSED_PATH = f"{DATA_PATH}/processed_pdfs"
DOCUMENT_FAILED = f"{DATA_PATH}/failed_documents"
GRAYLOG_IP = os.environ.get("GRAYLOG_IP")

REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")

QUEUES_NAMES = os.environ.get("QUEUES_NAMES", "convert-to-pdf")

CONFIG = {
    "source_documents": DOCUMENT_SOURCES_PATH,
    "processed_pdfs": PDF_PROCESSED_PATH,
    "failed_documents": DOCUMENT_FAILED,
}

handlers = [logging.StreamHandler()]
if GRAYLOG_IP:
    handlers.append(
        graypy.GELFUDPHandler(GRAYLOG_IP, 12201, localname="convert-to-pdf")
    )

logging.root.handlers = []
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=handlers,
)
