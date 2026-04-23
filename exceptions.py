"""Shared exception types and exit codes for the Bundle news scraper."""


class ExitCode:
    UNKNOWN_CRITICAL = 1
    STORAGE_ERROR    = 2
    BROWSER_ERROR    = 3


class CriticalScraperError(Exception):
    """
    Raised when an unrecoverable error occurs that must terminate the process.

    Carries an exit_code from ExitCode so the caller knows what went wrong.
    """

    def __init__(self, message: str, exit_code: int = ExitCode.UNKNOWN_CRITICAL):
        super().__init__(message)
        self.exit_code = exit_code
