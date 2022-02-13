# getter < https://t.me/kastaid >
# Copyright (C) 2022 - kastaid
# All rights reserved.
#
# This file is a part of < https://github.com/kastaid/getter/ >
# PLease read the GNU Affero General Public License in;
# < https://www.github.com/kastaid/getter/blob/main/LICENSE/ >
# ================================================================

from asyncio import get_event_loop
from pathlib import Path
from platform import python_version
from sys import exit, platform, version_info
from time import time

StartTime = time()
__version__ = "0.1.9"

if not platform.startswith("linux"):
    print("MUST be use Linux platform, currently {}. Quitting...".format(platform))
    exit(1)

if version_info.major < 3 or version_info.minor < 9:
    print("MUST be use Python version of least 3.9.x currently {}. Quitting...".format(python_version()))
    exit(1)

Root: Path = Path(__file__).parent.parent
LOOP = get_event_loop()
HELP = {}
CMD_LIST = {}
