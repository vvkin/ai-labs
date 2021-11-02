import time

class Timer:
    def __init__(self) -> None:
        self.reset()
    
    @property
    def elapsed(self) -> float:
        if self._elapsed is None:
            raise Exception("Timer hasn't started!")
        else: return self._elapsed
    
    def start(self) -> None:
        self._start = time.perf_counter()
    
    def stop(self) -> None:
        now = time.perf_counter()
        self._elapsed = now - self._start
    
    def reset(self) -> None:
        self._start = None
        self._elapsed = None
