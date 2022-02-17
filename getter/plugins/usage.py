# getter < https://t.me/kastaid >
# Copyright (C) 2022 - kastaid
# All rights reserved.
#
# This file is a part of < https://github.com/kastaid/getter/ >
# PLease read the GNU Affero General Public License in;
# < https://www.github.com/kastaid/getter/blob/main/LICENSE/ >
# ================================================================

import shutil as shu
from contextlib import suppress
from datetime import datetime
from math import floor
from secrets import choice
from time import time
import psutil as psu
from heroku3 import from_key
from requests import get
from . import (
    HELP,
    StartTime,
    Var,
    humanbytes,
    kasta_cmd,
    time_formatter,
)

usage = """
**🖥️ Uptime 🖥️**
**App**: `{}`
**System**: `{}`

**⚙️ Dyno Usage ⚙️**
-> **Dyno usage for** `{}`:
  •  **{}h**  **{}m |** `[{}%]`
-> **Dyno hours quota remaining this month**:
  •  **{}h**  **{}m |** `[{}%]`

**💾 Disk Space 💾**
**Total**: `{}`
**Used**: `{}`
**Free**: `{}`

**📊 Data Usage 📊**
**Upload**: `{}`
**Download**: `{}`

**📈 Memory Usage 📈**
**CPU**: `{}`
**RAM**: `{}`
**DISK**: `{}`
"""

usage_simple = """
**🖥️ Uptime 🖥️**
**App**: `{}`
**System**: `{}`

**💾 Disk Space 💾**
**Total**: `{}`
**Used**: `{}`
**Free**: `{}`

**📊 Data Usage 📊**
**Upload**: `{}`
**Download**: `{}`

**📈 Memory Usage 📈**
**CPU**: `{}`
**RAM**: `{}`
**DISK**: `{}`
"""

some_random_headers = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/72.0.3626.121 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) "
    "Chrome/19.0.1084.46 Safari/536.5",
    "Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) " "Chrome/19.0.1084.46 Safari/536.5",
    "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0",
]

HEROKU_API = None
HEROKU_APP_NAME = None
heroku_api, app_name = Var.HEROKU_API, Var.HEROKU_APP_NAME
try:
    if heroku_api and app_name:
        HEROKU_API = heroku_api
        HEROKU_APP_NAME = app_name
        Heroku = from_key(heroku_api)
        app = Heroku.app(app_name)
except BaseException:
    HEROKU_API = None
    HEROKU_APP_NAME = None


@kasta_cmd(pattern="usage(?: |$)(.*)")
async def _(e):
    with suppress(BaseException):
        Kst = await e.eor("`Processing...`")
        try:
            opt = e.text.split(" ", maxsplit=1)[1]
        except IndexError:
            return await Kst.edit(simple_usage())
        if opt in ["heroku", "h"]:
            is_hk, hk = heroku_usage()
            await Kst.edit(hk)
        else:
            await Kst.edit(simple_usage())


def simple_usage():
    app_uptime = time_formatter((time() - StartTime) * 1000)
    system_uptime = datetime.fromtimestamp(psu.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    total, used, free = shu.disk_usage(".")
    cpu_freq = psu.cpu_freq().current
    if cpu_freq >= 1000:
        cpu_freq = "{}GHz".format(round(cpu_freq / 1000, 2))
    else:
        cpu_freq = "{}MHz".format(round(cpu_freq, 2))
    CPU = "{}% ({}) {}".format(psu.cpu_percent(interval=0.5), psu.cpu_count(), cpu_freq)
    RAM = "{}%".format(psu.virtual_memory().percent)
    DISK = "{}%".format(psu.disk_usage("/").percent)
    UPLOAD = humanbytes(psu.net_io_counters().bytes_sent)
    DOWN = humanbytes(psu.net_io_counters().bytes_recv)
    TOTAL = humanbytes(total)
    USED = humanbytes(used)
    FREE = humanbytes(free)
    return usage_simple.format(
        app_uptime,
        system_uptime,
        TOTAL,
        USED,
        FREE,
        UPLOAD,
        DOWN,
        CPU,
        RAM,
        DISK,
    )


def heroku_usage():
    if HEROKU_API is None and HEROKU_APP_NAME is None:
        return False, "Please set `HEROKU_APP_NAME` and `HEROKU_API` in Config Vars."
    user_id = Heroku.account().id
    headers = {
        "User-Agent": choice(some_random_headers),
        "Authorization": f"Bearer {heroku_api}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    her_url = f"https://api.heroku.com/accounts/{user_id}/actions/get-quota"
    r = get(her_url, headers=headers)
    if r.status_code != 200:
        return (
            True,
            f"**ERROR**\n`{r.reason}`",
        )
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]
    remaining_quota = quota - quota_used
    percentage = floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = floor(minutes_remaining / 60)
    minutes = floor(minutes_remaining % 60)
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = floor(App[0]["quota_used"] * 100 / quota)
    AppHours = floor(AppQuotaUsed / 60)
    AppMinutes = floor(AppQuotaUsed % 60)
    app_uptime = time_formatter((time() - StartTime) * 1000)
    system_uptime = datetime.fromtimestamp(psu.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    total, used, free = shu.disk_usage(".")
    cpu_freq = psu.cpu_freq().current
    if cpu_freq >= 1000:
        cpu_freq = "{}GHz".format(round(cpu_freq / 1000, 2))
    else:
        cpu_freq = "{}MHz".format(round(cpu_freq, 2))
    CPU = "{}% ({}) {}".format(psu.cpu_percent(interval=0.5), psu.cpu_count(), cpu_freq)
    RAM = "{}%".format(psu.virtual_memory().percent)
    DISK = "{}%".format(psu.disk_usage("/").percent)
    UPLOAD = humanbytes(psu.net_io_counters().bytes_sent)
    DOWN = humanbytes(psu.net_io_counters().bytes_recv)
    TOTAL = humanbytes(total)
    USED = humanbytes(used)
    FREE = humanbytes(free)
    return True, usage.format(
        app_uptime,
        system_uptime,
        Var.HEROKU_APP_NAME,
        AppHours,
        AppMinutes,
        AppPercentage,
        hours,
        minutes,
        percentage,
        TOTAL,
        USED,
        FREE,
        UPLOAD,
        DOWN,
        CPU,
        RAM,
        DISK,
    )


HELP.update(
    {
        "usage": [
            "Usage",
            """• `{i}usage`
↳ : Get overall usage.

• `{i}usage <heroku|h>`
↳ : Get heroku stats.
""",
        ]
    }
)
