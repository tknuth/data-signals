import math
from typing import Optional

import numpy as np
import pandas as pd

from ..checks import ColumnCheck, ScalarCheck
from .base import Signal, series_wrapper


class NotNASignal(Signal):
    @series_wrapper
    def active(self, series: pd.Series) -> pd.Series:
        return series.isna()

    def check_scalar(self, value: float | int) -> ScalarCheck | None:
        # value is a scalar
        if not self.active(value):
            return None
        description = f"""Value is NaN."""
        return ScalarCheck(description, value, self)

    def check_column(self, series: pd.Series) -> ColumnCheck:
        ratio = self.active(series).mean()
        description = f"""{ratio*100:.0f}% of values are NaN """
        return ColumnCheck(description, ratio, self)
