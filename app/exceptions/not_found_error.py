# not_found_error.py

class NotFoundError(Exception):
    """Exception thrown when a queried entity is not found in db."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
