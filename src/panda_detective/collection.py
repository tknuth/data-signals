from dataclasses import dataclass

import pandas as pd

from .signals.range import RangeSignal
from .signals.base import Signal


@dataclass
class Mapping:
    column: str
    signal: Signal


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

    def evaluate(self, df: pd.DataFrame, axis=0):
        if axis == 0:
            return self._evaluate_columns(df)
        if axis == 1:
            return self._evaluate_rows(df)
        raise ValueError(f"Invalid axis {axis}.")

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

        df = pd.DataFrame(
            {"result": data},
            index=multi_index,
        ).assign(ratio=lambda df: df.result.apply(lambda d: d.ratio))

        return df

    def _evaluate_rows(self, df: pd.DataFrame):
        # TODO: check overlapping signals (same type, same column)
        index_tuples = []
        data = []

        for i, series in df.iterrows():
            for mapping in self.mappings:
                result = mapping.signal.check_scalar(series[mapping.column])
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
