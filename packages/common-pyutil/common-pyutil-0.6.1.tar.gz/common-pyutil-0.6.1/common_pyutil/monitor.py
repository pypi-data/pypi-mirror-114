import time


class Timer:
    """A timer context for easily timing blocks of code.

    Args:
        accumulate: Whether to accumulate time over multiple context entries
                    A value of `False` means timer is reset each time the
                    context is entered.

    Example:
        timer = Timer()
        with timer:
            retval = some_function(arg1, arg2)
        print(timer.time)              # prints e.g., 3.14159
        print(timer.as_dict)           # prints e.g., {"time": 3.14159}

    """
    def __init__(self, accumulate=False):
        self._accumulate = accumulate
        self._time = 0

    def __enter__(self):
        self._start = time.time()

    def __exit__(self, *args):
        if self.accumulate:
            self._time += time.time() - self._start
        else:
            self._time = time.time() - self._start

    def clear(self):
        "Clear the timer instance"
        self._time = 0

    @property
    def time(self) -> float:
        "Return the time"
        return self._time

    @property
    def accumulate(self) -> bool:
        "Are we accumulating the times?"
        return self._accumulate

    @property
    def as_dict(self):
        "As a dictionary of {\"time\": time}"
        return {"time": self._time}
