import logging
import os

def setup_logging(log_level=logging.INFO):
    # Create logs directory if it does not exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Set up logging
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Create file handler which logs even debug messages
    fh = logging.FileHandler('logs/job_bot.log')
    fh.setLevel(log_level)

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
