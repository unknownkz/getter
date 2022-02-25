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
from telethon import version
from . import (
    HELP,
    __version__,
    display_name,
    hl,
    kasta_cmd,
    Var,
)


@kasta_cmd(disable_errors=True, pattern="help(?: |$)(.*)")
async def _(e):
    args = e.pattern_match.group(1).lower()
    Kst = await e.eor("`Loading...`")
    if args:
        if args in HELP:
            await Kst.edit(
                f"📦 Plugin **{HELP[args][0]}** `{hl}help {args}`\n\n" + str(HELP[args][1]).replace("{i}", hl)
            )
        else:
            await Kst.edit(f"⛔ Plugin [`{args}`] not found! Type `{hl}help` correct plugins name.")
    else:
        plugins = ""
        for p in HELP:
            plugins += f"<code>{str(p)}</code>  |  "
        plugins = plugins[:-3]
        me = await e.client.get_me()
        text = f"""👤 <b>Owner:</b> <code>{display_name(me)} ({me.id})</code>
⚙️ <b>Heroku App Name:</b> <code>{Var.HEROKU_APP_NAME}</code>
🤖 <b>Getter Version:</b> <code>v{__version__}</code>
🐍 <b>Python Version:</b> <code>v{python_version()}</code>
📦 <b>Telethon Version:</b> <code>v{version.__version__}</code>
🔌 <b>Plugins:</b> <code>{len(HELP)}</code>
📚 <b>Usage:</b> <code>{hl}help &lt;plugin name&gt;</code>

<b>All plugins and their commands:</b>
{plugins}

<b>Example:</b> Type <code>{hl}help chats</code> for usage.
"""
        await sleep(1)
        await Kst.edit(text, parse_mode="html")
