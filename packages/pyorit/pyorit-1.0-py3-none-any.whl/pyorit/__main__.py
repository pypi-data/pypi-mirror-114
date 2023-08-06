# OrangIT - UserBot
# Copyright (C) 2021 OrangIT
#
# This file is a part of < https://github.com/Projectgeez/OrangIT/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/OrangIT/OrangIT/blob/main/LICENSE/>.

import asyncio
import multiprocessing
import os
import time
import traceback
import urllib
from pathlib import Path
from random import randint
from urllib.request import urlretrieve

from pyrogram import idle
from pytz import timezone
from telethon.errors.rpcerrorlist import (
    AccessTokenExpiredError,
    ApiIdInvalidError,
    AuthKeyDuplicatedError,
    ChannelsTooMuchError,
    PhoneNumberInvalidError,
)
from telethon.tl.custom import Button
from telethon.tl.functions.channels import (
    CreateChannelRequest,
    EditAdminRequest,
    EditPhotoRequest,
    JoinChannelRequest,
)
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.types import (
    ChatAdminRights,
    InputChatUploadedPhoto,
    InputMessagesFilterDocument,
)

from . import *
from .dB import DEVLIST
from .dB.database import Var
from .functions.all import updater
from .loader import plugin_loader
from .utils import load_addons

x = ["resources/auths", "resources/downloads", "addons"]
for x in x:
    if not os.path.isdir(x):
        os.mkdir(x)

if udB.get("CUSTOM_THUMBNAIL"):
    urlretrieve(udB.get("CUSTOM_THUMBNAIL"), "resources/extras/OrangIT.jpg")

if udB.get("GDRIVE_TOKEN"):
    with open("resources/auths/auth_token.txt", "w") as t_file:
        t_file.write(udB.get("GDRIVE_TOKEN"))

if udB.get("MEGA_MAIL") and udB.get("MEGA_PASS"):
    with open(".megarc", "w") as mega:
        mega.write(
            f'[Login]\nUsername = {udB.get("MEGA_MAIL")}\nPassword = {udB.get("MEGA_PASS")}'
        )

if udB.get("TIMEZONE"):
    try:
        timezone(udB.get("TIMEZONE"))
        os.environ["TZ"] = udB.get("TIMEZONE")
        time.tzset()
    except BaseException:
        LOGS.info(
            "Zona Waktu Salah ,\nPeriksa Zona Waktu yang Tersedia Dari Sini https://timezonedb.com/time-zones\nJadi Waktu adalah UTC Secara Default"
        )
        os.environ["TZ"] = "UTC"
        time.tzset()


async def autobot():
    await OrangIT_bot.start()
    if Var.BOT_TOKEN:
        udB.set("BOT_TOKEN", str(Var.BOT_TOKEN))
        return
    if udB.get("BOT_TOKEN"):
        return
    LOGS.info("MEMBUAT BOT TELEGRAM UNTUK ANDA DI @BotFather , Mohon Tunggu")
    who = await OrangIT_bot.get_me()
    name = who.first_name + "'s Assistant Bot"
    if who.username:
        username = who.username + "_bot"
    else:
        username = "OrangIT_" + (str(who.id))[5:] + "_bot"
    bf = "Botfather"
    await OrangIT_bot(UnblockRequest(bf))
    await OrangIT_bot.send_message(bf, "/cancel")
    await asyncio.sleep(1)
    await OrangIT_bot.send_message(bf, "/start")
    await asyncio.sleep(1)
    await OrangIT_bot.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    isdone = (await OrangIT_bot.get_messages(bf, limit=1))[0].text
    if isdone.startswith("Itu tidak bisa saya lakukan."):
        LOGS.info(
            "Silakan buat Bot dari @BotFather dan tambahkan tokennya di BOT_TOKEN, sebagai env var dan restart saya."
        )
        exit(1)
    await OrangIT_bot.send_message(bf, name)
    await asyncio.sleep(1)
    isdone = (await OrangIT_bot.get_messages(bf, limit=1))[0].text
    if not isdone.startswith("Bagus."):
        await OrangIT_bot.send_message(bf, "Bot Assistant Ku")
        await asyncio.sleep(1)
        isdone = (await OrangIT_bot.get_messages(bf, limit=1))[0].text
        if not isdone.startswith("Bagus."):
            LOGS.info(
            "Silakan buat Bot dari @BotFather dan tambahkan tokennya di BOT_TOKEN, sebagai env var dan restart saya."
        )
            exit(1)
    await OrangIT_bot.send_message(bf, username)
    await asyncio.sleep(1)
    isdone = (await OrangIT_bot.get_messages(bf, limit=1))[0].text
    await OrangIT_bot.send_read_acknowledge("botfather")
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = "OrangIT_" + (str(who.id))[6:] + str(ran) + "_bot"
        await OrangIT_bot.send_message(bf, username)
        await asyncio.sleep(1)
        nowdone = (await OrangIT_bot.get_messages(bf, limit=1))[0].text
        if nowdone.startswith("Done!"):
            token = nowdone.split("`")[1]
            udB.set("BOT_TOKEN", token)
            await OrangIT_bot.send_message(bf, "/setinline")
            await asyncio.sleep(1)
            await OrangIT_bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await OrangIT_bot.send_message(bf, "Search")
            LOGS.info(f"SELESAI BOT TELEGRAM ANDA SUKSES DIBUAT @{username}")
        else:
            LOGS.info(
                f"Silakan Hapus Beberapa Bot Telegram Anda di @Botfather atau Set Var BOT_TOKEN dengan token bot"
            )
            exit(1)
    elif isdone.startswith("Selesai!"):
        token = isdone.split("`")[1]
        udB.set("BOT_TOKEN", token)
        await OrangIT_bot.send_message(bf, "/setinline")
        await asyncio.sleep(1)
        await OrangIT_bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await OrangIT_bot.send_message(bf, "Search")
        LOGS.info(f"SELESAI BOT TELEGRAM ANDA SUKSES DIBUAT @{username}")
    else:
        LOGS.info(
            f"Silakan Hapus Beberapa Bot Telegram Anda di @Botfather atau Set Var BOT_TOKEN dengan token bot"
        )
        exit(1)


if not udB.get("BOT_TOKEN"):
    OrangIT_bot.loop.run_until_complete(autobot())


async def istart():
    OrangIT_bot.me = await OrangIT_bot.get_me()
    OrangIT_bot.uid = OrangIT_bot.me.id
    OrangIT_bot.first_name = OrangIT_bot.me.first_name
    if not OrangIT_bot.me.bot:
        udB.set("OWNER_ID", OrangIT_bot.uid)


async def autopilot():
    if Var.LOG_CHANNEL and str(Var.LOG_CHANNEL).startswith("-100"):
        udB.set("LOG_CHANNEL", str(Var.LOG_CHANNEL))
    k = []  # To Refresh private ids
    async for x in OrangIT_bot.iter_dialogs():
        k.append(x.id)
    if udB.get("LOG_CHANNEL"):
        try:
            await OrangIT_bot.get_entity(int(udB.get("LOG_CHANNEL")))
            return
        except BaseException:
            udB.delete("LOG_CHANNEL")
    try:
        r = await OrangIT_bot(
            CreateChannelRequest(
                title="Logs OrangIT Ku",
                about="Grup Log OrangIT Saya\n\n Bergabunglah dengan @OrangIT",
                megagroup=True,
            ),
        )
    except ChannelsTooMuchError:
        LOGS.info(
            "Anda Terlalu Banyak Channel & Grup, Tinggalkan Beberapa Dan Mulai Ulang Bot"
        )
        exit(1)
    except BaseException:
        LOGS.info(
            "Ada yang Salah, Buat Grup dan atur id-nya di config var LOG_CHANNEL."
        )
        exit(1)
    chat_id = r.chats[0].id
    if not str(chat_id).startswith("-100"):
        udB.set("LOG_CHANNEL", "-100" + str(chat_id))
    else:
        udB.set("LOG_CHANNEL", str(chat_id))
    rights = ChatAdminRights(
        add_admins=True,
        invite_users=True,
        change_info=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
        anonymous=False,
        manage_call=True,
    )
    await OrangIT_bot(EditAdminRequest(chat_id, asst.me.username, rights, "Assistant"))
    pfpa = await OrangIT_bot.download_profile_photo(chat_id)
    if not pfpa:
        urllib.request.urlretrieve(
            "https://telegra.ph/file/bf9627e0e9cdc6a71baf3.jpg", "channelphoto.jpg"
        )
        ll = await OrangIT_bot.upload_file("channelphoto.jpg")
        await OrangIT_bot(EditPhotoRequest(chat_id, InputChatUploadedPhoto(ll)))
        os.remove("channelphoto.jpg")
    else:
        os.remove(pfpa)


async def bot_info():
    asst.me = await asst.get_me()
    return asst.me


LOGS.info("Initialising...")


# log in
BOT_TOKEN = udB.get("BOT_TOKEN")
LOGS.info("Starting OrangIT...")
try:
    asst.start(bot_token=BOT_TOKEN)
    OrangIT_bot.start()
    OrangIT_bot.loop.run_until_complete(istart())
    OrangIT_bot.loop.run_until_complete(bot_info())
    LOGS.info("Done, startup completed")
    LOGS.info("Assistant - Started")
except (AuthKeyDuplicatedError, PhoneNumberInvalidError, EOFError):
    LOGS.info("Session String expired. Please create a new one! OrangIT is stopping...")
    exit(1)
except ApiIdInvalidError:
    LOGS.info("Your API ID/API HASH combination is invalid. Kindly recheck.")
    exit(1)
except AccessTokenExpiredError:
    udB.delete("BOT_TOKEN")
    LOGS.info(
        "BOT_TOKEN expired , So Quitted The Process, Restart Again To create A new Bot. Or Set BOT_TOKEN env In Vars"
    )
    exit(1)
except BaseException:
    LOGS.info("Error: " + str(traceback.print_exc()))
    exit(1)


if str(OrangIT_bot.uid) not in DEVLIST:
    chat = eval(udB.get("BLACKLIST_CHATS"))
    if -1001327032795 not in chat:
        chat.append(-1001327032795)
        udB.set("BLACKLIST_CHATS", str(chat))

OrangIT_bot.loop.run_until_complete(autopilot())

pmbot = udB.get("PMBOT")
manager = udB.get("MANAGER")
addons = udB.get("ADDONS") or Var.ADDONS
vcbot = udB.get("VC_SESSION") or Var.VC_SESSION

plugin_loader(addons=addons, pmbot=pmbot, manager=manager, vcbot=vcbot)

# for channel plugins
Plug_channel = udB.get("PLUGIN_CHANNEL")
if Plug_channel:

    async def plug():
        try:
            if Plug_channel.startswith("@"):
                chat = Plug_channel
            else:
                try:
                    chat = int(Plug_channel)
                except BaseException:
                    return
            async for x in OrangIT_bot.iter_messages(
                chat, search=".py", filter=InputMessagesFilterDocument
            ):
                await asyncio.sleep(0.6)
                files = await OrangIT_bot.download_media(x.media, "./addons/")
                file = Path(files)
                plugin = file.stem
                if "(" not in files:
                    try:
                        load_addons(plugin.replace(".py", ""))
                        LOGS.info(f"OrangIT - PLUGIN_CHANNEL - Installed - {plugin}")
                    except Exception as e:
                        LOGS.info(f"OrangIT - PLUGIN_CHANNEL - ERROR - {plugin}")
                        LOGS.info(str(e))
                else:
                    LOGS.info(f"Plugin {plugin} is Pre Installed")
                    os.remove(files)
        except Exception as e:
            LOGS.info(str(e))


# customize assistant


async def customize():
    try:
        chat_id = int(udB.get("LOG_CHANNEL"))
        xx = await OrangIT_bot.get_entity(asst.me.username)
        if xx.photo is None:
            LOGS.info("KUSTOMISASI BOT MU DI @BOTFATHER")
            UL = f"@{asst.me.username}"
            if (OrangIT_bot.me.username) is None:
                sir = OrangIT_bot.me.first_name
            else:
                sir = f"@{OrangIT_bot.me.username}"
            await OrangIT_bot.send_message(
                chat_id, "Kustomisasi Otomatis Di Mulai Di @botfather"
            )
            await asyncio.sleep(1)
            await OrangIT_bot.send_message("botfather", "/cancel")
            await asyncio.sleep(1)
            await OrangIT_bot.send_message("botfather", "/start")
            await asyncio.sleep(1)
            await OrangIT_bot.send_message("botfather", "/setuserpic")
            await asyncio.sleep(1)
            await OrangIT_bot.send_message("botfather", UL)
            await asyncio.sleep(1)
            await OrangIT_bot.send_file(
                "botfather", "resources/extras/OrangIT_assistant.jpg"
            )
            await asyncio.sleep(2)
            await OrangIT_bot.send_message("botfather", "/setabouttext")
            await asyncio.sleep(1)
            await OrangIT_bot.send_message("botfather", UL)
            await asyncio.sleep(1)
            await OrangIT_bot.send_message(
                "botfather", f"✨ Hai ✨!! Saya Asisten dari tuan {sir}"
            )
            await asyncio.sleep(2)
            await OrangIT_bot.send_message("botfather", "/setdescription")
            await asyncio.sleep(1)
            await OrangIT_bot.send_message("botfather", UL)
            await asyncio.sleep(1)
            await OrangIT_bot.send_message(
                "botfather",
                f"✨ PowerFul OrangIT Bot Assistant ✨\n✨ Master ~ {sir} ✨\n\n✨ Powered By ~ @GeezSupportGroup ✨",
            )
            await asyncio.sleep(2)
            await OrangIT_bot.send_message(
                chat_id, "**Kustomisasi Otomatis** Selesai di @BotFather"
            )
            LOGS.info("Kustomisasi Selesai")
    except Exception as e:
        LOGS.info(str(e))


# some stuffs
async def ready():
    chat_id = int(udB.get("LOG_CHANNEL"))
    MSG = f"**OrangIT Teleah Dideploy!**\n➖➖➖➖➖➖➖➖➖\n**UserMode**: [{OrangIT_bot.me.first_name}](tg://user?id={OrangIT_bot.me.id})\n**Assistant**: @{asst.me.username}\n➖➖➖➖➖➖➖➖➖\n**Support**: @GeezSupportGroup\n➖➖➖➖➖➖➖➖➖"
    BTTS = [Button.inline("Help", "open")]
    updava = await updater()
    try:
        if updava:
            BTTS = [
                [Button.inline("Pembaruan Tersedia", "updtavail")],
                [Button.inline("Menu", "open")],
            ]
        await asst.send_message(chat_id, MSG, buttons=BTTS)
    except BaseException:
        try:
            await OrangIT_bot.send_message(chat_id, MSG)
        except Exception as ef:
            LOGS.info(ef)
    try:
        # To Let Them know About New Updates and Changes
        await OrangIT_bot(JoinChannelRequest("@TheOrangIT"))
    except BaseException:
        pass


def pycli():
    vcasst.start()
    multiprocessing.Process(target=idle).start()
    CallsClient.run()


suc_msg = """
            ----------------------------------------------------------------------
            >   OrangIT telah Dideploy! Kunjungi @UserbotChannel untuk pembaruan!!
            ----------------------------------------------------------------------
"""

OrangIT_bot.loop.run_until_complete(customize())
if Plug_channel:
    OrangIT_bot.loop.run_until_complete(plug())
OrangIT_bot.loop.run_until_complete(ready())


if __name__ == "__main__":
    if vcbot:
        if vcasst and vcClient and CallsClient:
            multiprocessing.Process(target=pycli).start()
        LOGS.info(suc_msg)
        multiprocessing.Process(target=OrangIT_bot.run_until_disconnected).start()
    else:
        LOGS.info(suc_msg)
        OrangIT_bot.run_until_disconnected()
