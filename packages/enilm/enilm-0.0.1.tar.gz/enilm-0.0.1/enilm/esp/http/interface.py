import time
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class Params:
    esp_url: str
    retries: int = 2
    grace_time: float = 0.3  # seconds


params: Optional[Params] = None


def set_params(new_params: Params):
    global params
    assert new_params.esp_url.endswith('/')
    params = new_params


class ConnFailedException(Exception):
    pass


def set_input_buffer(data: bytes) -> bool:
    assert params is not None
    assert isinstance(data, bytes)
    # TODO: assert len(data) == params.input_n_bytes

    retry = 0
    while True:
        retry += 1
        if retry == params.retries + 1:
            break

        try:
            resp = requests.put(params.esp_url + 'set_inbuf', data)
        except requests.exceptions.ConnectionError:
            # sending too many requests
            # https://stackoverflow.com/questions/23013220/max-retries-exceeded-with-url-in-requests
            time.sleep(params.grace_time)
            continue
        if resp.status_code == 200 and resp.ok and resp.text == 'Ok!':
            return True

    return False


def get_inference_result(data: Optional[bytes] = None) -> bytes:
    assert params is not None

    if data is not None:
        set_input_buffer(data)

    res: bytes = b''
    retry = 0
    while True:
        retry += 1
        if retry == params.retries + 1:
            break

        try:
            resp = requests.get(params.esp_url + 'infer')
        except requests.exceptions.ConnectionError:
            # sending too many requests
            # https://stackoverflow.com/questions/23013220/max-retries-exceeded-with-url-in-requests
            time.sleep(params.grace_time)
            continue
        if resp.status_code == 200 and resp.ok:
            res = resp.content
            break
    if res == b'':
        raise ConnFailedException
    # TODO: assert len(res) == params.output_n_bytes
    return res
