"""Various functions"""

import functools
from typing import Any, Union


def drop_fields(representation:dict, fields:Union[str,list], error_handler=None):
    """Remove one or more keys from a dictionary"""
    fields = (fields,) if type(fields) == str else fields
    for field_name in fields:
        try:
            representation.pop(field_name)
        except Exception as error:
            if error_handler:
                error_handler(error)
            else:
                raise
    return representation

def getattr_nested(obj: Any, attr:str, default=None):
    """Retrieve attribute from nested objects using dot notation"""
    try:
        return functools.reduce(getattr, attr.split('.'), obj)
    except AttributeError as error:
        if default is None:
            raise error
        return default

def get_ignore_errors(errors:list):
    """Return error handler which ignores error from one or more classes and raises other errors"""
    def error_handler(error:Exception):
        if not isinstance(error, errors):
            raise error
    return error_handler
