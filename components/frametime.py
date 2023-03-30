import time
from collections import deque
from typing import Optional


class FrameTimeHandler:
    def __init__(self, frame_count: int):
        self.frame_times = deque(maxlen=frame_count)
        self.frame_start = time.perf_counter()
        self.frame_count = frame_count

    def tick(self):
        frame_time = time.perf_counter() - self.frame_start
        self.frame_start = time.perf_counter()

        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.frame_count:
            self.frame_times.popleft()

    def get_average_frame_time(self) -> Optional[float]:
        if not self.frame_times:
            return None
        else:
            total_time = sum(self.frame_times)
            return total_time / len(self.frame_times)

    def get_frames_per_second(self) -> float:
        average_frame_time = self.get_average_frame_time()
        if average_frame_time is not None:
            return 1.0 / average_frame_time
        else:
            return 0.0
