import requests
from inmoov import server_config
from time import time


class PID:
    p: float
    i: float
    d: float
    min_value: float
    max_value: float
    integral: float
    prev_error: float | None
    prev_time: float

    def __init__(
        self,
        p: float,
        i: float,
        d: float,
        min_value: float = float("-inf"),
        max_value: float = float("inf"),
    ) -> None:
        self.p = p
        self.i = i
        self.d = d

        self.min_value = min_value
        self.max_value = max_value

        self.integral = 0.0
        self.prev_error = None  # type: Optional[float]
        self.prev_time = time()

    def __call__(self, target: float, value: float) -> float:
        error = target - value

        if self.prev_error is None:
            self.prev_error = error
            de = 0.0
        else:
            de = error - self.prev_error
            self.prev_error = error

        dt = time() - self.prev_time

        self.integral += error * dt
        self.prev_error = error
        self.prev_time = time()

        return min(
            max(
                self.p * error
                + self.i * self.integral
                + (self.d * de / dt if dt != 0 else 0),
                self.min_value,
            ),
            self.max_value,
        )

    def clear(self) -> None:
        self.integral = 0.0
        self.prev_error = 0.0
        self.prev_time = time()


class HeadController:
    def __init__(self):
        self.rothead_PID = PID(0.7, 0, 0.05, 60, 130)

        self.neck_middle = 90
        self.neck_min = 50
        self.neck_max = 140

        self.rothead_middle = 95
        self.rothead_min = 60
        self.rothead_max = 130

        self.rothead_current = self.rothead_middle
        self.neck_current = self.neck_middle

    @staticmethod
    def map(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def adjust_head_position(self, x_center, y_center, frame_width, frame_height):
        rothead_angle = self.rothead_PID(frame_width / 2, x_center)
        rothead_angle = 180 - rothead_angle
        # rothead_angle = self.rothead_PID(x_center, frame_width / 2)
        # print(f"rothead angle: {rothead_angle}")

        # errorX = int(frame_width / 2) - x_center
        # errorY = int(frame_height / 2) - y_center

        # value = self.map(abs(errorX), 0, 600, 1, 10)

        # if errorX < 0:
        #     if self.rothead_current < self.rothead_max:
        #         self.rothead_current += value
        # else:
        #     if self.rothead_current > self.rothead_min:
        #         self.rothead_current -= value

        # if errorY < 0:
        #     if self.neck_current < self.neck_min:
        #         self.neck_current += 1
        # else:
        #     if self.neck_current > self.neck_min:
        #         self.neck_current -= 1
        # ------------------

        print(f"rothead angle: {rothead_angle}")

        requests.post(
            f"{server_config.BASE_URL}/serial/ports/lt_port/set_angle",
            json={
                # "angle": int(self.rothead_current),
                "angle": rothead_angle,
                "pin": 26,
                "speed": 10,
            },
        )

        # requests.post(
        #     f"{server_config.BASE_URL}/serial/ports/lt_port/set_angle",
        #     json={
        #         "angle": tilt_angle,
        #         "pin": 13,
        #         "speed": 30,
        #     },
        # )
