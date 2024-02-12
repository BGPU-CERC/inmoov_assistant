import requests
from server import server_config
from inmoov import servo_config


session = requests.Session()
session.headers.update(server_config.HEADER)


def open_serial():
    for el in ["lt_port", "rt_port"]:
        url = f"{server_config.BASE_URL}/serial/ports/{el}"
        session.put(url, json=server_config.params[el])


def attach_servo():
    for port, values in servo_config.all_servo.items():
        for item in values:
            for element, angle in item.items():
                pin = servo_config.node_to_pin.get(element)
                if pin is not None:
                    url = f"{server_config.BASE_URL}/serial/ports/{port}/attach"
                    attributes = {"pin": pin, "angle": angle, "speed": 100}
                    session.post(
                        url,
                        json=attributes,
                    )


def set_config_pose(config, speed):
    def set_servo_angle(port, element, angle, speed):
        pin = servo_config.node_to_pin.get(element)
        if pin is not None:
            url = f"{server_config.BASE_URL}/serial/ports/{port}/set_angle"
            attributes = {"pin": pin, "angle": angle, "speed": speed}
            session.post(
                url,
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


def set_servo_power(state):
    url = f"{server_config.BASE_URL}/serial/power"
    session.post(url, json={"state": state})


def set_led_state(state):
    url = f"{server_config.BASE_URL}/serial/led_state"
    session.post(url, json={"state": state})


def set_servo_target(port, pin, angle, speed):
    url = f"{server_config.BASE_URL}/serial/ports/{port}/set_angle"
    session.post(
        url,
        json={
            "angle": angle,
            "pin": pin,
            "speed": speed,
        },
    )


def set_servo_dafault():
    set_config_pose(servo_config.all_servo, 50)
