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

from .network import network_init, network_term
import logging
from .iotedge_twin import (
    iotedge_twin_get,
    iotedge_get_app_name,
    iotedge_get_module_id,
    iotedge_get_runtime_id,
)

_logger = logging.getLogger(__name__)


class Globals:
    def __init__(self):
        self.initialized = False
        self.app_name = None
        self.module_id = None
        self.runtime_id = None
        self.network_glob = None


glob = Globals()


async def application_module_init_from_environment(loop):
    """
    Initialize the Edgefarm Application SDK layer.
    This function must be called before any other SDK function.

    It determines the Application name and module ID from the IoTEdge
    environment and initializes the Networking of this module.

    :param loop: asyncio loop
    """
    await iotedge_twin_get()
    await application_module_init(
        loop, iotedge_get_app_name(), iotedge_get_module_id(), iotedge_get_runtime_id()
    )


async def application_module_init(loop, app_name, module_id, runtime_id):
    """
    Initialize the Edgefarm Application SDK layer.
    It is usually called from `application_module_init_from_environment()` but
    can be called directly for testing outside an IoTEdge environment.

    :param loop: asyncio loop
    :param app_name: application name
    :param module_id: String identifying the module
    :param runtime_id: String identifying the runtime
    """
    global glob

    glob.app_name = app_name
    glob.module_id = module_id
    glob.runtime_id = runtime_id

    glob.network_glob = await network_init(loop)
    glob.initialized = True


def application_module_check_initialized():
    global glob
    if not glob.initialized:
        raise RuntimeError(
            "alm module not initialized! Call application_module_init*()"
        )


def application_module_app_name():
    global glob
    application_module_check_initialized()
    return glob.app_name


def application_module_module_id():
    global glob
    application_module_check_initialized()
    return glob.module_id


def application_module_runtime_id():
    global glob
    application_module_check_initialized()
    return glob.runtime_id


def application_module_network_nats():
    global glob
    application_module_check_initialized()
    return glob.network_glob.nc


async def application_module_term():
    """
    De-Initialize the Edgefarm SDK ALM layer.
    This function must be called after cleaning
    up all other EdgeFarm SDK objects (and not before!)
    """
    global glob
    if glob.initialized:
        await network_term()
        glob.initialized = False
