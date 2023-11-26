import pandas as pd
import numpy as np
import random


def load_people() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie", "David", "Mike"],
            "gender": ["F", "M", np.nan, "M", "X"],
            "age": [25, 32, 18, 47, np.nan],
            "height": [175, 190, np.nan, 180, 190],
        },
        index=list("abcde"),
    )


def load_fruits() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": ["Apple", "Orange", "Pear", "Pineapple", "Kiwi", np.nan],
            "weight": [80, 120, np.nan, 500, 50, 120],
        },
    )


def random_na(df, ratio=0.9, exclude=None, seed=None):
    if seed is not None:
        random.seed(seed)

    if exclude is None:
        exclude = []

    df = df.copy()

    for i, row in df.iterrows():
        for col in row.index:
            if random.random() > ratio and col not in exclude:
                df.at[i, col] = np.nan

    return df
