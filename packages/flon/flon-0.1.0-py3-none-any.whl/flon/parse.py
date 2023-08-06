from __future__ import annotations
from typing import Union

import re

from .tokenize import tokenize, Token
from .basket import Basket



def parse(code: str):
    """Deserialize a string containing a FLON document to a Python object."""

    # Encapsulate entire string in parentheses
    # to allow the top scope to be properly processed
    code = f'({code})'

    # Initialize a stack to deal with navigating
    # up and down parenthesized sections
    stack = [[]]


    for token in tokenize(code):
        # Open up a new section
        # when a left-handed parenthesis is found
        if token.type == '(':
            stack[-1].append([])
            stack.append(stack[-1][-1])

        # Close down the last opened section
        # when a right-handed parenthesis is found
        elif token.type == ')':
            # Move back up the tree
            # and keep the array for further processing
            array = stack.pop()
            
            # Also remove the array from the scope it is in
            stack[-1].pop()
            
            # Extract unnamed and named arguments from sequence
            basket = Basket.create(array)

            # Name basket if there is a preceding name, otherwise simplify
            if len(stack[-1]) >= 1 and type(stack[-1][-1]) is Token and stack[-1][-1].type == '$':
                basket.name = stack[-1][-1].value
                del stack[-1][-1]
            else:
                basket = basket.simplify()

            stack[-1].append(basket)

        # If the token is not a parenthesis,
        # add it to the currently opened section
        else:
            stack[-1].append(token)

    # Remove the initial encapsulation
    result = stack[-1][0]

    # Convert result to a basket if necessary.
    # Top layer might be only a list or dictionary,
    # depending on the arguments provided,
    # because baskets get simplified upon closure.

    if type(result) is list:
        return Basket(args=result)

    if type(result) is dict:
        return Basket(kwargs=result)

    return result