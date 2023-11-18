import math
from typing import Optional
import functools
import numpy as np
import pandas as pd

from .base import Signal


def ignore_na(func):
    @functools.wraps(func)
    def wrapper(self, df):
        active = func(self, df)
        return active.mask(df[self.column].isna(), False)

    return wrapper


class RangeSignal(Signal):
    def __init__(
        self, columns: list[str], range: list[Optional[float], Optional[float]]
    ):
        self.columns = columns
        self.range = range
        self.min = range[0] or math.inf * -1
        self.max = range[1] or math.inf

    @property
    def config(self):
        return f"[{self.min}, {self.max}]"

    @ignore_na
    def active(self, df: pd.DataFrame) -> pd.Series:
        return ~df[self.column].between(self.min, self.max)

    def describe(self, series: pd.Series) -> pd.Series:
        if series.active:
            return f"Value {series.value:.0f} is outside {self.config}."

    def summarize(self, df: pd.DataFrame) -> str:
        ratio = df.active.mean()
        return f"""{ratio*100:.0f}% of values are outside {self.config}"""
