"""by Hubertus Mitschke created on 05/29/22"""
import time


class Timer:
    """Time execution of programs"""

    def __init__(self):
        self.start = 0
        self.end = 0

    def start_timer(self) -> None:
        self.start = time.time()

    def stop_timer(self) -> None:
        self.end = time.time()

    @property
    def time_elapsed(self) -> None:
        return self.end - self.start

    def print_timing_info(self, timing_description="") -> None:
        time_elapsed = self.time_elapsed
        print(f"\n{timing_description}:")
        print(f"Time elapsed: {time_elapsed // 60 // 60 :.0f} h {time_elapsed // 60 % 60 :.0f} min {time_elapsed % 60 % 60 :.1f} sec")
