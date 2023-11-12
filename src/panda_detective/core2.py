from dataclasses import dataclass
import re
import math
import functools
from typing import Optional, Callable
import pandas as pd

import numpy as np


def series_wrapper(func):
    """If passed a scalar, wrap it in a series."""

    @functools.wraps(func)
    def wrapper(self, value):
        if isinstance(value, pd.Series):
            return func(self, value)
        return func(self, pd.Series([value])).iloc[0]

    return wrapper


def format_text(text):
    return re.sub(" +", " ", text.replace("\n", "")).strip()


@dataclass
class Signal:
    def __str__(self):
        return f"<{self.name}>"

    @property
    def name(self):
        return self.__class__.__name__


@dataclass
class Mapping:
    column: str
    signal: Signal


class ValueCheck:
    def __init__(self, description, signal):
        self.description = format_text(description)
        self.signal = signal

    def __repr__(self):
        return f"<{self.__class__.__name__}>"


class ColumnCheck:
    def __init__(self, description, ratio, signal):
        self.description = format_text(description)
        self.signal = signal
        self.ratio = ratio

    def __repr__(self):
        return f"<{self.__class__.__name__}>"


@dataclass
class RangeSignal(Signal):
    range: list[Optional[float], Optional[float]]

    @property
    def min(self) -> float | int:
        return self.range[0] or math.inf * -1

    @property
    def max(self) -> float | int:
        return self.range[1] or math.inf

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


class SignalCollection:
    def __init__(self, df):
        self.df: pd.DataFrame = df
        # idea: only apply to current chain
        self.selected_columns: list[str] = []  # current selection
        self.mappings: list[Mapping] = []

    def select(self, *args):
        # idea: also accept functions
        self.selected_columns = args
        return self

    def register(self, signal, *args, **kwargs):
        for column in self.selected_columns:
            self.mappings.append(Mapping(column, signal(*args, **kwargs)))
        return self

    def range(self, range_):
        return self.register(RangeSignal, range_)

    def evaluate(self, df: pd.DataFrame, axis=0):
        if axis == 0:
            return self._evaluate_columns(df)
        if axis == 1:
            return self._evaluate_rows(df)
        raise ValueError(f"Invalid axis {axis}.")

    def _evaluate_columns(self, df: pd.DataFrame):
        # idea: check overlapping signals (same type, same column)
        index_tuples = []
        data = []

        for mapping in self.mappings:
            index_tuples.append((mapping.column, mapping.signal.name))
            data.append(mapping.signal.check_column(df[mapping.column]))

        multi_index = pd.MultiIndex.from_tuples(
            index_tuples, names=["column", "signal"]
        )

        df = pd.DataFrame(
            {"result": data},
            index=multi_index,
        ).assign(ratio=lambda df: df.result.apply(lambda d: d.ratio))

        return df

    def _evaluate_rows(self, df: pd.DataFrame):
        # idea: check overlapping signals (same type, same column)
        index_tuples = []
        data = []

        for i, series in df.iterrows():
            for mapping in self.mappings:
                result = mapping.signal.check_value(series[mapping.column])
                if result is not None:
                    index_tuples.append((i, mapping.column, mapping.signal.name))
                    data.append(result)

        multi_index = pd.MultiIndex.from_tuples(
            index_tuples, names=["row", "column", "signal"]
        )

        return pd.Series(
            data,
            index=multi_index,
        )
