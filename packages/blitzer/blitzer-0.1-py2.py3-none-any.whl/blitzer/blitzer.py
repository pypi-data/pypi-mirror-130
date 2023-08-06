import time

multipliers = {"ns": 1e9, "us": 1e6, "ms": 1e3, "s": 1}


def _format_time(seconds, unit="auto"):

    if unit == "auto":
        if seconds < 1e-6:
            unit = "ns"
        elif seconds < 1e-3:
            unit = "us"
        elif seconds < 1:
            unit = "ms"
        else:
            unit = "s"

    multiplier = multipliers[unit]

    multiplied_value = seconds * multiplier

    if multiplied_value >= 100:
        decimals = 0
    elif multiplied_value >= 10:
        decimals = 1
    else:
        decimals = 2

    time_string = f"{round(multiplied_value, decimals)} {unit}"
    return time_string


class Blitzer:
    def __init__(self, text="Runtime"):
        self.start = 0
        self.text = text

    def __enter__(self):
        self.start = time.perf_counter()

    def __exit__(self, type, value, traceback):
        runtime = time.perf_counter() - self.start
        print(f"{self.text}: {_format_time(runtime)}")
