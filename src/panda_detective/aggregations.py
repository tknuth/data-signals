import pandas as pd


def coverage(x: pd.DataFrame | pd.Series):
    return x.notna().mean()


def count_notna(x: pd.DataFrame | pd.Series):
    return x.notna().sum()


def count_na(x: pd.DataFrame | pd.Series):
    return x.isna().sum()

# TODO: format as fraction, i.e. [a, a+b]
def count_notna_na(x: pd.DataFrame | pd.Series):
    return [x.notna().sum(), x.isna().sum()]
