from panda_detective import aggregations as agg, selections as sel, testing as tst
from datetime import date
import numpy as np
import pandas as pd
import seaborn as sns
import random

iris = sns.load_dataset("iris")


def test_coverage():
    pd.testing.assert_series_equal(
        agg.coverage(tst.random_na(iris, seed=42)),
        pd.Series(
            {
                "sepal_length": 0.88,
                "sepal_width": 0.91,
                "petal_length": 0.91,
                "petal_width": 0.90,
                "species": 0.91,
            }
        ),
        rtol=0,
        atol=0.005,
    )


def test_coverage_last_nd_md():
    today = "2023-08-31"

    date_range = pd.date_range("2023-06-01", today, freq="1D")
    n = len(date_range)

    df1 = tst.random_na(iris.iloc[0 : n - 30], ratio=0.7, seed=42)
    df2 = tst.random_na(iris.iloc[n - 30 : n], ratio=0.9, seed=42)

    df = pd.concat([df1, df2])
    df.index = date_range

    pd.testing.assert_series_equal(
        agg.coverage(sel.last_60d_30d(df, today=today)),
        pd.Series(
            {
                "sepal_length": 0.53,
                "sepal_width": 0.73,
                "petal_length": 0.80,
                "petal_width": 0.77,
                "species": 0.63,
            }
        ),
        rtol=0,
        atol=0.005,
    )

    pd.testing.assert_series_equal(
        agg.coverage(sel.last_30d(df, today=today)),
        pd.Series(
            {
                "sepal_length": 0.97,
                "sepal_width": 0.87,
                "petal_length": 0.93,
                "petal_width": 0.83,
                "species": 0.87,
            }
        ),
        rtol=0,
        atol=0.005,
    )
