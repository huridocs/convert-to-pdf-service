from pathlib import Path

APP_PATH = Path(__file__).parent.absolute()
DATA_PATH = f"{APP_PATH}/../data"
DOCUMENT_SOURCES_PATH = f"{DATA_PATH}/source_documents"
PDF_PROCESSED_PATH = f"{DATA_PATH}/processed_pdfs"
DOCUMENT_FAILED = f"{DATA_PATH}/failed_documents"

CONFIG = {
    "source_documents": DOCUMENT_SOURCES_PATH,
    "processed_pdfs": PDF_PROCESSED_PATH,
}