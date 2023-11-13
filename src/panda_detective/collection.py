from dataclasses import dataclass

import pandas as pd
import numpy as np

from .signals.range import RangeSignal
from .signals.notna import NotNASignal
from .signals.base import Signal


def summarize(df: pd.DataFrame):
    return (
        df.groupby(["columns", "config", "type"])
        .agg({"column": "first", "signal": "first", "active": "mean"})
        .reset_index()
        .rename(columns={"active": "ratio"})
    )


class SignalCollection:
    def __init__(self, df):
        self.df: pd.DataFrame = df
        # TODO: only apply to current chain
        self.selection: list[str] = []
        self.signals: list[Signal] = []

    def select(self, *args):
        # TODO: also accept functions
        self.selection = args
        return self

    def range(self, range_):
        return self._register(RangeSignal, range_)

    def notna(self):
        return self._register(NotNASignal)

    def evaluate(self, df: pd.DataFrame):
        # TODO: check overlapping signals (same type, same column)
        results = []

        for signal in self.signals:
            results.append(
                pd.DataFrame(
                    {
                        "signal": signal,
                        "columns": [frozenset(signal.columns)] * len(df),
                        "column": signal.column if pd.notna(signal.column) else np.nan,
                        "type": signal.type,
                        "config": signal.config(),
                        "value": signal.value(df).values,
                        "active": signal.active(df).values,
                    }
                )
            )

        return pd.concat(results)

    def _register(self, signal, *args, **kwargs):
        for column in self.selection:
            self.signals.append(signal([column], *args, **kwargs))
        return self
