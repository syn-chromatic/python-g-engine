import time
from collections import deque

from shared_dcs import FrameTime


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

    def get_average_frame_time(self) -> float:
        if not self.frame_times:
            return 0.0

        total_time = sum(self.frame_times)
        return total_time / len(self.frame_times)

    def get_frames_per_second(self) -> float:
        average_frame_time = self.get_average_frame_time()
        if not average_frame_time:
            return 0.0

        return 1.0 / average_frame_time

    def get_frametime_data(self) -> FrameTime:
        average_fps = self.get_frames_per_second()
        frame_time = FrameTime(
            average_fps=average_fps,
        )
        return frame_time
