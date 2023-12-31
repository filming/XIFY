from xify import XIFY

import os
import logging

STORAGE_DIR_PATH = "../storage"
LOGS_DIR_PATH = f"{STORAGE_DIR_PATH}/logs"

if not os.path.exists(STORAGE_DIR_PATH): os.mkdir(STORAGE_DIR_PATH)
if not os.path.exists(LOGS_DIR_PATH): os.mkdir(LOGS_DIR_PATH)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler("../storage/logs/main.log", "w")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)

def main():
    logger.info("XIFY program has been started!")

    xify = XIFY()
    xify.create_tas()

if __name__ == "__main__":
    main()
