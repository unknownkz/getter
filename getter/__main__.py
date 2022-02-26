# getter < https://t.me/kastaid >
# Copyright (C) 2022 - kastaid
# All rights reserved.
#
# This file is a part of < https://github.com/kastaid/getter/ >
# PLease read the GNU Affero General Public License in;
# < https://www.github.com/kastaid/getter/blob/main/LICENSE/ >
# ================================================================

import asyncio
import signal
from base64 import b64decode
from contextlib import suppress
from importlib import import_module
from random import randrange
from sys import exit
from time import time
from telethon.errors import ApiIdInvalidError, AuthKeyDuplicatedError, PhoneNumberInvalidError
from telethon.tl.functions.channels import JoinChannelRequest
from getter import StartTime, __version__, LOOP
from .app import App
from .config import Var
from .logger import LOGS
from .plugins import ALL_PLUGINS
from .utils import time_formatter

success_msg = ">> Visit @kastaid for updates !!"

for signame in {"SIGINT", "SIGTERM", "SIGABRT"}:
    sig = getattr(signal, signame)
    LOOP.add_signal_handler(sig, lambda s=sig: asyncio.create_task(shutdown(s.name)))


async def shutdown(signum: str) -> None:
    LOGS.warning("Stop signal received : {}".format(signum))
    with suppress(BaseException):
        await App.disconnect()
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    LOGS.warning("Cancelling outstanding tasks : {}".format(len(tasks)))
    await asyncio.gather(*tasks, return_exceptions=True)
    await LOOP.shutdown_asyncgens()
    LOOP.stop()


async def autous() -> None:
    with suppress(BaseException):
        if not Var.DEV_MODE:
            for _ in ["QGthc3RhaWQ=", "QGthc3Rhb3Q=", "QGthc3RhdXA="]:
                _ = b64decode(_).decode("utf-8")
                await asyncio.sleep(randrange(2, 4))
                await App(JoinChannelRequest(_))


async def launching() -> None:
    try:
        await asyncio.sleep(randrange(5, 8))
        await App.start()
        await asyncio.sleep(2)
        App.me = await App.get_me()
        App.uid = App.me.id
        await autous()
    except ApiIdInvalidError:
        LOGS.error("API_ID and API_HASH combination does not match, please re-check! Quitting...")
        exit(1)
    except (AuthKeyDuplicatedError, PhoneNumberInvalidError, EOFError):
        LOGS.error("STRING_SESSION expired, please create new! Quitting...")
        exit(1)
    except Exception as e:
        LOGS.exception("[LAUNCHING] - {}".format(e))
        exit(1)


async def main() -> None:
    LOGS.info(">> Launching...")
    await launching()
    LOGS.info(">> Load Plugins...")
    start = time()
    plugins = ALL_PLUGINS
    [import_module("getter.plugins." + p) for p in plugins]
    loaded_plugins = time_formatter((time() - start) * 1000)
    LOGS.warning(">> Loaded Plugins {} (took {}) : {}".format(len(plugins), loaded_plugins, str(plugins)))
    await asyncio.sleep(randrange(2, 4))
    launch_time = time_formatter((time() - StartTime) * 1000)
    launch_msg = ">> 🚀 v{} Launch {} in {}".format(__version__, App.uid, launch_time)
    LOGS.info(launch_msg)
    await asyncio.sleep(2)
    LOGS.info(success_msg)
    await asyncio.sleep(2)
    await App.run_until_disconnected()


if __name__ == "__main__":
    try:
        LOOP.run_until_complete(main())
    except (
        NotImplementedError,
        KeyboardInterrupt,
        SystemExit,
        RuntimeError,
        ConnectionError,
        RecursionError,
        asyncio.CancelledError,
    ):
        pass
    except (ModuleNotFoundError, ImportError) as e:
        LOGS.exception("[MAIN_MODULE_IMPORT] : {}".format(e))
        exit(1)
    except Exception as e:
        LOGS.exception("[MAIN_ERROR] : {}".format(e))
    finally:
        LOGS.info("[MAIN] - App Stopped...")
        exit(0)
