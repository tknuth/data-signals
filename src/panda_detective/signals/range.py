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

    def config(self):
        return f"[{self.min}, {self.max}]"

    def active(self, df: pd.DataFrame) -> pd.Series:
        return ~df[self.column].between(self.min, self.max)
