import json
import logging.config
import os

ENV_NAME = "default"


def __init_logging():
    path = 'logging.json'
    if os.path.exists(path):
        with open(path, 'rt') as file:
            logging.config.dictConfig(json.loads(file.read()))
    else:
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s - %(module)s::%(funcName)s - [%(levelname)s] - %(message)s")
