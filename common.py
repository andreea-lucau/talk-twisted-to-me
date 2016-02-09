"""Common"""
import logging
import os
from datetime import datetime

import config


def setup_logging(base_name, level=logging.INFO):
    now = datetime.now()
    log_filename = os.path.join(
        config.LOG_DIR,
        "%s_%s_.log" % (base_name, now.strftime("%d_%m_%y")),
    )

    logging.basicConfig(
        filename=log_filename,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%I:%M:%S %p",
        level=level
    )
