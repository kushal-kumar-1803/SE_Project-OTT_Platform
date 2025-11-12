import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Create a new log file each day
log_filename = os.path.join(LOG_DIR, f"ott_{datetime.now().strftime('%Y-%m-%d')}.log")

# Configure logging
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("ott_logger")

class LogService:
    @staticmethod
    def log_user_action(user_id, action):
        message = f"User {user_id} performed action: {action}"
        logger.info(message)
        return {"status": "success", "message": message}

    @staticmethod
    def log_error(error_msg):
        message = f"ERROR: {error_msg}"
        logger.error(message)
        return {"status": "error", "message": message}
