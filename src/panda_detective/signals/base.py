from typing import Optional

import pandas as pd


class Signal:
    def __init__(self, columns: list[str], config=None):
        self.columns = columns

    @property
    def column(self):
        if len(self.columns) == 1:
            return self.columns[0]

    @property
    def type(self):
        if self.__class__.__name__ == "Signal":
            return None
        return self.__class__.__name__.replace("Signal", "").lower()

    @property
    def config(self):
        return None

    def value(self, df: pd.DataFrame) -> pd.Series:
        if self.column is None:
            return pd.Series([None] * len(df))
        return df[self.column]

    def __eq__(self, other: str):
        # allows filtering df by signal easily
        return self.type == other

    def __str__(self):
        return f"<{self.__class__.__name__}>"
