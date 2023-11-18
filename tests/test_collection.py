from panda_detective.collection import *
from panda_detective.testing import load_people
import numpy as np
import pandas as pd


def test_signals():
    df = load_people()
    sc = SignalCollection(df)
    sc.select("age").range([20, 50])
    sc.select("height").range([180, 190])
    sc.notna()
    print()
    print(sc.evaluate(df).show())
    print(sc.evaluate(df).summarize())


# dg.signal == "notna(age)"
# print()
# print(sc.evaluate(df))
