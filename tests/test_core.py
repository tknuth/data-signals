from panda_detective.collection import *
import numpy as np
import pandas as pd
from toolz import curried as tz


def test_signals():
    df = pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie", "David", "Mike"],
            "gender": ["F", "M", np.nan, "M", "X"],
            "age": [25, 32, 18, 47, 40],
            "height": [175, 190, np.nan, 180, 190],
        },
        index=list("abcde"),
    )

    sc = (
        SignalCollection(df)
        .select("age")
        .range([20, 50])
        .notna()
        .select("height")
        .range([180, 190])
        .notna()
    )

    print()
    print(sc.evaluate(df, axis=0))
    print(sc.evaluate(df, axis=1))
