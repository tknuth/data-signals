import math
from typing import Optional

import numpy as np
import pandas as pd

from .base import Signal


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

    def active(self, df: pd.DataFrame) -> pd.Series:
        return ~df[self.column].between(self.min, self.max)

    def describe(self, active: pd.Series, df: pd.DataFrame) -> pd.Series:
        def func(s):
            if s.active and pd.notna(s.value):
                return f"{s.value:.0f} is outside {self.config}."
            return np.nan

        return pd.DataFrame({"active": active, "value": df[self.column]}).apply(
            func, axis=1
        )

    def summarize(self, active: pd.Series, df: pd.DataFrame) -> str:
        ratio = active.mean()
        return f"""{ratio*100:.0f}% of values are outside {self.config}"""
