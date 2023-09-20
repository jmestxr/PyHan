import logging
import os

LOG_FILE = f"{os.path.dirname(__file__)}/log.txt"

lexLogger = logging.getLogger(__name__)
lexLogger.setLevel(logging.INFO)

handler = logging.FileHandler(LOG_FILE, mode='w')

format = logging.Formatter('From lexer: %(message)s')
handler.setFormatter(format)

lexLogger.addHandler(handler)
