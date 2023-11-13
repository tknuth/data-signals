import numpy as np
import pandas as pd

from .base import Signal


class NotNASignal(Signal):
    def active(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column].isna()

    def describe(self, active: pd.Series, df: pd.DataFrame) -> str:
        assert len(active) == 1
        if not active.iloc[0]:
            return np.nan
        return "Value is NaN."

    def summarize(self, active: pd.Series, df: pd.DataFrame) -> str:
        ratio = active.mean()
        return f"""{ratio*100:.0f}% of values are NaN """
