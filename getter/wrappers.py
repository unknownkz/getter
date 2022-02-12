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
from telethon.tl.custom import Message


async def eor(e, text=None, **args):
    time = args.get("time", None)
    edit_time = args.get("edit_time", None)
    force_reply = args.get("force_reply", False)
    if "time" in args:
        del args["time"]
    if "edit_time" in args:
        del args["edit_time"]
    if "force_reply" in args:
        del args["force_reply"]
    if "link_preview" not in args:
        args.update({"link_preview": False})
    with suppress(BaseException):
        if hasattr(e, "out") and e.out:
            if "silent" in args:
                del args["silent"]
            if edit_time:
                await sleep(edit_time)
            res = await e.edit(text, **args)
        else:
            if force_reply:
                args["reply_to"] = e.reply_to_msg_id or e
            else:
                args["reply_to"] = e.reply_to_msg_id or None
            res = await e.client.send_message(e.chat_id, text, **args)
        if time:
            await sleep(time)
            return await _try_delete(res)
        return res


async def eod(e, text=None, **kwargs):
    kwargs["time"] = kwargs.get("time", 8)
    return await eor(e, text, **kwargs)


async def eos(e, text=None, **args):
    edit = args.get("edit", False)
    force_reply = args.get("force_reply", False)
    if "edit" in args:
        del args["edit"]
    if "force_reply" in args:
        del args["force_reply"]
    if "link_preview" not in args:
        args.update({"link_preview": False})
    if "silent" not in args:
        args.update({"silent": True})
    with suppress(BaseException):
        if not edit:
            if force_reply:
                args["reply_to"] = e.reply_to_msg_id or e
            else:
                args["reply_to"] = e.reply_to_msg_id or None
            await _try_delete(e)
            await e.client.send_message(e.chat_id, text, **args)
        else:
            if "silent" in args:
                del args["silent"]
            await e.edit(text, **args)


async def _try_delete(e):
    with suppress(BaseException):
        return await e.delete()


setattr(Message, "eor", eor)  # noqa: B010
setattr(Message, "eos", eos)  # noqa: B010
setattr(Message, "try_delete", _try_delete)  # noqa: B010
