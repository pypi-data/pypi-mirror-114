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

import logging
from edgefarm_application.base.application_module import (
    application_module_app_name,
    application_module_module_id,
    application_module_runtime_id,
    application_module_network_nats,
)

ADS_TOPIC_NAME = "ads"

_logger = logging.getLogger(__name__)


class AdsProducer:
    """
    Publish messages from an edgefarm application to edgefarm ADS

    Example usage:
    ``
    import edgefarm_application as ef

    await ef.application_module_init_from_environment(loop)
    ads = ef.AdsProducer()

    # Create an encoder for an application specific payload
    payload_schema = { .... }  # your avro schema
    encoder = ef.AdsEncoder(
        payload_schema,
        schema_name="temperature_data",
        schema_version=(1, 0, 0),
        tags={"monitor": "channel1"},
    )

    ads_payload = { 'mydata': 1234 }

    await ads.encode_and_send(encoder, ads_payload)
    ``

    This module uses the application name, module id and runtime id
    determined by application_module_init*()
    """

    def __init__(self):
        self._nc = application_module_network_nats()
        self._app_name = application_module_app_name()
        self._module_id = application_module_module_id()
        self._runtime_id = application_module_runtime_id()

    async def encode_and_send(self, encoder, data):
        """
        Encode `data` with the `encoder` and send it to ADS.

        The `data` must be a python dict that matches the payload schema provided to the
        encoder's constructor.

        :param encoder: The encoder to produce a bytestream containing an ADS_DATA record
        :param data dict: User payload to encode.
        """
        ads_data = encoder.encode(
            self._app_name, self._module_id, self._runtime_id, data
        )
        await self._send(ads_data)

    async def _send(self, data):
        await self._nc.publish(ADS_TOPIC_NAME, data)
