import datetime
import os
import time
import requests
import typing as tp

from fastapi import Depends, Response, status

from logger import get_logger
from models import *

from dotenv import load_dotenv
load_dotenv()

logger = get_logger("API")
servers = {
    "TEST": "https://games-test.datsteam.dev/",
    "MAIN": "https://games.datsteam.dev/"
}

def make_request(
        method: str, endpoint: str, body: tp.Optional[tp.Dict[str, tp.Any]] = None, 
        params: tp.Optional[tp.Dict[str, tp.Any]] = None
    ) -> tp.Optional[Response]:
    api = servers[os.getenv('SERVER')]
    url = f"{api}{endpoint}"
    headers = {
        "X-Auth-Token": os.getenv('TOKEN'),
    }
    resp = requests.request(method, url, headers=headers, json=body, params=params)

    resp_json = resp.json()
    if resp.status_code == status.HTTP_200_OK:
        logger.debug(f"{datetime.datetime.now()}\n{method} Request for URL: {url} with body: {body}\nRequest success, body: {resp_json}\n")
        return resp
    else:
        logger.error(f"{datetime.datetime.now()}\n{method} Request for URL: {url} with body: {body}\nRequest failed with status: {resp.status_code}\nError text: {resp_json}")
    return resp_json


def make_move(transports: list[CarpetMove]) -> CarpetMoveResponse:
    body = CarpetMoveRequest(transports=transports)
    resp = make_request("POST", f"play/magcarp/player/move") #, body=body)
    if resp:
        resp_json = resp.json()
        logger.error(resp_json)
        resp = CarpetMoveResponse(**resp_json)
        return resp
    else:
        raise Exception("Request failed")

# def participate() -> tp.Tuple[str, bool]:
#     headers = {
#         "X-Auth-Token": os.getenv('TOKEN'),
#     }
#     api = servers[os.getenv('SERVER')]
#     # url = f"{api}play/url/participate"

#     logger.info(datetime.datetime.now())
#     logger.info(f"Attempt to participate in round")

#     resp = requests.request("PUT", url, headers=headers)

#     if resp.status_code == status.HTTP_200_OK:
#         logger.info(f"Registered for round successfully\n")
#         return f"ROUND STARTS IN {resp.json()['startsInSec']}", False
        
#     if resp.status_code == status.HTTP_400_BAD_REQUEST:
#         if "NOT" in resp.text:
#             logger.info(f"Failed to register for round\n")
#             return f"Not participating in this round", False
#         if "not" in  resp.text:
#             logger.info(f"Rounds not found\n")
#             return f"Rounds not found", False
#         else:
#             logger.info(f"Round has already started\n")
#             return "Round has already started", True

