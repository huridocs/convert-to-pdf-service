import os
import shutil
import pathlib
import subprocess

from config import CONFIG

THIS_SCRIPT_PATH = pathlib.Path(__file__).parent.absolute()
DATA_PATH = f"{THIS_SCRIPT_PATH}/../data"


def get_paths(namespace: str, pdf_file_name: str):
    file_name = "".join(pdf_file_name.split(".")[:-1])
    source_document_filepath = (
        f'{CONFIG["source_documents"]}/{namespace}/{pdf_file_name}'
    )
    processed_pdf_dir = f'{CONFIG["processed_pdfs"]}/{namespace}'
    processed_pdf_filepath = f"{processed_pdf_dir}/{file_name}.pdf"
    failed_documents_filepath = (
        f'{CONFIG["failed_documents"]}/{namespace}/{pdf_file_name}'
    )
    return (
        source_document_filepath,
        processed_pdf_dir,
        processed_pdf_filepath,
        failed_documents_filepath,
    )


def convert_to_pdf(filename, namespace):
    (
        source_document_filepath,
        processed_pdf_dir,
        processed_pdf_filepath,
        failed_documents_filepath,
    ) = get_paths(namespace, filename)
    os.makedirs(f"/{processed_pdf_dir}", exist_ok=True)

    result = subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            processed_pdf_dir,
            source_document_filepath,
        ]
    )

    if result.returncode == 0:
        os.remove(source_document_filepath)
        return processed_pdf_filepath

    if not os.path.exists(f'{CONFIG["failed_documents"]}/{namespace}'):
        os.makedirs(f'{CONFIG["failed_documents"]}/{namespace}', exist_ok=True)
    shutil.move(source_document_filepath, failed_documents_filepath)
    return False
