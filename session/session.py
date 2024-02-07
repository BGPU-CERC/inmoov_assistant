import config
import requests

BASE_URL = "http://localhost:3000/api"
HEADER = {"authorization": config.PASSWORD}

session = requests.Session()
session.headers.update(HEADER)
