from __future__ import annotations
from typing import Union

from collections import namedtuple

from .exceptions import ParsingError

from .tokenize import Token



KeyValuePair = namedtuple('KeyValuePair', ['key', 'value'])


class Basket():
    def __init__(self, name: str=None, args: list=None, kwargs: dict=None):
        self.name = name
        self.args = args or []
        self.kwargs = kwargs or {}

    def __str__(self):
        name = safe_repr(self.name or '')
        args = safe_repr(self.args)[1:-1]
        kwargs = safe_repr(self.kwargs)[1:-1]
        
        return f'{name}({f"{args}, {kwargs}".strip(", ")})'

    def __getitem__(self, key: Union[int, str]):
        if type(key) is int:
            return self.args[key]
        if type(key) is str:
            return self.kwargs[key]

        raise KeyError('Key must be either integer or string')

    @property
    def is_function(self):
        return self.name is not None

    @classmethod
    def create(cls, elements: list[Union[Token, KeyValuePair, Basket]]) -> Basket:
        """Extract unnamed and named arguments from list
        and construct either a basket, list, or dictionary.
        """

        # Linking key-value pairs
        i = 0
        while i < len(elements) - 2:
            # Left, Middle, Right
            l, m, r = elements[i : i + 3]

            if type(m) is not Token or m.type != '=':
                i += 1
                continue


            if type(l) is Token and l.type == '=' \
            or type(r) is Token and r.type == '=':
                raise ParsingError('Unresolved key-value pair')


            if type(l) is not Token or l.type != '$':
                raise ParsingError('Key must be a primitive value')

            if type(r) is Token and r.type == ',':
                raise ParsingError('Comma before resolving key-value pair')
            

            # Replace element with key-value pair
            # and remove the relevant elements
            value = r.value if type(r) is Token else r
            elements[i] = KeyValuePair(l.value, value)
            del elements[i+1 : i+3]

            i += 1

        # Commas must be alternating evenly

        types = [t.type if type(t) is Token else '$'
                    for t in elements]

        if not all(t == ',' for t in types[1::2]):
            raise ParsingError('Commas incorrectly placed')

        if any(t == ',' for t in types[0::2]):
            raise ParsingError('Too many commas')

        # Remove all commas
        del elements[1::2]


        # Finally, go through all elements
        # and add arguments to a list and a dictionary

        args, kwargs = [], {}

        for element in elements:
            if type(element) is KeyValuePair:
                kwargs[element.key] = element.value
                continue
            
            if kwargs:
                raise ParsingError('Named argument before unnamed argument')

            if type(element) is Token:
                args.append(element.value)
            else:
                args.append(element)

        return cls(args=args, kwargs=kwargs)

    def simplify(self) -> Union[list, dict, Basket]:
        """Return the simplest object needed to represent the data"""

        # Functions cannot be simplified,
        # as they require the name to remain
        if self.is_function:
            return self

        # List
        if not self.kwargs:
            return self.args

        # Dictionary
        if not self.args:
            return self.kwargs

        # Default to the same basket
        return self


def safe_repr(obj: Union[int, str, list, dict, Basket]):
    """Represent an object in a form that is safe to put in a FLON document"""

    if type(obj) is list:
        return f'({", ".join(safe_repr(x) for x in obj)})'

    if type(obj) is dict:
        return f'({", ".join(f"{safe_repr(k)}={safe_repr(v)}" for k, v in obj.items())})'

    return str(obj)