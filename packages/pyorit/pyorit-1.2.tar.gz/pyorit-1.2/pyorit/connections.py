# OrangIT - UserBot
# Copyright (C) 2021 OrangIT
#
# This file is a part of < https://github.com/Projectgeez/OrangIT/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/OrangIT/OrangIT/blob/main/LICENSE/>.

import os
import time
from logging import INFO, FileHandler, StreamHandler, basicConfig, getLogger

import redis
from decouple import config
from pyrogram import Client
from pytgcalls import PyLogs, PyTgCalls
from telethon import TelegramClient
from telethon import __version__ as vers
from telethon.errors.rpcerrorlist import (
    ApiIdInvalidError,
    AuthKeyDuplicatedError,
    PhoneNumberInvalidError,
)
from telethon.sessions import StringSession

from .dB.database import Var
from .version import __version__ as ver
from .version import OrangIT_version

LOGS = getLogger("pyorit")

if os.path.exists("OrangIT.log"):
    try:
        os.remove("OrangIT.log")
    except BaseException:
        pass

basicConfig(
    format="%(asctime)s || %(name)s [%(levelname)s] - %(message)s",
    level=INFO,
    datefmt="%m/%d/%Y, %H:%M:%S",
    handlers=[FileHandler("OrangIT.log"), StreamHandler()],
)

LOGS.info(
    """
                -----------------------------------
                        Memulai Proses
                -----------------------------------
"""
)
LOGS.info(f"Versi pyorit - {ver}")
LOGS.info(f"Versi Telethon - {vers}")
LOGS.info(f"Versi OrangIT - {OrangIT_version}")


def connect_redis():
    if Var.REDIS_URI and Var.REDIS_PASSWORD:
        err = ""
        if ":" not in Var.REDIS_URI:
            err += "\nREDIS_URI salah. Berhenti...\n"
        if "/" in Var.REDIS_URI:
            err += "REDIS_URI Anda harus dimulai dengan redis.xxx. Berhenti...\n"
        if " " in Var.REDIS_URI:
            err += "Hapus spasi dari REDIS_URI\n"
        if " " in Var.REDIS_PASSWORD:
            err += "Hapus spasi dari REDIS_PASSWORD\n"
        if "\n" in Var.REDIS_URI:
            err += "Hapus baris baru dari REDIS_URI\n"
        if "\n" in Var.REDIS_PASSWORD:
            err += "Hapus baris baru dari REDIS_PASSWORD\n"
        if err != "":
            LOGS.info(err)
            exit(1)
        redis_info = Var.REDIS_URI.split(":")
        LOGS.info("Mendapatkan Koneksi Dengan Database Redis")
        time.sleep(3.5)
        return redis.Redis(
            host=redis_info[0],
            port=redis_info[1],
            password=Var.REDIS_PASSWORD,
            decode_responses=True,
        )
    else:
        LOGS.info("Mendapatkan Koneksi Dengan Database Redis")
        time.sleep(3.5)
        return connect_qovery_redis()
        """
        uri, passw = get_redis_vars()
        redis_info = uri.split(":")
        return redis.Redis(
            host=redis_info[0],
            port=redis_info[1],
            password=passw,
            decode_responses=True,
        )
        """


def redis_connection():
    our_db = connect_redis()
    time.sleep(5)
    try:
        our_db.ping()
    except BaseException:
        connected = []
        LOGS.info("Tidak dapat terhubung ke Redis Database.... Mencoba Ulang....")
        for x in range(1, 6):
            try:
                our_db = connect_redis()
                time.sleep(3)
                if our_db.ping():
                    connected.append(1)
                    break
            except BaseException as conn:
                LOGS.info(
                    f"{(conn)}\nKoneksi gagal ...  Mencoba Ulang {x}/5 .."
                )
        if not connected:
            LOGS.info("Koneksi Redis Gagal.....")
            exit(1)
        else:
            LOGS.info("Berhasil Terhubung Ke Server Redis")
    LOGS.info("Berhasil Membuat Koneksi Dengan Redis DataBase.")
    return our_db


def session_file():
    if os.path.exists("client-session.session"):
        _session = "client-session"
    elif Var.SESSION:
        _session = StringSession(Var.SESSION)
    else:
        LOGS.info("Sesi String tidak ditemukan. Berhenti...")
        exit(1)
    return _session


def client_connection():
    try:
        client = TelegramClient(session_file(), Var.API_ID, Var.API_HASH)
        bot_client = TelegramClient(None, api_id=Var.API_ID, api_hash=Var.API_HASH)
    except (AuthKeyDuplicatedError, PhoneNumberInvalidError, EOFError):
        LOGS.info(
            "Sesi String Kedaluwarsa. Silakan Buat Sesi String Baru. Berhenti..."
        )
        exit(1)
    except ApiIdInvalidError:
        LOGS.info(
            "Kombinasi API_ID dan API_HASH tidak valid. Silahkan Cek Ulang. Berhenti..."
        )
        exit(1)
    except Exception as ap:
        LOGS.info(f"ERROR - {ap}")
        exit(1)
    return client, bot_client


def vc_connection(udB):
    VC_SESSION = udB.get("VC_SESSION") or Var.VC_SESSION
    if VC_SESSION:
        try:
            vcasst = Client(
                ":memory:",
                api_id=Var.API_ID,
                api_hash=Var.API_HASH,
                bot_token=udB.get("BOT_TOKEN"),
            )
            vcClient = Client(VC_SESSION, api_id=Var.API_ID, api_hash=Var.API_HASH)
            CallsClient = PyTgCalls(vcClient, log_mode=PyLogs.verbose)
            return vcasst, vcClient, CallsClient
        except Exception as er:
            LOGS.info(str(er))
    return None, None, None


def connect_qovery_redis():
    uri = config("REDIS_URI", default=None)
    passw = config("REDIS_PASSWORD", default=None)
    if not uri and not passw:
        var = ""
        for i in os.environ:
            if i.startswith("QOVERY_REDIS_") and i.endswith("_PORT"):
                var = i
        if var:
            try:
                hash = var.split("QOVERY_REDIS_")[1].split("_")[0]
                # or config(f"QOVERY_REDIS_{hash}_HOST")
                endpoint = os.environ[f"QOVERY_REDIS_{hash}_HOST"]
                # or config(f"QOVERY_REDIS_{hash}_PORT")
                port = os.environ[f"QOVERY_REDIS_{hash}_PORT"]
                # or config(f"QOVERY_REDIS_{hash}_PASSWORD")
                passw = os.environ[f"QOVERY_REDIS_{hash}_PASSWORD"]
            except KeyError:
                LOGS.info("Redis Vars hilang. Berhenti.")
                exit(1)
            except Exception as er:
                LOGS.info(er)
                exit(1)
            # uri = endpoint + ":" + str(port)
    return redis.Redis(
        host=endpoint,
        port=str(port),
        password=passw,
        decode_responses=True,
    )
    # return uri, passw
