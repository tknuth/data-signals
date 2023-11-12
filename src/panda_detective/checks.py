import re


def format_text(text):
    return re.sub(" +", " ", text.replace("\n", "")).strip()


class ScalarCheck:
    def __init__(self, description, value, signal):
        self.description = format_text(description)
        self.signal = signal
        self.value = value

    def __repr__(self):
        return f"<{self.__class__.__name__}>"


class ColumnCheck:
    def __init__(self, description, ratio, signal):
        self.description = format_text(description)
        self.signal = signal
        self.ratio = ratio

    def __repr__(self):
        return f"<{self.__class__.__name__}>"
