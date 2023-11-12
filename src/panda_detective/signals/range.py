import math
from typing import Optional

import numpy as np
import pandas as pd

from ..checks import ColumnCheck, ValueCheck
from .base import Signal, series_wrapper


class RangeSignal(Signal):
    def __init__(self, range: list[Optional[float], Optional[float]]):
        self.range = range
        self.min = range[0] or math.inf * -1
        self.max = range[1] or math.inf

    @series_wrapper
    def active(self, series: pd.Series) -> pd.Series:
        return ~series.between(self.min, self.max)

    def check_value(self, value: float | int) -> ValueCheck | None:
        # value is a scalar
        if not self.active(value) or np.isnan(value):
            return None
        description = (
            f"""Value {value:.0f} is outside """
            f"""allowed range [{self.min}, {self.max}]."""
        )
        return ValueCheck(description, self)

    def check_column(self, series: pd.Series) -> ColumnCheck:
        ratio = self.active(series).mean()
        description = (
            f"""{ratio*100:.0f}% of values are outside """
            f"""allowed range [{self.min}, {self.max}]."""
        )
        return ColumnCheck(description, ratio, self)
