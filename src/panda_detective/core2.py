from dataclasses import dataclass
import re
import math
import functools
from typing import Optional, Callable
import pandas as pd

import numpy as np


def series_wrapper(func):
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

    def to_dict(self, value: float | int | pd.Series):
        is_series = isinstance(value, pd.Series)
        return {
            "active": self.active(value).any() if is_series else self.active(value),
            "value": value.mean() if is_series else value,
            "message": self.message(value),
        } | {k: self.__getattribute__(k) for k in self.__annotations__}


@dataclass
class Mapping:
    # assign an expectation to a column
    column: str
    signal: Signal


@dataclass
class RangeSignal(Signal):
    range: list[Optional[float], Optional[float]]

    @property
    def min(self):
        return self.range[0] or math.inf * -1

    @property
    def max(self):
        return self.range[1] or math.inf

    @series_wrapper
    def active(self, series: pd.Series):
        return ~series.between(self.min, self.max)

    def _from_scalar(self, scalar: float | int):
        if not self.active(scalar):
            return None
        return format_text(
            f"""
            Value {scalar:.0f} is outside
            allowed range [{self.min}, {self.max}].
                """
        )

    def _from_series(self, series: pd.Series):
        ratio = self.active(series).mean()
        return format_text(
            f"""
                {ratio*100:.0f}% of values are outside
                allowed range [{self.min}, {self.max}].
                """
        )

    def message(self, value: float | int | pd.Series):
        if isinstance(value, pd.Series):
            return self._from_series(value)
        return self._from_scalar(value)


class Signals:
    def __init__(self, df):
        self.df: pd.DataFrame = df
        self.selected_columns: list[str] = []  # current selection
        self.mappings: list[Mapping] = []

    def select(self, *args):
        # idea: also accept functions
        self.selected_columns = args
        return self

    def register(self, expectation, *args, **kwargs):
        for column in self.selected_columns:
            self.mappings.append(Mapping(column, expectation(*args, **kwargs)))
        return self

    def range(self, range_):
        return self.register(RangeSignal, range_)

    def evaluate_columns(self, df: pd.DataFrame):
        # evaluate all columns
        for mapping in self.mappings:
            print(mapping.signal.to_dict(df[mapping.column]))
        # wip

    def evaluate_row(self, series: pd.Series):
        # evaluate row
        for mapping in self.mappings:
            print(mapping.signal.to_dict(series[mapping.column]))
        # wip
