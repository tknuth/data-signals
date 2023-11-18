from typing import Optional

import pandas as pd


class Signal:
    def __init__(self, columns: list[str]):
        self.columns = columns

    @property
    def column(self):
        if len(self.columns) == 1:
            return self.columns[0]
        raise Exception("Signal can only be applied to a single column.")

    @property
    def type(self):
        if self.__class__.__name__ == "Signal":
            return None
        return self.__class__.__name__.replace("Signal", "").lower()

    @property
    def config(self):
        return None

    def active(self, df: pd.DataFrame) -> pd.Series:
        raise NotImplementedError

    def describe(self):
        raise NotImplementedError

    def summarize(self):
        raise NotImplementedError

    def value(self, df: pd.DataFrame) -> pd.Series:
        if len(self.columns) == 1:
            return df[self.column]
        return pd.Series([None] * len(df))

    def __eq__(self, other: str):
        # allows filtering df by signal easily
        return self.type == other

    def __str__(self):
        return f"<{self.__class__.__name__}>"
