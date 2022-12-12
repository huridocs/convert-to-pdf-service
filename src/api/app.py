import logging
import os
import sys
import json
from fastapi import FastAPI, HTTPException, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from sentry_sdk.integrations.redis import RedisIntegration
from starlette.status import HTTP_202_ACCEPTED
from rsmq import RedisSMQ

import sentry_sdk

from supported_files import check_file_support, FileNotSupported
from document_file import DocumentFile
from src.config import CONFIG

logger = logging.getLogger(__name__)

app = FastAPI()

logger.info("Convert to PDF service has started")

redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = os.environ.get("REDIS_PORT", "6739")

queue = RedisSMQ(
    host=redis_host,
    port=redis_port,
    qname="convert-to-pdf_tasks",
)

try:
    sentry_sdk.init(
        os.environ.get("SENTRY_CONVERT_TO_PDF_DSN"),
        traces_sample_rate=0.1,
        environment=os.environ.get("ENVIRONMENT", "development"),
        integrations=[RedisIntegration()],
    )
except Exception:
    pass


@app.get("/info")
async def info():
    logger.info("Convert to PDF info endpoint")

    content = jsonable_encoder({"service:": "Convert to PDF API", "sys": sys.version})
    return JSONResponse(content=content)


@app.get("/error")
async def error():
    message = "This is a test error from the error endpoint"
    logger.error(message)
    raise HTTPException(status_code=500, detail=message)


@app.post("/upload/{namespace}", status_code=HTTP_202_ACCEPTED)
async def upload_document(namespace: str, file: UploadFile):
    try:
        check_file_support(file.filename)
        document_file = DocumentFile()
        document_file.save(file, namespace)

        queue.sendMessage().message(
            json.dumps(
                {
                    "task": "convert-to-pdf",
                    "params": {"filename": file.filename, "namespace": namespace},
                }
            )
        ).execute()

        return "File uploaded"
    except FileNotSupported:
        message = f"Error uploading document {file.filename}"
        logger.exception(message)
        raise HTTPException(status_code=422, detail=message)


@app.get("/processed_pdf/{namespace}/{pdf_file_name}", response_class=FileResponse)
async def processed_pdf(
        namespace: str, pdf_file_name: str, background_tasks: BackgroundTasks
):
    try:
        file_path = f'{CONFIG["processed_pdfs"]}/{namespace}/{pdf_file_name}'
        os.stat(file_path)
        background_tasks.add_task(os.remove, path=file_path)
        return FileResponse(
            path=file_path,
            media_type="application/pdf",
            filename=pdf_file_name,
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Processed PDF not found")
