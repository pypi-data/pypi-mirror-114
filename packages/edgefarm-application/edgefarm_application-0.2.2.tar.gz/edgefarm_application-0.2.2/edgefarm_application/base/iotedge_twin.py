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
import asyncio
from azure.iot.device.aio import IoTHubModuleClient

_logger = logging.getLogger(__name__)

UNKNOWN_APP = "UNKNOWN_APP"
twin = None


async def iotedge_twin_get():
    global twin
    module_client = IoTHubModuleClient.create_from_edge_environment()
    await module_client.connect()
    while True:
        twin = await module_client.get_twin()
        if iotedge_get_app_name() != UNKNOWN_APP:
            break
        _logger.error("Module twin not up to date yet. No property called 'applicationName' found. Retrying...")
        await asyncio.sleep(1)
    await module_client.shutdown()


def iotedge_get_app_name():
    global twin
    app_name = UNKNOWN_APP
    try:
        app_name = twin['desired']['applicationName']
    except KeyError:
        _logger.error("No applicationName in module twin")
    except TypeError:
        raise RuntimeError("module twin is no dictionary. Did you forget to call iotedge_twin_get()?")
    return app_name


def iotedge_get_module_id():
    return os.getenv("IOTEDGE_MODULEID", "UNKNOWN_MODULE")


def iotedge_get_runtime_id():
    return os.getenv("IOTEDGE_DEVICEID", "UNKNOWN_RUNTIME")
