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
from gpytranslate import Translator
from telethon.errors import YouBlockedUserError
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.types import Chat
from . import (
    HELP,
    display_name,
    get_user,
    hl,
    kasta_cmd,
)


@kasta_cmd(disable_errors=True, pattern="del|(d|D|del|Del)")
async def _(e):
    if hasattr(e, "text") and e.text.lower() not in [f"{hl}del", "d", "del"]:
        return
    await e.try_delete()
    reply = await e.get_reply_message()
    if reply:
        await reply.try_delete()


@kasta_cmd(disable_errors=True, pattern="purge(?: |$)(.*)")
async def _(e):
    match = e.pattern_match.group(1)
    if not e.is_reply:
        return await e.try_delete()
    if match or e.is_private or isinstance(e.chat, Chat):
        count = 0
        try:
            num = int(match)
        except BaseException:
            num = None
        async for m in e.client.iter_messages(
            e.chat_id,
            limit=num,
            min_id=e.reply_to_msg_id if e.reply_to_msg_id else None,
        ):
            await m.try_delete()
            count += 1
            await sleep(0.5)
        await e.eor(f"`Purged {count}`", time=2)
        return
    with suppress(BaseException):
        msgs = [x for x in range(e.reply_to_msg_id, e.id + 1)]  # noqa: C416
        await e.client.delete_messages(e.chat_id, msgs)
    Kst = await e.client.send_message(e.chat_id, "`purged`")
    await sleep(2)
    await Kst.try_delete()


@kasta_cmd(disable_errors=True, pattern="purgeme(?: |$)(.*)")
async def _(e):
    match = e.pattern_match.group(1)
    count = 0
    if match and not e.is_reply:
        try:
            num = int(match)
        except BaseException:
            num = None
        async for m in e.client.iter_messages(e.chat_id, limit=num, from_user="me"):
            await m.try_delete()
            count += 1
        await e.eor(f"`Purged {count}`", time=2)
        return
    if not (match or e.is_reply):
        await e.eor(f"Reply to a message to purge from or use it like `{hl}purgeme <num>`", time=10)
        return
    chat = await e.get_input_chat()
    msgs = []
    async for m in e.client.iter_messages(
        chat,
        from_user="me",
        min_id=e.reply_to_msg_id if e.reply_to_msg_id else None,
    ):
        msgs.append(m)
        count += 1
        msgs.append(e.reply_to_msg_id)
        if len(msgs) == 100:
            await e.client.delete_messages(chat, msgs)
            msgs = []
    if msgs:
        await e.client.delete_messages(chat, msgs)
    await e.eor(f"`Purged {count}`", time=2)


@kasta_cmd(disable_errors=True, pattern="ids?")
async def _(e):
    chat_id = e.chat_id or e.from_id
    if e.reply_to_msg_id:
        reply = await e.get_reply_message()
        userid = reply.sender_id
        text = f"**User ID:** `{userid}`" if e.is_private else f"**Chat ID:** `{chat_id}`\n**User ID:** `{userid}`"
        text = text + f"\n**Message ID:** `{reply.id}`"
        await e.eor(text)
        return
    text = "**User ID:** " if e.is_private else "**Chat ID:** "
    text = f"{text}`{chat_id}`" + f"\n**Message ID:** `{e.id}`"
    await e.eor(text)


@kasta_cmd(disable_errors=True, pattern="total(?: |$)(.*)")
async def _(e):
    match = e.pattern_match.group(1)
    if match:
        user = match
    elif e.is_reply:
        user = (await e.get_reply_message()).sender_id
    else:
        user = "me"
    msg = await e.client.get_messages(e.chat_id, 0, from_user=user)
    user = await e.client.get_entity(user)
    await e.eor(f"Total messages from `{display_name(user)}` [`{msg.total}`]")


@kasta_cmd(disable_errors=True, pattern="(delayspam|ds)(?: |$)(.*)")
async def _(e):
    try:
        args = e.text.split(" ", 3)
        delay = float(args[1])
        count = int(args[2])
        msg = str(args[3])
    except BaseException:
        return await e.eor(f"**Usage:** `{hl}delayspam <time> <count> <text>`", time=10)
    await e.try_delete()
    try:
        delay = 5 if delay and int(delay) < 5 else delay
        for _ in range(count):
            await e.respond(msg)
            await sleep(delay)
    except Exception as err:
        await e.respond(f"**Error:** `{err}`")


@kasta_cmd(func=lambda x: not x.is_private, pattern="kickme$")
async def _(e):
    with suppress(BaseException):
        await e.try_delete()
        await e.client(LeaveChannelRequest(e.chat_id))


@kasta_cmd(disable_errors=True, pattern="tr")
async def _(e):
    if len(e.text) > 3 and e.text[3] != " ":
        await e.try_delete()
        return
    input = e.text[4:6]
    txt = e.text[7:]
    Kst = await e.eor("`Translate...`")
    if txt:
        text = txt
        lang = input or "id"
    elif e.is_reply:
        prev_msg = await e.get_reply_message()
        text = prev_msg.message
        lang = input or "id"
    else:
        await Kst.eor(f"`{hl}tr <lang code>` reply a message.", time=15)
        return
    try:
        translator = Translator()
        translated = await translator(text.strip(), targetlang=lang)
        after_tr_text = translated.text
        source_lang = await translator.detect(translated.orig)
        transl_lang = await translator.detect(translated.text)
        output_str = "Detected: **{}**\nTranslated: **{}**\n\n```{}```".format(
            source_lang,
            transl_lang,
            after_tr_text,
        )
        await Kst.edit(output_str)
    except Exception as e:
        await Kst.edit(str(e))


@kasta_cmd(disable_errors=True, pattern="(sa|sg)(?: |$)(.*)")
async def _(e):
    Kst = await e.eor("`Getting...`")
    chat_id = e.chat_id or e.from_id
    user, _ = await get_user(e, 2)
    if not user:
        await Kst.eor("`Failed, required Username/ID or reply message.`", time=15)
        return
    sangmata = "@SangMataInfo_bot"
    try:
        async with e.client.conversation(sangmata) as conv:
            try:
                rets = await conv.send_message(f"/search_id {user.id}")
                r = await conv.get_response()
                resp = await conv.get_response()
            except YouBlockedUserError:
                await Kst.eor("`Try again now...!`", time=15)
                await e.client(UnblockRequest(sangmata))
                return
            if r.text.startswith("Name"):
                respd = await conv.get_response()
                if len(r.message) > 4096:
                    with suppress(BaseException):
                        with BytesIO(str.encode(r.message)) as file:
                            file.name = "sangmata.txt"
                            await e.client.send_file(
                                chat_id,
                                file=file,
                                force_document=True,
                                allow_cache=False,
                                reply_to=e.id,
                            )
                    await Kst.try_delete()
                else:
                    await Kst.edit(f"`{r.message}`")
                await e.client.delete_messages(conv.chat_id, [rets.id, r.id, resp.id, respd.id])
                return
            if resp.text.startswith("No records") or r.text.startswith("No records"):
                await Kst.eor("__No records found.__", time=10)
                await e.client.delete_messages(conv.chat_id, [rets.id, r.id, resp.id])
                return
            else:
                respd = await conv.get_response()
                if len(resp.message) > 4096:
                    with suppress(BaseException):
                        with BytesIO(str.encode(resp.message)) as file:
                            file.name = "sangmata.txt"
                            await e.client.send_file(
                                chat_id,
                                file=file,
                                force_document=True,
                                allow_cache=False,
                                reply_to=e.id,
                            )
                    await Kst.try_delete()
                else:
                    await Kst.edit(f"```{resp.message}```")
            await e.client.delete_messages(conv.chat_id, [rets.id, r.id, resp.id, respd.id])
    except TimeoutError:
        return await Kst.eor("__Not responding, try again later!__", time=15)


HELP.update(
    {
        "chats": [
            "Chats",
            """• `{i}del|d|D|del|Del`
↳ : Delete a messages.

• `{i}purge <limit (optional)> <reply to message>`
↳ : Purge all messages from the replied message.

• `{i}purgeme <reply to message>`
↳ : Purge Only your messages from the replied message.

• `{i}id|{i}ids`
↳ : Get current Chat/User/Message ID.

• `{i}total <username/reply>`
↳ : Get total user messages.

• `{i}tr <lang code> <reply to message>`
↳ : Translate a replied messages.

• `{i}sa|{i}sg <reply/username/id>`
↳ : Get history of names and usernames by sangmata.

• `{i}delayspam|{i}ds <time> <count> <text>`
↳ : Spam chat with delays in seconds (min 5 seconds).

• `{i}kickme`
↳ : Leaves the groups.
""",
        ]
    }
)
