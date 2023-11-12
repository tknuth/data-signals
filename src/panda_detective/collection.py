from dataclasses import dataclass

import pandas as pd
import numpy as np

from .signals.range import RangeSignal
from .signals.notna import NotNASignal
from .signals.base import Signal


@dataclass
class Mapping:
    column: str
    signal: Signal


def add_config_column(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(config=lambda df: df.check.apply(lambda d: d.signal.config))


def add_value_column(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(value=lambda df: df.check.apply(lambda d: d.value))


def add_ratio_column(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(ratio=lambda df: df.check.apply(lambda d: d.ratio))


def replace_none_with_nan(df: pd.DataFrame) -> pd.DataFrame:
    return df.replace({None: np.nan})


class SignalCollection:
    def __init__(self, df):
        self.df: pd.DataFrame = df
        # TODO: only apply to current chain
        self.selected_columns: list[str] = []  # current selection
        self.mappings: list[Mapping] = []

    def select(self, *args):
        # TODO: also accept functions
        self.selected_columns = args
        return self

    def register(self, signal, *args, **kwargs):
        for column in self.selected_columns:
            self.mappings.append(Mapping(column, signal(*args, **kwargs)))
        return self

    def range(self, range_):
        return self.register(RangeSignal, range_)

    def notna(self):
        return self.register(NotNASignal)

    def evaluate(self, df: pd.DataFrame, aggregate=False):
        if aggregate:
            return self._evaluate_columns(df)
        return self._evaluate_cells(df)

    def _evaluate_columns(self, df: pd.DataFrame):
        # TODO: check overlapping signals (same type, same column)
        index_tuples = []
        data = []

        for mapping in self.mappings:
            index_tuples.append((mapping.column, mapping.signal.name))
            data.append(mapping.signal.check_column(df[mapping.column]))

        multi_index = pd.MultiIndex.from_tuples(
            index_tuples, names=["column", "signal"]
        )

        return (
            pd.DataFrame(
                {"check": data},
                index=multi_index,
            )
            .pipe(add_config_column)
            .pipe(add_ratio_column)
            .pipe(replace_none_with_nan)
        )

    def _evaluate_cells(self, df: pd.DataFrame):
        # TODO: check overlapping signals (same type, same column)
        index_tuples = []
        data = []

        for i, series in df.iterrows():
            for mapping in self.mappings:
                check = mapping.signal.check_scalar(series[mapping.column])
                if check is not None:
                    index_tuples.append((i, mapping.column, mapping.signal.name))
                    data.append(check)

        multi_index = pd.MultiIndex.from_tuples(
            index_tuples, names=["row", "column", "signal"]
        )

        return (
            pd.DataFrame(
                {"check": data},
                index=multi_index,
            )
            .pipe(add_config_column)
            .pipe(add_value_column)
            .pipe(replace_none_with_nan)
        )
