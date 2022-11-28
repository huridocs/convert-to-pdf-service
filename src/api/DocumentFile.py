import os
import pathlib
from pathlib import Path

APP_PATH = Path(__file__).parent.absolute()
DATA_PATH = f"{APP_PATH}/../data"
DOCUMENT_SOURCES_PATH = f"{DATA_PATH}/source_documents"
PDF_PROCESSED_PATH = f"{DATA_PATH}/processed_pdfs"
DOCUMENT_FAILED = f"{DATA_PATH}/failed_documents"

CONFIG = {
    "app": APP_PATH,
    "data": DATA_PATH,
    "source_documents": DOCUMENT_SOURCES_PATH,
    "processed_pdfs": PDF_PROCESSED_PATH,
    "failed_documents": DOCUMENT_FAILED,
}


class DocumentFile:
    def __init__(self, namespace: str):
        path = Path(os.path.dirname(os.path.realpath(__file__)))
        self.root_folder = path.parent.absolute()
        self.namespace = namespace

    def save(self, document_file_name: str, file: bytes):
        source_folder = CONFIG["source_documents"]

        if not os.path.exists(CONFIG[source_folder]):
            os.mkdir(CONFIG[source_folder])

        if not os.path.exists(f'{CONFIG[source_folder]}/{self.namespace}'):
            os.mkdir(f'{CONFIG[source_folder]}/{self.namespace}')

        path = f'{CONFIG[source_folder]}/{self.namespace}/{document_file_name}'

        file_path_document = pathlib.Path(path)
        file_path_document.write_bytes(file)
