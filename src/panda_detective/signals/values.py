import functools
import math
from typing import Optional

import numpy as np
import pandas as pd

from panda_detective.core import ignore_na

from .base import Signal


class ValuesSignal(Signal):
    """Test whether values are part of a set of allowed values and not part of a set of forbidden values."""

    def __init__(self, columns: list[str], values: list, mode: str = "allowed"):
        if mode not in ["allowed", "forbidden"]:
            raise ValueError("Parameter mode must be either 'allowed' or 'forbidden'.")
        self.columns = columns
        self.values = values
        self.mode = mode

    @property
    def config(self) -> str:
        return f"{len(self.values)} {self.mode} values"

    @ignore_na
    def active(self, df: pd.DataFrame) -> pd.Series:
        series = ~df[self.column].isin(self.values)
        if self.mode == "forbidden":
            return ~series
        return series.astype("boolean")

    def describe(self, series: pd.Series) -> pd.Series | None:
        if series.active:
            return f"Value {series.value} is not allowed."

    def summarize(self, df: pd.DataFrame) -> str:
        ratio = df.active.mean()
        return f"""{ratio*100:.0f}% of values are not allowed."""
