__version__ = '0.1.0'

from .parse import parse
from .basket import Basket



def loads(code: str) -> Basket:
    """Load FLON from string"""
    return parse(code)