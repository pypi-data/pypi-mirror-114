

class PyFLONError(Exception):
    """Generic error for PyFLON."""


class ParsingError(PyFLONError):
    """Something went wrong during parsing."""

    def __init__(self, message: str, index: int=None):
        super().__init__(message)
        self.index = index