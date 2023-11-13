import functools
from typing import Optional
from dataclasses import dataclass

import pandas as pd


def series_wrapper(func):
    """If passed a scalar, wrap it in a series."""

    @functools.wraps(func)
    def wrapper(self, value):
        if isinstance(value, pd.Series):
            return func(self, value)
        return func(self, pd.Series([value])).iloc[0]

    return wrapper


class Signal:
    def __init__(self, column: str, config: Optional[str] = None):
        self.column = column
        self.config = config

    def __str__(self):
        return f"<{self.name}>"

    @property
    def name(self):
        return self.__class__.__name__.replace("Signal", "").lower()
