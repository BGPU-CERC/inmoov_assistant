import config

BASE_URL = "http://localhost:3000/api"
HEADER = {"authorization": config.PASSWORD}

params = {
    "lt_port": {
        "path": "COM5",
        "rate": 115200,
    },
    "rt_port": {
        "path": "COM4",
        "rate": 115200,
    },
}
