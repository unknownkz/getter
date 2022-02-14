#!/usr/bin/env python3
# getter < https://t.me/kastaid >
# Copyright (C) 2022 - kastaid
# All rights reserved.
#
# This file is a part of < https://github.com/kastaid/getter/ >
# PLease read the GNU Affero General Public License in;
# < https://www.github.com/kastaid/getter/blob/main/LICENSE/ >
# ================================================================

from subprocess import check_call
from sys import exit, executable

try:
    import telethon as tl
except (ImportError, ModuleNotFoundError):
    print("Installing Telethon...")
    # python3 -m pip install --no-cache-dir Telethon==1.24.0
    check_call([executable, "-m", "pip", "install", "--no-cache-dir", "Telethon==1.24.0"])
finally:
    import telethon as tl


print("Get your API ID and API HASH from my.telegram.org or @ScrapperRoBot to proceed.\n\n")

try:
    API_ID = int(input("Please enter your API ID: "))
except ValueError:
    print("APP ID must be an integer.\nQuitting...")
    exit(0)
API_HASH = input("Please enter your API HASH: ")

client = tl.TelegramClient(tl.sessions.StringSession(), api_id=API_ID, api_hash=API_HASH)


async def main() -> None:
    try:
        print("Generating STRING_SESSION...")
        string_session = client.session.save()
        print("\n" + string_session + "\n")
        await client.send_message(
            "me",
            f"""
**This Is Your Telethon UserBot** `STRING_SESSION`
⚠️ **DO NOT SHARE WITH ANYONE** ⚠️

```{string_session}```

Generated by @kastaid""",
        )
        print("Generated !! Check your Telegram Saved Messages to copy STRING_SESSION or copy from above.")
        exit(0)
    except tl.errors.ApiIdInvalidError:
        print("Your API ID/API HASH combination is invalid. Kindly recheck.\nQuitting...")
        exit(0)
    except ValueError:
        print("API HASH must not be empty!\nQuitting...")
        exit(0)
    except tl.errors.PhoneNumberInvalidError:
        print("The phone number is invalid!\nQuitting...")
        exit(0)


with client:
    client.loop.run_until_complete(main())
