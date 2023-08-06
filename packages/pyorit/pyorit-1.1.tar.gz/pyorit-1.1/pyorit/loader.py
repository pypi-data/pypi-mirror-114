# OrangIT - UserBot
# Copyright (C) 2021 OrangIT
#
# This file is a part of < https://github.com/Projectgeez/OrangIT/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/OrangIT/OrangIT/blob/main/LICENSE/>.

import os

from . import LOGS
from .utils import (
    load_addons,
    load_assistant,
    load_manager,
    load_plugins,
    load_pmbot,
    load_vc,
)


def plugin_loader(addons=None, pmbot=None, manager=None, vcbot=None):
    # for userbot
    files = sorted(os.listdir("plugins"))
    for plugin_name in files:
        try:
            if plugin_name.endswith(".py"):
                load_plugins(plugin_name[:-3])
                LOGS.info(f"OrangIT - Official -  Terinstal - {plugin_name}")
        except Exception as exc:
            LOGS.info(f"OrangIT - Official - ERROR - {plugin_name}")
            LOGS.info(str(type(exc)) + ": " + str(exc))
    LOGS.info("-" * 70)

    # for assistant
    files = sorted(os.listdir("assistant"))
    for plugin_name in files:
        try:
            if plugin_name.endswith(".py"):
                load_assistant(plugin_name[:-3])
                LOGS.info(f"OrangIT - Assistant -  Terinstal - {plugin_name}")
        except Exception as exc:
            LOGS.info(f"OrangIT - Assistant - ERROR - {plugin_name}")
            LOGS.info(str(type(exc)) + ": " + str(exc))
    LOGS.info("-" * 70)

    # for addons
    if addons == "True" or not addons:
        try:
            os.system(
                "git clone https://github.com/ProjectGeez/OrangITModule.git addons/"
            )
        except BaseException:
            pass
        """
        LOGS.info("Installing packages for addons")
        os.system("pip install -r addons/addons.txt")
        """
        files = sorted(os.listdir("addons"))
        for plugin_name in files:
            try:
                if plugin_name.endswith(".py"):
                    load_addons(plugin_name[:-3])
                    LOGS.info(f"OrangIT - Addons -  Terinstal - {plugin_name}")
            except Exception as exc:
                LOGS.info(f"OrangIT - Addons - ERROR - {plugin_name}")
                LOGS.info(str(type(exc)) + ": " + str(exc))
        LOGS.info("-" * 70)
    else:
        pass
        # os.system("cp plugins/__init__.py addons/")

    # group manager
    if manager == "True":
        files = sorted(os.listdir("assistant/manager"))
        for plugin_name in files:
            if plugin_name.endswith(".py"):
                load_manager(plugin_name[:-3])
                LOGS.info(f"OrangIT - Grup Manajer - Terinstal - {plugin_name}.")
        LOGS.info("-" * 70)

    # chat via assistant
    if pmbot == "True":
        files = sorted(os.listdir("assistant/pmbot"))
        for plugin_name in files:
            if plugin_name.endswith(".py"):
                load_pmbot(plugin_name[:-3])
        LOGS.info(f"OrangIT - Penerusan Pesan Bot PM - Diaktifkan.")
        LOGS.info("-" * 70)

    # vc bot
    if vcbot:
        files = sorted(os.listdir("vcbot"))
        for plugin_name in files:
            if plugin_name.endswith(".py"):
                load_vc(plugin_name[:-3])
            if not plugin_name.startswith("_"):
                LOGS.info(f"OrangIT - VC Bot - Terinstal - {plugin_name}.")
        LOGS.info("-" * 70)
