import numpy as np
import random


def set_random_na(df, ratio=0.9, exclude=None, seed=None):
    if seed is not None:
        random.seed(seed)
    df = df.copy()
    if exclude is None:
        exclude = []
    for i, row in df.iterrows():
        for col in row.index:
            if random.random() > ratio and col not in exclude:
                df.at[i, col] = np.nan
    return df


def sample_over_time(df, date_range, seed=None):
    df = df.sample(len(date_range), replace=True, random_state=seed).reset_index(drop=True)
    df.index = date_range
    return df
