from panda_detective import signals
from panda_detective.collection import SignalCollection
from panda_detective.testing import load_people, load_fruits
from pandas.testing import assert_series_equal, assert_frame_equal
import numpy as np
import pandas as pd

# TODO: Test "forbidden" mode


def test_values():
    df = load_fruits()
    signal = signals.ValuesSignal(["name"], ["Apple", "Pear", "Pineapple"])
    assert signal.config == "3 allowed values"
    assert_series_equal(
        signal.active(df),
        pd.Series(
            {
                0: False,
                1: True,
                2: False,
                3: False,
                4: True,
                5: False,
            },
            name="name",
            dtype="boolean",
        ),
    )
    result = SignalCollection(df, signals=[signal]).evaluate(df)
    assert_series_equal(
        result.show().description,
        pd.Series(
            {
                1: "Value Orange is not allowed.",
                4: "Value Kiwi is not allowed.",
            },
            name="description",
        ),
    )
    assert_frame_equal(
        result.summarize(),
        pd.DataFrame(
            {
                "column": ["name"],
                "type": ["values"],
                "config": ["3 allowed values"],
                "ratio": [1 / 3],
                "description": ["33% of values are not allowed."],
            }
        ),
    )
