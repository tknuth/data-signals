import numpy as np
import random


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
