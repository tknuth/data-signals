from panda_detective.core2 import *
import numpy as np
import pandas as pd


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

    s = RangeSignal([18, 40])
    # print()
    # print(s)
    # print(s.to_bool(df.age.iloc[0]))
    # print(s.to_bool(df.age))
    # print(s.message(df.age.iloc[3]))
    # print(s.message(df.age))
    # print(s.message(df.age))
    # print(s.to_dict(df.age))
    # print(s.name)
    # print(s)

    print()
    Signals(df).select("age").range([18, 40]).evaluate_columns(df)
    Signals(df).select("age").range([18, 40]).evaluate_row(df.iloc[3])


# def test_expectations():
#     df = pd.DataFrame(
#         {
#             "name": ["Alice", "Bob", "Charlie", "David", "Mike"],
#             "gender": ["F", "M", np.nan, "M", "X"],
#             "age": [25, 32, 18, 47, 40],
#             "height": [175, 190, np.nan, 180, 190],
#         },
#         index=list("abcde"),
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
#     # print(df)
#     print(rs)
