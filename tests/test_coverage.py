from panda_detective import aggregations as agg, selections as sel, testing as tst
from datetime import date
import numpy as np
import pandas as pd
import seaborn as sns
import random

iris = sns.load_dataset("iris")


def test_coverage():
    random.seed(42)
    pd.testing.assert_series_equal(
        agg.coverage(tst.set_random_na(iris, seed=42)),
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

    # until one day before last 30 days
    rng_a = pd.date_range("2021-01-01", "2023-08-01", freq="1D")

    # last 30 days
    rng_b = pd.date_range("2023-08-02", today, freq="1D")

    # complete range
    rng_c = pd.date_range("2021-01-01", today, freq="1D")

    rna_a = tst.set_random_na(iris, ratio=0.7, seed=42)
    rna_b = tst.set_random_na(iris, ratio=0.9, seed=42)

    da = tst.sample_over_time(rna_a, rng_a, seed=42)
    db = tst.sample_over_time(rna_b, rng_b, seed=42)

    df = pd.concat([da, db])
    df.index = rng_c

    pd.testing.assert_series_equal(
        agg.coverage(sel.last_60d_30d(df, today=today)),
        pd.Series(
            {
                "sepal_length": 0.63,
                "sepal_width": 0.73,
                "petal_length": 0.70,
                "petal_width": 0.87,
                "species": 0.77,
            }
        ),
        rtol=0,
        atol=0.005,
    )

    pd.testing.assert_series_equal(
        agg.coverage(sel.last_30d(df, today=today)),
        pd.Series(
            {
                "sepal_length": 0.93,
                "sepal_width": 0.87,
                "petal_length": 0.97,
                "petal_width": 0.93,
                "species": 0.93,
            }
        ),
        rtol=0,
        atol=0.005,
    )
