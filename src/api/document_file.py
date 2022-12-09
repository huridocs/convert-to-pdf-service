import os
import pathlib
from pathlib import Path

from src.config import CONFIG


class DocumentFile:
    def __init__(self, namespace: str):
        self.namespace = namespace

    def save(self, document_file_name: str, file: bytes):
        source_folder = CONFIG["source_documents"]

        if not os.path.exists(source_folder):
            os.mkdir(source_folder)

        if not os.path.exists(f"{source_folder}/{self.namespace}"):
            os.mkdir(f"{source_folder}/{self.namespace}")

        path = f"{source_folder}/{self.namespace}/{document_file_name}"

        file_path_document = pathlib.Path(path)
        file_path_document.write_bytes(file)
