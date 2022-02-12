# getter < https://t.me/kastaid >
# Copyright (C) 2022 - kastaid
# All rights reserved.
#
# This file is a part of < https://github.com/kastaid/getter/ >
# PLease read the GNU Affero General Public License in;
# < https://www.github.com/kastaid/getter/blob/main/LICENSE/ >
# ================================================================

from os import getenv
from zoneinfo import ZoneInfo
from dotenv import find_dotenv, load_dotenv
from .logger import LOGS

load_dotenv(find_dotenv("config.env"))


def tobool(val):
    """Convert a string representation of truth to true (1) or false (0).
    https://github.com/python/cpython/blob/main/Lib/distutils/util.py
    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return 1
    elif val in ("n", "no", "f", "false", "off", "0"):
        return 0
    else:
        raise ValueError("invalid truth value %r" % (val,))


class Var:
    DEV_MODE = tobool(getenv("DEV_MODE", "False"))
    STRING_SESSION = getenv("STRING_SESSION" "")
    API_ID = int(getenv("API_ID", "0"))
    API_HASH = getenv("API_HASH", "")
    HANDLER = getenv("HANDLER", ".")
    TZ = getenv("TZ", "Asia/Jakarta")
    HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", None)
    HEROKU_API = getenv("HEROKU_API", None)


TZ = ZoneInfo(Var.TZ)  # python 3.9
if not (
    Var.HANDLER.startswith(
        (
            "/",
            ".",
            "!",
            "+",
            "-",
            "_",
            ";",
            "$",
            ",",
            "~",
            "^",
            "%",
            "&",
        )
    )
):
    LOGS.warning("Your HANDLER [{}] is not supported yet, set default as dot [.command]".format(Var.HANDLER))
    HANDLER = "."
else:
    HANDLER = Var.HANDLER