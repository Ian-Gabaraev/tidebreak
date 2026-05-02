"""
Custom exceptions for Tidebreak.
"""


class TidebreakException(Exception):
    """Base exception for Tidebreak."""
    pass


class InvalidCountryError(TidebreakException):
    """Raised when an invalid country code is provided."""
    pass


class FetchError(TidebreakException):
    """Raised when there's an error fetching from a news source."""
    pass


class ParseError(TidebreakException):
    """Raised when there's an error parsing a news source."""
    pass

