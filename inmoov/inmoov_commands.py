import requests

from inmoov import server_config
from inmoov import servo_config

from opencv.face_trak import FaceTracker

face_track = None
session = requests.Session()
session.headers.update(server_config.HEADER)


def serial_open():
    for el in ["lt_port", "rt_port"]:
        session.put(
            f"{server_config.BASE_URL}/serial/ports/{el}", json=server_config.params[el]
        )


def servo_attach():
    for port, values in servo_config.servo.items():
        for item in values:
            for _, attributes in item.items():
                session.post(
                    f"{server_config.BASE_URL}/serial/ports/{port}/attach",
                    json={
                        "pin": attributes["pin"],
                        "angle": attributes["angle"],
                        "speed": attributes["speed"],
                    },
                )


def servo_power(state):
    session.post(f"{server_config.BASE_URL}/serial/power", json={"state": state})


def set_led_state(state):
    session.post(f"{server_config.BASE_URL}/serial/led_state", json={"state": state})


def servo_dafault():
    for port, values in servo_config.servo.items():
        for item in values:
            for _, attributes in item.items():
                session.post(
                    f"{server_config.BASE_URL}/serial/ports/{port}/set_angle",
                    json={
                        "pin": attributes["pin"],
                        "angle": attributes["angle"],
                        "speed": attributes["speed"],
                    },
                )


def face_tracking(mode):
    global face_track
    if face_track is None:
        face_track = FaceTracker()

    if mode:
        face_track.start_video_tracking()
    else:
        # face_track.release_capture()
        face_track.stop_video_tracking()
        face_track = None
        # del face_track


def stay_balance3():
    session.post(
        f"{server_config.BASE_URL}/serial/ports/lt_port/set_angle",
        json={
            "angle": 93,
            "pin": 27,
            "speed": 10,
        },
    )


def stay_balance2():
    session.post(
        f"{server_config.BASE_URL}/serial/ports/lt_port/set_angle",
        json={
            "angle": 53,
            "pin": 27,
            "speed": 10,
        },
    )


def stay_balance1():
    session.post(
        f"{server_config.BASE_URL}/serial/ports/rt_port/set_angle",
        json={
            "angle": 180,
            "pin": 7,
            "speed": 100,
        },
    )
    session.post(
        f"{server_config.BASE_URL}/serial/ports/rt_port/set_angle",
        json={
            "angle": 170,
            "pin": 10,
            "speed": 100,
        },
    )
    session.post(
        f"{server_config.BASE_URL}/serial/ports/rt_port/set_angle",
        json={
            "angle": 65,
            "pin": 11,
            "speed": 100,
        },
    )
    session.post(
        f"{server_config.BASE_URL}/serial/ports/lt_port/set_angle",
        json={
            "angle": 180,
            "pin": 7,
            "speed": 100,
        },
    )
    session.post(
        f"{server_config.BASE_URL}/serial/ports/lt_port/set_angle",
        json={
            "angle": 170,
            "pin": 10,
            "speed": 100,
        },
    )
    session.post(
        f"{server_config.BASE_URL}/serial/ports/lt_port/set_angle",
        json={
            "angle": 65,
            "pin": 11,
            "speed": 100,
        },
    )


def lbicep_up():
    session.post(
        f"{server_config.BASE_URL}/serial/porst/lt_port/set_angle",
        json={"angle": 10, "pin": 8, "speed": 100},
    )


def lbicep_down():
    session.post(
        f"{server_config.BASE_URL}/serial/porst/lt_port/set_angle",
        json={"angle": 95, "pin": 8, "speed": 100},
    )


def check_rhand():
    session.post(
        f"{server_config.BASE_URL}/serial/ports/rt_port/set_angle",
        json={
            "angle": 27,
            "pin": 7,
            "speed": 10,
        },
    )
    session.post(
        f"{server_config.BASE_URL}/serial/ports/rt_port/set_angle",
        json={
            "angle": 20,
            "pin": 8,
            "speed": 100,
        },
    )
    session.post(
        f"{server_config.BASE_URL}/serial/ports/rt_port/set_angle",
        json={
            "angle": 90,
            "pin": 9,
            "speed": 100,
        },
    )
    session.post(
        f"{server_config.BASE_URL}/serial/ports/rt_port/set_angle",
        json={
            "angle": 116,
            "pin": 10,
            "speed": 100,
        },
    )
    session.post(
        f"{server_config.BASE_URL}/serial/ports/rt_port/set_angle",
        json={
            "angle": 30,
            "pin": 11,
            "speed": 100,
        },
    )
    session.post(
        f"{server_config.BASE_URL}/serial/ports/lt_port/set_angle",
        json={
            "angle": 140,
            "pin": 13,
            "speed": 100,
        },
    )
    session.post(
        f"{server_config.BASE_URL}/serial/ports/lt_port/set_angle",
        json={
            "angle": 115,
            "pin": 26,
            "speed": 100,
        },
    )
