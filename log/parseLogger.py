import logging
import os

LOG_FILE = f"{os.path.dirname(__file__)}/log.txt"

parseLogger = logging.getLogger(__name__)
parseLogger.setLevel(logging.INFO)

handler = logging.FileHandler(LOG_FILE, mode='w')

format = logging.Formatter('From parser: %(message)s')
handler.setFormatter(format)

parseLogger.addHandler(handler)
