"""
ducmagic helper.
"""

import logging
import sys
import subprocess

E_DATABASE_NOT_FOUND = "Error opening:" # Duc's response if the db is not found.
E_PATH_NOT_IN_INDEX = "Requested path not found"  # Duc's friendly error msg if path not in db.


def _setup_logger(loglevel: int = logging.DEBUG,
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

log = _setup_logger(logging.DEBUG)

def do_cmd(cmd: str) -> str:
    '''
    Returns the output of a shell command.

            Parameters:
                    cmd (str): The command to execute.

            Returns:
                    output.decode() (str): The result from the shell command.

    On error (stderr) this command halts the running code.

    >>> _do_cmd('ls ' + __file__).find(__file__) > -1
    True
    '''
    output = ""

    with subprocess.Popen(cmd,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          shell=True) as proc:

        output, err = proc.communicate()

        if err:
            if err.decode().startswith(E_PATH_NOT_IN_INDEX):
                sys.exit(-1)
            elif err.decode().startswith(E_DATABASE_NOT_FOUND):
                output = E_DATABASE_NOT_FOUND
            else:
                log.error(err.decode())
                sys.exit(-1)
        else:
            output = output.decode()

    return output
