import os
import pathlib

from fastapi import UploadFile

from src.config import CONFIG


class DocumentFile:

    def save(self, file: UploadFile, namespace: str):
        source_folder = CONFIG["source_documents"]

        if not os.path.exists(source_folder):
            os.mkdir(source_folder)

        if not os.path.exists(f"{source_folder}/{namespace}"):
            os.mkdir(f"{source_folder}/{namespace}")

        path = f"{source_folder}/{namespace}/{file.filename}"

        file_path_document = pathlib.Path(path)
        file_path_document.write_bytes(file.file.read())
