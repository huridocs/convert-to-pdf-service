import os
import logging
import graypy

from pathlib import Path
from typing import Dict


OPTIONS = ["redis_host", "redis_port", "service_host", "service_port"]
SERVICE_NAME = "convert-to-pdf"


APP_PATH = Path(__file__).parent.absolute()
DATA_PATH = f"{APP_PATH}/../data"
DOCUMENT_SOURCES_PATH = f"{DATA_PATH}/source_documents"
PDF_PROCESSED_PATH = f"{DATA_PATH}/processed_pdfs"
DOCUMENT_FAILED = f"{DATA_PATH}/failed_documents"


class ServiceConfig:
    def __init__(self):
        self.tasks_queue_name = SERVICE_NAME + "_tasks"
        self.results_queue_name = SERVICE_NAME + "_results"
        self.paths: Dict[str, str] = dict(
            {
                "app": APP_PATH,
                "data": DATA_PATH,
                "source_documents": DOCUMENT_SOURCES_PATH,
                "processed_pdfs": PDF_PROCESSED_PATH,
                "failed_documents": DOCUMENT_FAILED,
            }
        )

        self.config_from_yml: Dict[str, any] = dict()

        self.redis_host = os.environ.get('REDIS_HOST')
        self.redis_port = os.environ.get('REDIS_PORT')

        self.service_host = os.environ.get('SERVICE_HOST')
        self.service_port = os.environ.get('SERVICE_PORT')
        self.service_url = f"{self.service_host}:{self.service_port}"

    def get_logger(self, logger_name):
        logger = logging.getLogger("graylog")
        logger.setLevel(logging.INFO)

        if (
            "graylog_ip" not in self.config_from_yml
            or not self.config_from_yml["graylog_ip"]
        ):
            logger.addHandler(
                logging.FileHandler(f'{self.paths["data"]}/{logger_name}.log')
            )
            return logger

        handler = graypy.GELFUDPHandler(
            self.config_from_yml["graylog_ip"], 12201, localname="convert_to_pdf_service"
        )
        logger.addHandler(handler)
        return logger

    def write_configuration(self, config_dict: Dict[str, str]):
        config_to_write = dict()
        for config_key, config_value in config_dict.items():
            if not config_value and config_key not in self.config_from_yml:
                continue

            if not config_value and config_key in self.config_from_yml:
                config_to_write[config_key] = self.config_from_yml[config_key]
                continue

            config_to_write[config_key] = config_value

        if "graylog_ip" in self.config_from_yml:
            config_to_write["graylog_ip"] = self.config_from_yml["graylog_ip"]

        if len(config_to_write) == 0:
            return

        with open("config.yml", "w") as config_file:
            config_file.write(
                "\n".join([f"{k}: {v}" for k, v in config_to_write.items()])
            )

    def create_configuration(self):
        config_dict = dict()

        config_dict["redis_host"] = self.redis_host
        config_dict["redis_port"] = self.redis_port
        config_dict["service_host"] = self.service_host
        config_dict["service_port"] = self.service_port

        print(":::::::::: Actual configuration :::::::::::\n")
        for config_key in config_dict:
            print(f"{config_key}: {config_dict[config_key]}")

        user_input = None

        while user_input not in ("yes", "n", "y", "no", "N", "Y", ""):
            user_input = input("\nDo you want to change the configuration? [Y/n]\n")

        if user_input != "" and user_input[0].lower() == "n":
            return

        print("[Enter to KEEP current configuration]")
        for option in OPTIONS:
            configuration_input = input(f"{option}: [{config_dict[option]}] ")
            config_dict[option] = configuration_input

        self.write_configuration(config_dict)


if __name__ == "__main__":
    config = ServiceConfig()
    config.create_configuration()
