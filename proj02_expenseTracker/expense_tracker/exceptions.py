class ExceptionTrackerError(Exception):
    """Base exception for expected application errors."""
    pass

class ValidationError(ExceptionTrackerError):
    """Raised when input violates application validation rules."""
    pass

class PersistenceError(ExceptionTrackerError):
    """Raised when a technical/database exception is raised."""
    pass