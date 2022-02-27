# getter < https://t.me/kastaid >
# Copyright (C) 2022 - kastaid
# All rights reserved.
#
# This file is a part of < https://github.com/kastaid/getter/ >
# PLease read the GNU Affero General Public License in;
# < https://www.github.com/kastaid/getter/blob/main/LICENSE/ >
# ================================================================

import sys
from telethon import TelegramClient
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from telethon.sessions import StringSession
from .config import Var
from .logger import LOGS

session = ""
if Var.STRING_SESSION:
    if len(Var.STRING_SESSION.strip()) != 353:
        LOGS.error("STRING_SESSION wrong. Copy paste correctly! Quitting...")
        sys.exit(1)
    session = StringSession(str(Var.STRING_SESSION))
else:
    LOGS.error("STRING_SESSION empty. Please filling! Quitting...")
    sys.exit(1)

try:
    App = TelegramClient(
        session=session,
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        loop=None,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )
    App.parse_mode = "markdown"
except Exception as e:
    LOGS.exception("[APP] - {}".format(e))
    sys.exit(1)
