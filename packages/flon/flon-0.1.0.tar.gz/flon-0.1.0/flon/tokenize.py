from __future__ import annotations
from typing import Union, Iterator

import re

from .exceptions import ParsingError

from collections import namedtuple



Token = namedtuple('Token', ['type', 'value'])

SPECIALS = '(),='
COMMENT_PATTERN = re.compile(r'^/\*(.+)\*/')
VALUE_PATTERN = re.compile(fr'^(?:([\"\'])((?:\\?[^\n])+?)\1|([^{SPECIALS}\s]+))')



def tokenize(code: str) -> Iterator[Token]:
    """Segment a string into its atomic parts."""

    i = 0
    while i < len(code):
        rest = code[i:]

        # Ignore leading whitespace to make parsing easier
        difference = len(rest) - len(rest.lstrip())
        if difference:
            i += difference
            continue

        # Special characters!
        if rest[0] in SPECIALS:
            yield Token(rest[0], None)
            i += 1
            continue
        
        # Comments!
        if m := COMMENT_PATTERN.match(rest):
            i += len(m.group(0))
            continue

        # Values!
        if m := VALUE_PATTERN.match(rest):
            yield Token('$', m.group(0))
            i += len(m.group(0))
            continue


        raise ParsingError(f'Error at character {i}', index=i)