# ============================================
# logger.py - Logging Module
# AI Powered Smart Study Assistant
# ============================================

import logging
import os
from datetime import datetime

def setup_logger():
    """
    Setup logger for the application
    Logs to both file and console
    Returns:
        Logger instance
    """
    # Create logs directory if not exists
    os.makedirs("logs", exist_ok=True)

    # Create logger
    logger = logging.getLogger("AIStudyAssistant")
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # File handler - saves to logs/app.log
    file_handler = logging.FileHandler(
        f"logs/app.log",
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)

    # Console handler - shows in terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create global logger instance
logger = setup_logger()