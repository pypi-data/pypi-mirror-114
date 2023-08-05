import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler


def setup_logging(log_dir):
    log_file_format = "[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s in %(pathname)s:%(lineno)d"
    log_console_format = "[%(levelname)s]: %(message)s"

    # Main logger
    main_logger = logging.getLogger()
    main_logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(Formatter(log_console_format))

    exp_file_handler = RotatingFileHandler(
        "{}training_log.log".format(log_dir), maxBytes=10 ** 6, backupCount=5
    )
    exp_file_handler.setLevel(logging.DEBUG)
    exp_file_handler.setFormatter(Formatter(log_file_format))

    main_logger.addHandler(console_handler)
    main_logger.addHandler(exp_file_handler)

    return main_logger


def remove_logging(log_dir):
    # Main logger
    main_logger = logging.getLogger()
    main_logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()

    exp_file_handler = RotatingFileHandler(
        "{}training_log.log".format(log_dir), maxBytes=10 ** 6, backupCount=5
    )

    main_logger.removeHandler(console_handler)
    main_logger.removeHandler(exp_file_handler)
