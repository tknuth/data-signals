from datetime import datetime, timedelta
import pandas as pd


def last_nd_md(df, n, m, col=None, today=None):
    if today is None:
        today = pd.to_datetime(datetime.now())
    else:
        today = pd.to_datetime(today)

    if col is None:
        series = df.index
    else:
        series = df[col]

    last_nd = today - pd.to_timedelta(timedelta(days=n))
    last_nd_md = today - pd.to_timedelta(timedelta(days=m))

    return df[(series >= last_nd) & (series < last_nd_md)]


def last_60d_30d(df, col=None, today=None):
    return last_nd_md(df, 60, 30, col, today)


def last_30d(df, col=None, today=None):
    return last_nd_md(df, 30, 0, col, today)
