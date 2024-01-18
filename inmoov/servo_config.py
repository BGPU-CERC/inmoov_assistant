DEFAULT_SPEED = 100

hand = {
    "thumb": {"pin": 2, "angle": 0, "speed": DEFAULT_SPEED},
    "index": {"pin": 3, "angle": 0, "speed": DEFAULT_SPEED},
    "middleFinger": {"pin": 4, "angle": 0, "speed": DEFAULT_SPEED},
    "ringFinger": {"pin": 5, "angle": 0, "speed": DEFAULT_SPEED},
    "pinky": {"pin": 6, "angle": 0, "speed": DEFAULT_SPEED},
    "wrist": {"pin": 7, "angle": 90, "speed": DEFAULT_SPEED},
}

arm = {
    "bicep": {"pin": 8, "angle": 95, "speed": DEFAULT_SPEED},
    "rotate": {"pin": 9, "angle": 90, "speed": DEFAULT_SPEED},
    "shoulder": {"pin": 10, "angle": 150, "speed": DEFAULT_SPEED},
    "omoplate": {"pin": 11, "angle": 18, "speed": DEFAULT_SPEED},
}

head = {
    "neck": {"pin": 13, "angle": 90, "speed": DEFAULT_SPEED},
    "rollneck": {"pin": 77, "angle": 90, "speed": DEFAULT_SPEED},
    "rothead": {"pin": 26, "angle": 85, "speed": DEFAULT_SPEED},
    "jaw": {"pin": 12, "angle": 65, "speed": DEFAULT_SPEED},
}

stom = {
    "topstom": {"pin": 27, "angle": 73, "speed": DEFAULT_SPEED},
    "midstom": {"pin": 28, "angle": 90, "speed": DEFAULT_SPEED},
}

eyes = {
    "eyeX": {"pin": 12, "angle": 80, "speed": DEFAULT_SPEED},
    "eyeY": {"pin": 13, "angle": 90, "speed": DEFAULT_SPEED},
}

servo = {
    "lt_port": (hand, arm, head, stom),
    "rt_port": (hand, arm, eyes),
}
