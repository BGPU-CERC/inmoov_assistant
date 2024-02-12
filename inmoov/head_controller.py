from server.api import api


class HeadController:
    def __init__(self):
        self.neck_middle = 90
        self.neck_min = 50
        self.neck_max = 140

        self.rothead_middle = 90
        self.rothead_min = 40
        self.rothead_max = 160

        self.rothead_current = self.rothead_middle
        self.neck_current = self.neck_middle

    @staticmethod
    def map(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def adjust_head_position(self, x_center, y_center, frame_width, frame_height):
        errorX = int(frame_width / 2) - x_center
        errorY = int(frame_height / 2) - y_center

        dx = self.map(abs(errorX), 10, frame_width / 2, 1, 5)
        dy = self.map(abs(errorY), 10, frame_height / 2, 1, 5)

        if errorX < -20:
            if self.rothead_current < self.rothead_max:
                self.rothead_current += dx
        elif errorX > 20:
            if self.rothead_current > self.rothead_min:
                self.rothead_current -= dx

        if errorY < -20:
            if self.neck_current < self.neck_max:
                self.neck_current += dy
        elif errorY > 20:
            if self.neck_current > self.neck_min:
                self.neck_current -= dy

        print(
            f"rothead angle: {self.rothead_current} neck angle: {self.neck_current} errorX: {errorX} errorY: {errorY}"
        )

        api.set_servo_target("lt_port", 26, self.rothead_current, 100)
        api.set_servo_target("lt_port", 13, self.neck_current, 100)
