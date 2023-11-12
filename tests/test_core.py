from panda_detective.core2 import *
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
        .select("height")
        .range([180, 190])
    )

    tz.pipe(
        sc.evaluate(df, axis=0),
    )
    #     )
    #     rs = (
    #         Expectations(df)
    #         .select("age")
    #         .range((18, 40))
    #         .select("height")
    #         .range((180, 190))
    #         .select("gender")
    #         .values(["M", "F"])
    #         .evaluate()
    #         # .evaluate(format="string")
    #     )

    #     # should also be possible to do this:
    #     # expectations.select(...).range(...)
    #     # expectations.select(...).range(...)

    #     print()
    #     print(rs)
