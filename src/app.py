import os
import sys

from fastapi import FastAPI, HTTPException, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_202_ACCEPTED

from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
import sentry_sdk

from ServiceConfig import ServiceConfig
from DocumentFile import DocumentFile

config = ServiceConfig()
logger = config.get_logger("convert_to_pdf_api")

app = FastAPI()

logger.info("Convert to PDF service has started")

try:
    sentry_sdk.init(
        os.environ.get("SENTRY_OCR_DSN"),
        traces_sample_rate=0.1,
        environment=os.environ.get("ENVIRONMENT", "development"),
    )
    app.add_middleware(SentryAsgiMiddleware)
except Exception:
    pass


@app.get("/info")
async def info():
    logger.info("Convert to PDF info endpoint")

    content = jsonable_encoder(
        {
            "service:": "Convert to PDF API",
            "sys": sys.version
        }
    )
    return JSONResponse(content=content)


@app.get("/error")
async def error():
    message = "This is a test error from the error endpoint"
    logger.error(message)
    raise HTTPException(
        status_code=500, detail=message
    )


# @app.post("/")
# async def convert_to_pdf_sync(
#     file: UploadFile = File(...)
# ):
#     filename = "No file name"
#     try:
#         namespace = "sync_convert"
#         filename = file.filename
#         document_file = DocumentFile(namespace)
#         document_file.save(document_file_name=filename, file=file.file.read())
#         processed_pdf_filepath = convert_to_pdf(filename, namespace)
#         return FileResponse(path=processed_pdf_filepath, media_type="application/pdf")
#     except Exception:
#         message = f"Error processing {filename}"
#         logger.error(message, exc_info=1)
#         raise HTTPException(status_code=422, detail=message)


@app.post("/upload/{namespace}", status_code=HTTP_202_ACCEPTED)
async def upload_document(namespace, file: UploadFile = File(...)):
    filename = "No file name"
    try:
        filename = file.filename
        document_file = DocumentFile(namespace)
        document_file.save(document_file_name=filename, file=file.file.read())
        return "File uploaded"
    except Exception:
        message = f"Error uploading document {filename}"
        logger.error(message, exc_info=1)
        raise HTTPException(status_code=422, detail=message)


@app.get("/processed_pdf/{namespace}/{pdf_file_name}", response_class=FileResponse)
async def processed_pdf(namespace: str, pdf_file_name: str, background_tasks: BackgroundTasks):
    # try:
        file_path = f'{config.paths["processed_pdfs"]}/{namespace}/{pdf_file_name}'
        os.stat(file_path)
        background_tasks.add_task(os.remove, path=file_path)
        return FileResponse(
            path=file_path,
            media_type="application/pdf",
            filename=pdf_file_name,
        )

    # except FileNotFoundError:
    #     raise HTTPException(status_code=404, detail="Processed PDF not found")
    # except Exception:
    #     logger.error("Error", exc_info=1)
    #     raise HTTPException(status_code=422)
