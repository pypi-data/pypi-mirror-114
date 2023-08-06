# pylint: disable=useless-import-alias

import asyncio
import sys
from typing import Tuple

# Shortcuts
from .parser import probe as probe

__all__: Tuple[str, ...] = ("probe",)

# Workaround for known issue of aiohttp on Windows / Python 3.8
# See: https://github.com/aio-libs/aiohttp/issues/4324
if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform == "win32":
    # pylint: disable=no-member
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
