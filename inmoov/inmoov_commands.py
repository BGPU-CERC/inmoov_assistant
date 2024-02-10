from session import session
from server import server
from inmoov import servo_config

from opencv.face_tracking import FaceTracker
from inmoov.idle_controller import IdleController

face_track = None
idle = None


def serial_open():
    for el in ["lt_port", "rt_port"]:
        session.session.put(
            f"{session.BASE_URL}/serial/ports/{el}", json=server.params[el]
        )


def servo_attach():
    for port, values in servo_config.servo.items():
        for item in values:
            for element, angle in item.items():
                pin = servo_config.node_to_pin.get(element)
                if pin is not None:
                    attributes = {"pin": pin, "angle": angle, "speed": 100}
                    session.session.post(
                        f"{session.BASE_URL}/serial/ports/{port}/attach",
                        json=attributes,
                    )


def set_config_pose(config, speed):
    def set_servo_angle(port, element, angle, speed):
        pin = servo_config.node_to_pin.get(element)
        if pin is not None:
            attributes = {"pin": pin, "angle": angle, "speed": speed}
            session.session.post(
                f"{session.BASE_URL}/serial/ports/{port}/set_angle",
                json=attributes,
            )

    def process_config(config, speed):
        for port, values in config.items():
            if isinstance(values, dict):  # Обработка словарей
                for element, angle in values.items():
                    set_servo_angle(port, element, angle, speed)
            else:  # Обработка кортежей
                for item in values:
                    for element, angle in item.items():
                        set_servo_angle(port, element, angle, speed)

    process_config(config, speed)


def servo_power(state):
    session.session.post(f"{session.BASE_URL}/serial/power", json={"state": state})


def set_led_state(state):
    session.session.post(f"{session.BASE_URL}/serial/led_state", json={"state": state})


def servo_dafault():
    set_config_pose(servo_config.servo, 50)


def run_face_tracking(mode):
    global face_track
    if face_track is None:
        face_track = FaceTracker()

    if mode:
        face_track.start_video_tracking()
    else:
        face_track.stop_video_tracking()
        face_track = None


def run_idle_animation(mode):
    global idle
    if idle is None:
        idle = IdleController()

    if mode:
        idle.start_idle_animation()
    else:
        idle.stop_idle_animation()
        idle = None
