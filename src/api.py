import datetime
import os
import time
import requests
import typing as tp

from fastapi import Depends, Response, status

from logger import get_logger
from models import *

from dotenv import load_dotenv

from utils import IncorrectDataException
load_dotenv()

logger = get_logger("API")
servers = {
    "TEST": "https://games-test.datsteam.dev/",
    "MAIN": "https://games.datsteam.dev/"
}

def make_request(
        method: str, endpoint: str, body: tp.Optional[tp.Dict[str, tp.Any]] = None, 
        params: tp.Optional[tp.Dict[str, tp.Any]] = None
    ) -> tuple[bool, tp.Optional[Response]]:
    api = servers[os.getenv('SERVER')]
    url = f"{api}{endpoint}"
    headers = {
        "X-Auth-Token": os.getenv('TOKEN'),
    }
    resp = requests.request(method, url, headers=headers, json=body, params=params)

    resp_json = resp.json()
    if resp.status_code == status.HTTP_200_OK:
        logger.debug(f"{datetime.datetime.now()}\n{method} Request for URL: {url}\nRequest success\n")
        return True, resp_json
    
    logger.error(f"{datetime.datetime.now()}\n{method} Request for URL: {url}\nRequest failed with status: {resp.status_code}\nError text: {resp_json}")
    return False, resp_json


def make_move(transports: list[CarpetMove]) -> CarpetMoveResponse | None:
    body = CarpetMoveRequest(transports=transports).model_dump()
    success, resp_json = make_request("POST", f"play/magcarp/player/move", body=body)
    if success:
        logger.error(resp_json)
        move_resp = CarpetMoveResponse(**resp_json)
        return move_resp
    else:
        logger.error(resp_json)
        raise IncorrectDataException(resp_json)
