import logging.config
from logging.handlers import RotatingFileHandler

file_handler = RotatingFileHandler("logs/log_file.log", maxBytes=20000, backupCount=5)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[file_handler, logging.StreamHandler()],
)
logger = logging.getLogger("SQLite_to_Postgres_ETL")
