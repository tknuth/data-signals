from dataclasses import dataclass

import pandas as pd
import numpy as np

from .signals.range import RangeSignal
from .signals.notna import NotNASignal
from .signals.base import Signal
from typing import Optional


def summarize(df: pd.DataFrame):
    return (
        df.groupby(["columns", "config", "type"])
        .agg({"column": "first", "signal": "first", "active": "mean"})
        .reset_index()
        .rename(columns={"active": "ratio"})
    )


class Evaluation:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def show(self):
        df = self.df.query("active == True")

        df["description"] = df.apply(
            lambda series: series.signal.describe(series), axis=1
        )

        return df.drop(columns=["signal", "columns"])

    def summarize(self):
        def func(g):
            signal = g.signal.iloc[0]
            return pd.Series(
                {
                    "column": signal.column,
                    "type": signal.type,
                    "config": signal.config,
                    "ratio": g.active.mean(),
                    "description": signal.summarize(g),
                }
            )

        return self.df.groupby(["signal", "columns"]).apply(func).reset_index(drop=True)


class SignalCollection:
    def __init__(
        self, df, selection: Optional[list] = None, signals: Optional[list] = None
    ):
        self.df: pd.DataFrame = df
        self.selection = [] if selection is None else selection
        self.signals = [] if signals is None else signals

    def select(self, *args):
        # TODO: also accept functions
        return SignalCollection(self.df, selection=args, signals=self.signals)

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
                        "config": signal.config,
                        "value": signal.value(df).values,
                        "active": signal.active(df).values,
                    }
                )
            )

        return Evaluation(pd.concat(results))
        # return pd.concat(results)

    def _register(self, signal, *args, **kwargs):
        if not self.selection:
            self.selection = self.df.columns.tolist()
        for column in self.selection:
            self.signals.append(signal([column], *args, **kwargs))
        return self
