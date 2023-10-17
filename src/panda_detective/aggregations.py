import pandas as pd


def coverage(x: pd.DataFrame | pd.Series):
    return x.notna().mean()
