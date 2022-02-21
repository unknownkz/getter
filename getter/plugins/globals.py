# getter < https://t.me/kastaid >
# Copyright (C) 2022 - kastaid
# All rights reserved.
#
# This file is a part of < https://github.com/kastaid/getter/ >
# PLease read the GNU Affero General Public License in;
# < https://www.github.com/kastaid/getter/blob/main/LICENSE/ >
# ================================================================

from asyncio import sleep
from contextlib import suppress
from io import BytesIO
from random import randrange
from time import time
from telethon.errors import FloodWaitError
from . import (
    DEVS,
    HELP,
    eor,
    eod,
    kasta_cmd,
    time_formatter,
    NOSPAM_CHAT,
)


@kasta_cmd(pattern="g(admin|)cast(?: |$)(.*)")
@kasta_cmd(own=True, senders=DEVS, pattern="gg(admin|)cast(?: |$)(.*)")
async def _(e):
    is_admin = True if e.text and e.text[2:7] == "admin" or e.text[3:8] == "admin" else False
    match = e.pattern_match.group(2)
    if match:
        content = match
    elif e.is_reply:
        content = await e.get_reply_message()
    else:
        return await eod(e, "`Give some text to Gcast or reply a message.`")
    if is_admin:
        Kst = await eor(e, "📢 __Gcasting to groups as admin...__")
    else:
        Kst = await eor(e, "📢 __Gcasting to all groups...__")
    start_time = time()
    success = failed = 0
    errors = ""
    async for x in e.client.iter_dialogs():
        if x.is_group:
            chat = x.entity.id
            if int("-100" + str(chat)) not in NOSPAM_CHAT and (
                not is_admin or (x.entity.admin_rights or x.entity.creator)
            ):
                try:
                    await e.client.send_message(chat, content)
                    await sleep(randrange(2, 4))
                    success += 1
                except FloodWaitError as fw:
                    await sleep(fw.seconds + 10)
                    try:
                        await e.client.send_message(chat, content)
                        await sleep(randrange(2, 4))
                        success += 1
                    except Exception as err:
                        errors += f"• {err}\n"
                        failed += 1
                except Exception as err:
                    errors += "• " + str(err) + "\n"
                    failed += 1
    taken = time_formatter((time() - start_time) * 1000)
    if is_admin:
        text = r"\\**#Gcast**// in `{}` to `{}` groups as admin, failed `{}` groups.".format(
            taken,
            success,
            failed,
        )
    else:
        text = r"\\**#Gcast**// in `{}` to `{}` groups, failed `{}` groups.".format(
            taken,
            success,
            failed,
        )
    with suppress(BaseException):
        if errors != "":
            with BytesIO(str.encode(errors)) as file:
                file.name = "gcast-error.log"
                await e.client.send_file(
                    e.chat_id or e.from_id,
                    errors,
                    caption="Gcast Error Logs",
                    force_document=True,
                    allow_cache=False,
                )
    await Kst.edit(text)


HELP.update(
    {
        "globals": [
            "Globals",
            """• `{i}gcast <text/reply>`
↳ : Send broadcast messages to all groups.

• `{i}gadmincast <text/reply>`
↳ : Same as above, but only in your admin groups.

**DWYOR ~ Do With Your Own Risk!**
""",
        ]
    }
)
