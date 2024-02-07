node_to_pin = {
    "thumb": 2,
    "index": 3,
    "middle": 4,
    "ring": 5,
    "pinky": 6,
    "wrist": 7,
    "bicep": 8,
    "rotate": 9,
    "shoulder": 10,
    "omoplate": 11,
    "neck": 13,
    "rollneck": 77,
    "rothead": 26,
    "jaw": 12,
    "topstom": 27,
    "midstom": 28,
    "eyeX": 12,
    "eyeY": 13,
}

hand = {
    "thumb": 0,
    "index": 0,
    "middle": 0,
    "ring": 0,
    "pinky": 0,
    "wrist": 90,
}

arm = {
    "bicep": 95,
    "rotate": 90,
    "shoulder": 150,
    "omoplate": 18,
}

head = {
    "neck": 90,
    "rollneck": 90,
    "rothead": 85,
    "jaw": 65,
}

stom = {
    "topstom": 73,
    "midstom": 90,
}

eyes = {
    "eyeX": 80,
    "eyeY": 90,
}

servo = {
    "lt_port": (hand, arm, head, stom),
    "rt_port": (hand, arm, eyes),
}
