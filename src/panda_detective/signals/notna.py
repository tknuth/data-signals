import numpy as np
import pandas as pd

from .base import Signal


class NotNASignal(Signal):
    def active(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column].isna()

    def describe(self, series: pd.Series) -> pd.Series:
        if series.active:
            return "Value is NaN."

    def summarize(self, df: pd.DataFrame) -> str:
        ratio = df.active.mean()
        return f"""{ratio*100:.0f}% of values are NaN"""
