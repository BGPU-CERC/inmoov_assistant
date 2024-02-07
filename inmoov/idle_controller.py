import threading
import random
import time
from inmoov import gestures_config
from inmoov import inmoov_commands


class IdleController:
    def __init__(self):
        self.thread = None
        self.is_animating = False

    def process_idle_animation(self):
        self.is_animating = True
        functions = [
            (gestures_config.idle_look_left, 5),
            (gestures_config.idle_look_right, 5),
            (gestures_config.idle_look_center, 5),
        ]

        while self.is_animating:
            try:
                selected_function, speed = random.choice(functions)
                inmoov_commands.set_config_pose(selected_function, speed)
                if selected_function == gestures_config.idle_look_center:
                    inmoov_commands.set_config_pose(gestures_config.idle_grabin, 70)
                else:
                    inmoov_commands.set_config_pose(gestures_config.idle_grabout, 70)
                time.sleep(random.randint(3, 5))
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
                raise

    def start_idle_animation(self):
        self.thread = threading.Thread(target=self.process_idle_animation)
        self.thread.start()

    def stop_idle_animation(self):
        inmoov_commands.servo_dafault()
        self.is_animating = False
        self.thread.join()
