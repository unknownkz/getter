# getter < https://t.me/kastaid >
# Copyright (C) 2022 - kastaid
# All rights reserved.
#
# This file is a part of < https://github.com/kastaid/getter/ >
# PLease read the GNU Affero General Public License in;
# < https://www.github.com/kastaid/getter/blob/main/LICENSE/ >
# ================================================================

from asyncio import sleep
from . import (
    HELP,
    __version__,
    display_name,
    hl,
    kasta_cmd,
)


@kasta_cmd(disable_errors=True, pattern="help(?: |$)(.*)")
async def _(e):
    args = e.pattern_match.group(1).lower()
    Kst = await e.eor("`Loading...`")
    me = await e.client.get_me()
    if args:
        if args in HELP:
            await Kst.edit(
                f"📦 Plugin **{HELP[args][0]}** `{hl}help {args}`\n\n" + str(HELP[args][1]).replace("{i}", hl)
            )
        else:
            await Kst.edit(f"⛔ Plugin [`{args}`] not found! Type `{hl}help` to see the correct plugins name.")
    else:
        plugins = ""
        for p in HELP:
            plugins += f"<code>{str(p)}</code>  |  "
        plugins = plugins[:-3]
        text = f"""👤 <b>Owner</b>: <code>{display_name(me)} ({me.id})</code>
🤖 <b>Version</b>: <code>v{__version__}</code>
📦 <b>Plugins</b>: <code>{len(HELP)}</code>
📚 <b>Usage</b>: <code>{hl}help &lt;plugin name&gt;</code>

<b>All plugins and their commands:</b>
{plugins}

~ @kastaid"""
        await sleep(1)
        await Kst.try_delete()
        help = await e.client.send_message(
            e.chat_id,
            text,
            link_preview=False,
            parse_mode="html",
        )
        await help.reply(f"**Example**: Type `{hl}help devs` for usage.")
