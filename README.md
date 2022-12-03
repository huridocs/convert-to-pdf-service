# Convert documents to PDF

A Docker-powered service for converting files supported by Libreoffice to PDF.

---

## Dependencies and requirements

- Redis server for managing queues
- Docker ([install](https://runnable.com/docker/getting-started/))
- Docker-compose ([install](https://docs.docker.com/compose/install/))
  - Note: On mac Docker-compose is installed with Docker

## Quick Start

Start the service:

    ./run start

This script will start the service with default configurations.

Default configuration values are as follows:

```
REDIS_HOST=localhost
REDIS_PORT=6379
SERVICE_HOST=127.0.0.1
SERVICE_PORT=5060
```

## Development and testing

A Python virtual env is needed for some of the development tasks

    ./run install_venv

Start the service for testing (with a redis server included)

    ./run start

Check service is up and get general info on supported languages and other important information:

    curl localhost:5060/info

Test converting to PDF is working

curl -X POST -F 'file=@./src/test_files/sample-english.pdf' localhost:5060 --output english.pdf


To list all available commands just run `./run`, some useful commands:

    ./run test
    ./run linter
    ./run check_format
    ./run formatter

## Contents

- [Asynchronous OCR](#asynchronous-ocr)
- [HTTP server](#http-server)
- [Retrieve OCRed PDF](#retrieve-ocred-pdf)
- [Queue processor](#queue-processor)
- [Service configuration](#service-configuration)
- [Troubleshooting](#troubleshooting)

## Asynchronous OCR

1. Upload the file to the service

   curl -X POST -F 'file=@/PATH/TO/PDF/pdf_name.pdf' localhost:5060/upload/[namespace]

![Alt logo](readme_pictures/send_materials.png?raw=true "Send PDF to extract")

The enpoint sends a message to the Redis queue to be processed asynchronously by the worker

2. Retrieve converted PDF

Upon completion of the OCR process, a message is placed in the `ocr_results` Redis queue. This response is, for now, using specific Uwazi terminology. To check if the process for a specific file has been completed:

    queue = RedisSMQ(host=[redis host], port=[redis port], qname='ocr_results', quiet=True)
    results_message = queue.receiveMessage().exceptions(False).execute()

    # The message.message contains the following information:
    # {
    #   "namespace": "namespace",
    #   "task": "pdf_name.pdf",
    #   "success": true,
    #   "error_message": "",
    #   "file_url": "http://localhost:5050/processed_pdf/[namespace]/[pdf_name]"
    #   }


    curl -X GET http://localhost:5050/processed_pdf/[namespace]/[pdf_name]

## HTTP server

The container `HTTP server` is coded using Python 3.10 and uses the [FastApi](https://fastapi.tiangolo.com/) web framework.

The endpoints code can be found inside the file `./src/api/app.py`.

## Queue processor

The container `Queue processor` is coded using Python 3.10, and it is in charge of communications with the Redis queue.

The code can be found in the file `./src/worker/queue_processor.py` and it uses the library `RedisSMQ` to interact with the Redis queues.
