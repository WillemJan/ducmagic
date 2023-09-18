import logging
import sys


def setup_logger(loglevel: int = logging.DEBUG,
                 log_to_disk: str = "") -> logging.Logger:
    '''
    Setup log handler
        Parameters:
            log_to_disk (str): Write to filename, if provided.

        Returns:
            Instantiated log handler.

    >>> log = setup_logger()
    >>> log.debug('test')
    '''

    if log_to_disk:
        # Setup loghandler to write to disk.
        file_handler = logging.FileHandler(filename="tmp.log")

    # Use stdout by default for logging.
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    handlers = [stdout_handler]

    if log_to_disk:
        handlers.append(file_handler)

    # Define the log format.
    logging.basicConfig(
        level=loglevel,
        format="[%(asctime)s] {%(filename)s:" +
               "%(lineno)d} %(levelname)s - %(message)s",
        handlers=handlers,
    )

    # Instantiate the logging object.
    logger = logging.getLogger(__name__)

    return logger
