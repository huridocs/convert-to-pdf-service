import os
import pathlib
from pathlib import Path
from ServiceConfig import ServiceConfig

config = ServiceConfig()


class DocumentFile:
    def __init__(self, namespace: str):
        path = Path(os.path.dirname(os.path.realpath(__file__)))
        self.root_folder = path.parent.absolute()
        self.namespace = namespace

    def save(self, document_file_name: str, file: bytes):
        sourceFolder = "source_documents"

        if not os.path.exists(config.paths[sourceFolder]):
            os.mkdir(config.paths[sourceFolder])

        if not os.path.exists(f'{config.paths[sourceFolder]}/{self.namespace}'):
            os.mkdir(f'{config.paths[sourceFolder]}/{self.namespace}')

        path = f'{config.paths[sourceFolder]}/{self.namespace}/{document_file_name}'

        file_path_document = pathlib.Path(path)
        file_path_document.write_bytes(file)
