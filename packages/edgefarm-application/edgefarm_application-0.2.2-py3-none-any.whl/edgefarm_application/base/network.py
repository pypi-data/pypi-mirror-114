# Copyright © 2021 Ci4Rail GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import logging
from nats.aio.client import Client as Nats


_logger = logging.getLogger(__name__)


class Globals:
    def __init__(self):
        self.nc = None
        self.loop = None


glob = Globals()


async def network_init(loop):
    """Initialize EdgeFarn Network Functionality.

    Currently: Connect to the nats server.
    You can specify the nats server by defining the environment
    variable `NATS_SERVER`, e.g. `nats:4222`.

    :param loop: asyncio loop
    """
    global glob

    if glob.nc is not None:
        raise RuntimeError(f"{__name__}: Already initialized")

    glob.nc = Nats()
    glob.loop = loop

    nats_server = os.getenv("NATS_SERVER", "nats:4222")
    options = {
        "servers": ["nats://" + nats_server],
        "loop": glob.loop,
        "connect_timeout": 10,
        "ping_interval": 1,
        "max_outstanding_pings": 5,
    }

    await glob.nc.connect(**options)
    return glob


async def network_term():
    """De-initialize EdgeFarn Network Functionality.

    Currently: Close connection to the nats server.
    """
    global glob

    if glob.nc.is_closed:
        return
    try:
        await glob.nc.close()
    except Exception as e:
        _logger.exception(f"Exception {e} closing NATS (ignored)")
