import math
from typing import Optional
import pandas as pd
import json
from toolz import curry

import numpy as np


def skipna(func):
    def wrapper(self, value):
        if pd.isna(value):
            return True
        return func(self, value)

    return wrapper

# idea: trigger interesting signals/alerts, i.e. not only "failed expectations"
class Expectation:
    def __str__(self):
        return f"<{self.name}>"

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def type(self):
        return self.__class__.__name__.lower().replace("expectation", "")

    def to_string(self, value):
        raise f"Value {value} did not pass expectation."

    def to_json(self, value):
        return json.dumps(self.to_dict(value))

    def to_dict(self, value):
        raise NotImplementedError()

    def to_format(self, format, value):
        return {
            "bool": self.to_bool,
            "string": self.to_string,
            "json": self.to_json,
            "dict": self.to_dict,
        }[format](value)


class ValuesExpectation(Expectation):
    def __init__(self, column: str, allowed_values: list):
        self.column = column
        self.allowed_values = allowed_values

    @skipna
    def to_bool(self, value):
        return value in self.allowed_values

    def to_string(self, value):
        if not self.to_bool(value):
            return f"Value {value} is not in {self.allowed_values}."

    def to_dict(self, value):
        return {
            "success": self.to_bool(value),
            "value": float(value),
            "allowed_values": self.allowed_values,
            "message": self.to_string(value),
        }


class RangeExpectation(Expectation): # ColumnExpectation
    def __init__(self, column: str, range: list[Optional[float], Optional[float]]):
        self.column = column
        self.range = range
        self.min = self.range[0] or math.inf * -1
        self.max = self.range[1] or math.inf

    @skipna
    def to_bool(self, value):
        return (value >= self.min) & (value <= self.max)

    def to_string(self, value):
        if not self.to_bool(value):
            a = "{:.0f}".format(value)
            b = "{:.0f}".format(self.min)
            c = "{:.0f}".format(self.max)
            return f"Value {a} is outside allowed range [{b}, {c}]."

    def to_dict(self, value):
        return {
            "success": bool(self.to_bool(value)),
            "value": float(value),
            "min": float(self.min),
            "max": float(self.max),
            "message": self.to_string(value),
        }


class Expectations:
    def __init__(self, df):
        self.df: pd.DataFrame = df
        self.selected_columns: list[str] = []  # current selection
        self.expectations: list[tuple[str, Expectation]] = []

    def select(self, column):
        # idea: also accept multiple cols or functions
        if isinstance(column, str):
            self.selected_columns = [column]
        return self

    def range(self, range):
        for column in self.selected_columns:
            self.expectations.append(RangeExpectation(column, range))
        return self

    def values(self, allowed_values):
        for column in self.selected_columns:
            self.expectations.append(ValuesExpectation(column, allowed_values))
        return self

    # def dispersion(self, z):
    #     ZExpectation(column, values, z) # values list is used for fitting the expectation model


    # def custom(self, custom_expectation):
    #     custom_expectation() # column is None here because it applies to the whole row
        
        

    def _create_empty_series(self):
        index_tuples = []

        for i in self.df.index:
            for expectation in self.expectations:
                idx = i, expectation.type, expectation.column
                index_tuples.append(idx)

        s = pd.Series(
            index=pd.MultiIndex.from_tuples(
                index_tuples, names=["row", "type", "column"]
            ),
        )

        return s

    def evaluate(self, format="bool"):
        s = self._create_empty_series()
        results = []

        for i in self.df.index:
            for expectation in self.expectations:
                idx = i, expectation.type, expectation.column
                value = self.df[expectation.column].loc[i]
                results.append([idx, expectation.to_format(format, value)]) # for dealing with RowExpectations, test class inheritance

        results = list(zip(*results))
        s = pd.Series(results[1], index=pd.MultiIndex.from_tuples(results[0]))
        return s  # .unstack()
