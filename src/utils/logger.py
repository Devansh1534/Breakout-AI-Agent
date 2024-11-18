# src/utils/logger.py

import logging

def setup_logger(name, log_file, level=logging.INFO):
    """
    Sets up a logger for debugging and error tracking.
    
    Args:
        name (str): Logger name.
        log_file (str): Log file path.
        level: Logging level.

    Returns:
        Logger: Configured logger instance.
    """
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
