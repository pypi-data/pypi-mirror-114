from .. import asst, udB, OrangIT_bot  # pylint ignore

CMD_HELP = {}


def sudoers():
    return udB["SUDOS"].split()


def should_allow_sudo():
    if udB["SUDO"] == "True":
        return True
    else:
        return False


def owner_and_sudos():
    return [str(OrangIT_bot.uid), *sudoers()]
