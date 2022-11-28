import logging
import os

import graypy


def get_logger(logger_name):
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
        os.environ.get(""), 12201, localname="convert_to_pdf_service"
    )
    logger.addHandler(handler)
    return logger
