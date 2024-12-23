import logging
import json
from datetime import datetime, UTC

def configure_logging():
    """
    Configure Flask application logging with JSONFormatter.
    """
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers = [handler]


class JSONFormatter(logging.Formatter):
    """
    Custom JSON log formatter for structured logs.
    """
    def format(self, record):
        log_record = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        # Add extra fields if available (e.g., request path, method)
#        if hasattr(record, "path"):
#            log_record["path"] = record.path
#        if hasattr(record, "method"):
#            log_record["method"] = record.method
#        if hasattr(record, "status_code"):
#            log_record["status_code"] = record.status_code

        return json.dumps(log_record)
