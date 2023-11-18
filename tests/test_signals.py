from panda_detective.signals.range import RangeSignal
from panda_detective.testing import load_people


def test_range():
    df = load_people()
    signal = RangeSignal(["age"], [18, 25])
    assert signal.config == "[18, 25]"
    assert signal.active(df).to_dict() == {
        "a": False,
        "b": True,
        "c": False,
        "d": True,
        "e": True,
    }
