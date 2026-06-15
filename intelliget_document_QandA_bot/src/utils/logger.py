import logging
import logging.handlers
import os
from datetime import datetime

# ========================= CONFIGURATION =========================
LOG_DIR = "logs"                    # Folder where logs will be saved
LOG_FILE = "chatbot_session.log"                # Main log file name
MAX_BYTES = 10 * 1024 * 1024        # 10 MB per log file
BACKUP_COUNT = 5                    # Keep last 5 rotated files

# Create logs directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)

log_path = os.path.join(LOG_DIR, LOG_FILE)

# ========================= LOGGER SETUP =========================
logger = logging.getLogger("chatbot_logger")
logger.setLevel(logging.DEBUG)      # Capture everything (DEBUG → CRITICAL)

# ------------------- File Handler (with rotation) -------------------
file_handler = logging.handlers.RotatingFileHandler(
    log_path,
    maxBytes=MAX_BYTES,
    backupCount=BACKUP_COUNT,
    encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)

# ------------------- Console Handler -------------------
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)   # Console shows INFO and above

# ------------------- Formatter -------------------
formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers (only once)
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
