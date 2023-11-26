import math
from typing import Optional

import numpy as np
import pandas as pd

from panda_detective.core import ignore_na

from .base import Signal


class RangeSignal(Signal):
    """Test whether values are within a range. Ignores non-numeric values."""

    def __init__(
        self, columns: list[str], range: list[Optional[float], Optional[float]]
    ):
        self.columns = columns
        self.range = range
        self.min = range[0] or math.inf * -1
        self.max = range[1] or math.inf

    @property
    def config(self) -> str:
        return f"[{self.min}, {self.max}]"

    # due to ignore_na, NaN values are always False,
    # even though explicitly created in the function
    @ignore_na
    def active(self, df: pd.DataFrame) -> pd.Series:
        # create nan series with same index and name
        series = pd.Series(
            [np.nan] * len(df), index=df.index, name=self.column, dtype="boolean"
        )
        # mask numeric values
        mask = df[self.column].apply(lambda x: isinstance(x, (int, float)))
        series.loc[mask] = ~df.loc[mask, self.column].between(self.min, self.max)
        return series

    def describe(self, series: pd.Series) -> pd.Series | None:
        if series.active:
            return f"Value {series.value:.0f} is outside {self.config}."

    def summarize(self, df: pd.DataFrame) -> str:
        ratio = df.active.mean()
        return f"""{ratio*100:.0f}% of values are outside {self.config}."""
