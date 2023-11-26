import functools


def ignore_na(func):
    @functools.wraps(func)
    def wrapper(self, df):
        active = func(self, df)
        return active.mask(df[self.column].isna(), False)

    return wrapper
