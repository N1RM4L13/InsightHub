import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class Logger:
    def __init__(self, log_file: str = "app.log", log_level: int = logging.INFO, max_bytes: int = 5 * 1024 * 1024, backup_count: int = 5):
        """
        Initializes the Logger instance with file and console logging.

        Args:
            log_file (str): The name of the log file.
            log_level (int): The logging level (e.g., logging.INFO, logging.DEBUG).
            max_bytes (int): Maximum size of the log file in bytes before rotating (default 5 MB).
            backup_count (int): Number of backup log files to keep (default 5).
        """
        # Create a logger instance
        self.logger = logging.getLogger("AppLogger")
        self.logger.setLevel(log_level)
        
        # Ensure the log directory exists
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, log_file)

        # File handler with rotation
        file_handler = RotatingFileHandler(log_path, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setLevel(log_level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # Define log formatting
        log_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(log_format)
        console_handler.setFormatter(log_format)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message: str):
        """Logs an info message."""
        self.logger.info(message)

    def debug(self, message: str):
        """Logs a debug message."""
        self.logger.debug(message)

    def warning(self, message: str):
        """Logs a warning message."""
        self.logger.warning(message)

    def error(self, message: str):
        """Logs an error message."""
        self.logger.error(message)

    def critical(self, message: str):
        """Logs a critical message."""
        self.logger.critical(message)
