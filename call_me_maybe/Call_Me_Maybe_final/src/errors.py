"""Application-specific exceptions."""


class CallMeMaybeError(Exception):
    """Base exception for expected application failures."""


class InputFileError(CallMeMaybeError):
    """Raised when an input file cannot be read or validated."""


class GenerationError(CallMeMaybeError):
    """Raised when one prompt cannot produce a validated function call."""


class ModelSetupError(CallMeMaybeError):
    """Raised when the model runtime or tokenizer cannot be initialized."""
