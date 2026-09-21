"""Application-specific exceptions."""


class CallMeMaybeError(Exception):
    """Base exception for expected application failures."""


class InputFileError(CallMeMaybeError):
    """Raised when an input file cannot be read or validated."""
