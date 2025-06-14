# src/utils/logger.py
import structlog
from dotenv import load_dotenv
import os

load_dotenv()
logging_level = os.getenv("LOGGING_LEVEL", "INFO")

structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging_level),
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
)

log = structlog.get_logger()