from panda_detective import signals
from panda_detective.collection import SignalCollection
from panda_detective.testing import load_people
from pandas.testing import assert_series_equal, assert_frame_equal
import numpy as np
import pandas as pd
import pytest


def test_base():
    df = load_people()

    signal = signals.Signal(["age"])
    assert signal.column == "age"
    assert_series_equal(signal.value(df), df.age)

    signal = signals.Signal(["age", "gender"])
    assert signal.config is None
    assert signal.type is None
    assert signal.value(df).isna().all()

    with pytest.raises(Exception):
        signal.column


def test_notna():
    df = load_people()
    signal = signals.NotNASignal(["age"])
    assert_series_equal(
        signal.active(df),
        pd.Series(
            {
                "a": False,
                "b": False,
                "c": False,
                "d": False,
                "e": True,
            },
            name="age",
        ),
    )
    result = SignalCollection(df, signals=[signal]).evaluate(df)
    assert_series_equal(
        result.show().description,
        pd.Series(
            {
                "e": "Value is NaN.",
            },
            name="description",
        ),
    )
    assert_frame_equal(
        result.summarize(),
        pd.DataFrame(
            {
                "column": ["age"],
                "type": ["notna"],
                "config": [None],
                "ratio": [0.2],
                "description": ["20% of values are NaN"],
            }
        ),
    )
