# duplicate_error.py

class DuplicateError(Exception):
    """Exception thrown when duplicate of an entity exists in db."""

    def __init__(self, value):
        self.value = value
        self.number = ''

    def __str__(self):
        return repr(self.value)
