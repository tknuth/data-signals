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
        # Works with original DataFrame
        raise NotImplementedError

    def describe(self):
        # Works with row Series
        raise NotImplementedError

    def summarize(self):
        # Works with evaluation DataFrame
        raise NotImplementedError

    def value(self, df: pd.DataFrame) -> pd.Series:
        if len(self.columns) == 1:
            return df[self.column]
        return pd.Series([None] * len(df))

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __gt__(self, other):
        return self.__key() > other.__key()

    def __key(self):
        return tuple([self.type, *self.columns])

    def __hash__(self) -> int:
        return hash(self.__key())

    # def __str__(self):
    # return f"<{self.__class__.__name__}>"
