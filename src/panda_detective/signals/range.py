import math
from typing import Optional

import numpy as np
import pandas as pd

from ..checks import ColumnCheck, ScalarCheck
from .base import Signal, series_wrapper


class RangeSignal(Signal):
    def __init__(self, range: list[Optional[float], Optional[float]]):
        self.range = range
        self.min = range[0] or math.inf * -1
        self.max = range[1] or math.inf
        self.config = f"[{self.min}, {self.max}]"

    @series_wrapper
    def active(self, series: pd.Series) -> pd.Series:
        return ~series.between(self.min, self.max)

    def check_scalar(self, value: float | int) -> ScalarCheck | None:
        # value is a scalar
        if not self.active(value) or np.isnan(value):
            return None
        description = (
            f"""Value {value:.0f} is outside """
            f"""allowed range [{self.min}, {self.max}]."""
        )
        return ScalarCheck(description, value, self)

    def check_column(self, series: pd.Series) -> ColumnCheck:
        ratio = self.active(series).mean()
        description = (
            f"""{ratio*100:.0f}% of values are outside """
            f"""allowed range [{self.min}, {self.max}]."""
        )
        return ColumnCheck(description, ratio, self)
