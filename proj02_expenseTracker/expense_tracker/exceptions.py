class ExceptionTrackerError(Exception):
    """Base exception for expected application errors."""

class ValidationError(ExceptionTrackerError):
    """Raised when input violates application validation rules."""