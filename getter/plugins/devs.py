# getter < https://t.me/kastaid >
# Copyright (C) 2022 - kastaid
# All rights reserved.
#
# This file is a part of < https://github.com/kastaid/getter/ >
# PLease read the GNU Affero General Public License in;
# < https://www.github.com/kastaid/getter/blob/main/LICENSE/ >
# ================================================================

import sys
from asyncio import sleep
from contextlib import suppress
from io import BytesIO
from os import execl, name, system
from secrets import choice
from time import time
from heroku3 import from_key
from telethon import functions
from . import (
    StartTime,
    Root,
    Var,
    DEVS,
    HELP,
    hl,
    kasta_cmd,
    parse_pre,
    time_formatter,
)


async def heroku_logs(m):
    if not (Var.HEROKU_API and Var.HEROKU_APP_NAME):
        await m.edit("Please set `HEROKU_APP_NAME` and `HEROKU_API` Config Vars.")
        return
    try:
        app = (from_key(Var.HEROKU_API)).app(Var.HEROKU_APP_NAME)
    except BaseException:
        await m.edit("`HEROKU_API` and `HEROKU_APP_NAME` is wrong! Kindly re-check in Config Vars.")
        return
    await m.edit("`Downloading Logs...`")
    res = app.get_log()
    with open("app-heroku.log", "w") as f:
        f.write(res)
    await m.client.send_file(
        m.chat_id,
        file="app-heroku.log",
        caption="Heroku Logs",
        force_document=True,
        allow_cache=False,
    )
    (Root / "app-heroku.log").unlink(missing_ok=True)
    await m.try_delete()


@kasta_cmd(pattern="dea(c|k)$")
async def _(e):
    Kst = "[Delete Telegram Account](https://telegram.org/deactivate)"
    await e.eor(Kst)


@kasta_cmd(pattern="dc$")
async def _(e):
    result = await e.client(functions.help.GetNearestDcRequest())
    await e.eor(
        f"**Country:** `{result.country}`\n"
        f"**Nearest Datacenter:** `{result.nearest_dc}`\n"
        f"**This Datacenter:** `{result.this_dc}`"
    )


@kasta_cmd(disable_errors=True, pattern="ping|([pP]ing)$")
async def _(e):
    if hasattr(e, "text") and e.text.lower() not in [f"{hl}ping", "ping"]:
        return
    start = time()
    Kst = await e.eor("Ping !")
    end = round((time() - start) * 1000)
    uptime = time_formatter((time() - StartTime) * 1000)
    await Kst.edit(
        f"🏓 Pong !!\n<b>Speed</b> - <code>{end}ms</code>\n<b>Uptime</b> - <code>{uptime}</code>",
        parse_mode="html",
    )


@kasta_cmd(disable_errors=True, pattern="logs?(?: |$)(.*)")
@kasta_cmd(disable_errors=True, own=True, senders=DEVS, pattern="glogs?(?: |$)(.*)")
async def _(e):
    is_devs = True if not (hasattr(e, "out") and e.out) else False
    with suppress(BaseException):
        opt = e.pattern_match.group(1)
        Kst = await e.eor("`Getting...`", silent=True)
        if is_devs:
            await sleep(choice((4, 5, 6)))
        if opt in ["heroku", "hk", "h"]:
            await heroku_logs(Kst)
        else:
            await Kst.reply("Terminal Logs", file="app.log", silent=True)
            await Kst.try_delete()


@kasta_cmd(pattern="restart$")
async def _(e):
    with suppress(BaseException):
        Kst = await e.eor("`Restarting...`")
        if name == "posix":
            _ = system("clear")
        await sleep(1)
        await Kst.edit("`Restarting your app, please wait for a minute!`")
        if not (Var.HEROKU_API and Var.HEROKU_APP_NAME):
            execl(sys.executable, sys.executable, *sys.argv)
            sys.exit()
            return
        try:
            Heroku = from_key(Var.HEROKU_API)
            app = Heroku.apps()[Var.HEROKU_APP_NAME]
            app.restart()
        except BaseException:
            await Kst.edit("`HEROKU_API` or `HEROKU_APP_NAME` is wrong! Kindly re-check in Config Vars.")


@kasta_cmd(disable_errors=True, pattern="json$")
async def _(e):
    with suppress(BaseException):
        chat_id = e.chat_id or e.from_id
        Kst = (await e.get_reply_message()).stringify() if e.reply_to_msg_id else e.stringify()
        reply_to = e.reply_to_msg_id if e.reply_to_msg_id else e.id
        if len(Kst) > 4096:
            with BytesIO(str.encode(Kst)) as file:
                file.name = "json_output.txt"
                await e.client.send_file(
                    chat_id,
                    file=file,
                    force_document=True,
                    allow_cache=False,
                    reply_to=reply_to,
                )
            await e.try_delete()
        else:
            await e.edit(Kst, parse_mode=parse_pre)


HELP.update(
    {
        "devs": [
            "Devs",
            """❯ `{i}deak|{i}deac`
Give a link Deactivated Account.

❯ `{i}dc`
Finds the nearest datacenter from your server.

❯ `{i}ping|ping|Ping`
Check response time.

❯ `{i}logs`
Get the full terminal logs.

❯ `{i}logs <heroku|hk|h>`
Get the latest 100 lines of heroku logs.

❯ `{i}restart`
Restart the app.

❯ `{i}json <reply>`
Get the json encoding of the message.
""",
        ]
    }
)
