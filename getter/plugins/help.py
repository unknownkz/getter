# getter < https://t.me/kastaid >
# Copyright (C) 2022 - kastaid
# All rights reserved.
#
# This file is a part of < https://github.com/kastaid/getter/ >
# PLease read the GNU Affero General Public License in;
# < https://www.github.com/kastaid/getter/blob/main/LICENSE/ >
# ================================================================

from asyncio import sleep
from platform import python_version
from time import time
from telethon import version
from . import (
    StartTime,
    __version__,
    HELP,
    display_name,
    hl,
    kasta_cmd,
    Var,
    time_formatter,
)

help_text = """
█▀▀ █▀▀ ▀█▀ ▀█▀ █▀▀ █▀█
█▄█ ██▄ ░█░ ░█░ ██▄ █▀▄

┏━━━━━━━━━━━━━━━━━━━━━━━━
┣  <b>User</b> - <code>{}</code>
┣  <b>ID</b> - <code>{}</code>
┣  <b>Heroku App Name</b> - <code>{}</code>
┣  <b>Getter Version</b> - <code>{}</code>
┣  <b>Python Version</b> - <code>{}</code>
┣  <b>Telethon Version</b> - <code>{}</code>
┣  <b>Uptime</b> - <code>{}</code>
┣  <b>Handler</b> - <code>{}</code>
┣  <b>Plugins</b> - <code>{}</code>
┣  <b>Usage</b> - <code>{}help &lt;plugin name&gt;</code>
┗━━━━━━━━━━━━━━━━━━━━━━━━

<b>~ All plugins and commands are below:</b>

{}

<b>Example:</b> Type <code>{}help core</code> for usage.
"""


@kasta_cmd(disable_errors=True, pattern="help(?: |$)(.*)")
async def _(e):
    args = e.pattern_match.group(1).lower()
    Kst = await e.eor("`Loading...`")
    if args:
        if args in HELP:
            _ = "📦 **Plugin {}** <`{}help {}`>\n\n{}".format(
                HELP[args][0],
                hl,
                args,
                HELP[args][1].replace("{i}", hl),
            )
            await Kst.edit(_)
        else:
            await Kst.edit(f"❌ **Invalid Plugin** ➞ `{args}`\nType ```{hl}help``` to see valid plugin names.")
    else:
        uptime = time_formatter((time() - StartTime) * 1000)
        plugins = ""
        for p in HELP:
            plugins += f"<code>{p.strip()}</code>  |  "
        plugins = plugins[:-3]
        me = await e.client.get_me()
        text = help_text.format(
            display_name(me),
            e.client.uid,
            Var.HEROKU_APP_NAME,
            __version__,
            python_version(),
            version.__version__,
            uptime,
            hl,
            len(HELP),
            hl,
            plugins,
            hl,
        )
        await sleep(1)
        await Kst.edit(text, parse_mode="html")
