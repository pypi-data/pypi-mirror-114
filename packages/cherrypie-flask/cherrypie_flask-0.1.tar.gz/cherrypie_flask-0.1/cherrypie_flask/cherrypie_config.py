import logging
import os
import sys
from typing import List, Any, Callable

def setup_logger(
    debug_mode: bool = False,
):
    # Set up basic logger
    logger = logging.getLogger('Cherrypie')

    # Setup stdout logger
    soh = logging.StreamHandler(sys.stdout)
    logger.addHandler(soh)

    # Get log level from env vars
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    if debug_mode:
        if log_level:
            logger.warn("Overriding LOG_LEVEL setting with DEBUG")
        log_level = 'DEBUG'

    try:
        logger.setLevel(log_level)
    except ValueError:
        logger.setLevel(logging.INFO)
        logger.warn("Variable LOG_LEVEL not valid - Setting Log Level to INFO")
    return logger


class CherryPieConfig:
    """Cherrypie API configuration object.

    Attributes:
        CHERRYPIE_API_KEY (str) Your Cherrypie API key

        IDENTITY_FUNCTION (lambda): Identity function that constructs an
            identity object. It accepts a flask request and returns 
            a dictionary that must contain "entityKey" field.

        DEBUG_MODE (bool): Development mode. Defaults to False.

        CHERRYPIE_API_URL (str): Base URL of the Cherrypie API.

        TIMEOUT (int): Timeout (in seconds) for API calls.

        LOGGER (logging.Logger): Logger used by all classes and methods in the
            cherrypie package.
    """

    CHERRYPIE_API_KEY: str = None
    IDENTITY_FUNCTION: Callable[[Any], None] = lambda req: None
    DEBUG_MODE: bool = False
    CHERRYPIE_API_URL: str = "https://api.cherrypie.app"
    TIMEOUT: int = 3 # seconds

    def __init__(
        self,
        api_key: str,
        cherrypie_api_url = CHERRYPIE_API_URL,
        identity_function = None,
        debug_mode: bool = False,
        timeout: int = 3,
    ):
        self.CHERRYPIE_API_KEY = api_key
        self.IDENTITY_FUNCTION = identity_function
        self.DEBUG_MODE = debug_mode
        self.TIMEOUT = timeout
        self.CHERRYPIE_API_URL = cherrypie_api_url
        self.LOGGER = setup_logger(self.DEBUG_MODE)
