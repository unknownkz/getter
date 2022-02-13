# getter < https://t.me/kastaid >
# Copyright (C) 2022 - kastaid
# All rights reserved.
#
# This file is a part of < https://github.com/kastaid/getter/ >
# PLease read the GNU Affero General Public License in;
# < https://www.github.com/kastaid/getter/blob/main/LICENSE/ >
# ================================================================

from base64 import b64decode
from telethon import events
from getter import (
    HELP,
    Root,
    StartTime,
    __version__,
)
from getter.app import App
from getter.config import Var, TZ, HANDLER
from getter.decorators import kasta_cmd
from getter.logger import LOGS
from getter.utils import (
    display_name,
    get_user,
    get_username,
    humanbytes,
    is_telegram_link,
    runner,
    time_formatter,
)
from getter.wrappers import eod, eor, eos

hl = HANDLER
DEVS = list(map(int, b64decode("MjAwMzM2MTQxMCA1MDY4Mzc5NjY3IDUwNzUxMDE2MTA=").split()))  # v, e, t
NOSPAM_CHAT = [
    -1001387666944,  # @PyrogramChat
    -1001221450384,  # @pyrogramlounge
    -1001109500936,  # @TelethonChat
    -1001471736013,  # @TelegrafJSChat
    -1001185324811,  # @pytgcallschat
    -1001050982793,  # @Python
    -1001256902287,  # @DurovsChat
    -1001235155926,  # @RoseSupportChat
    -1001341570295,  # @tgbetachat
    -1001336679475,  # @tgandroidtests
    -1001120290128,  # @plusmsgrchat
    -1001311056733,  # @BotTalk
    -1001312712379,  # @SpamWatchSupport
    -1001360494801,  # @OFIOpenChat
    -1001435671639,  # @xfichat
    -1001421589523,  # @tdspya
    -1001052242766,  # @pythonID
    -1001294181499,  # @userbotindo
    -1001109837870,  # @TelegramBotIndonesia
    -1001327032795,  # @UltroidSupport
    -1001451324102,  # @Ultroidspam
    -1001481357570,  # @usergeot
    -1001465749479,  # @UserGeSpam
    -1001596433756,  # @MFIChat
    -1001180648994,  # @FSGOpenChat
    -1001699144606,  # @kastaoot
    -1001700971911,  # @GetterUpdater
    -1001776850404,  # @MetaUpdater
    -1001307868573,  # @caritemanok
    -1001261461928,  # @temanrandomchatt
    -1001459701099,  # @CatUserbotSupport
    -1001062690377,  # @SohbetDoge
    -1001473548283,  # @SharingUserbot
    -1001209432070,  # @GeezSupportGroup
    -1001433238829,  # @TedeSupport
    -1001419516987,  # @VeezSupportGroup
    -1001752592753,  # @Skyzusupport
]


def _all_plugins():
    from glob import glob
    from os.path import basename, dirname, isfile

    p = glob(dirname(__file__) + "/*.py")
    return [basename(f)[:-3] for f in p if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")]


ALL_PLUGINS = sorted(_all_plugins())
