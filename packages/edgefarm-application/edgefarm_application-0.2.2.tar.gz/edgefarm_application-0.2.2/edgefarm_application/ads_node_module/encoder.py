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

import json
import logging
import fastavro
from edgefarm_application.base.avro import schemaless_encode
from edgefarm_application.base.schema import schema_load_builtin

_logger = logging.getLogger(__name__)


class AdsEncoder:
    """
    Encoder to generate ADS_DATA message from the user's payload.

    Create an instance of this class for each stream you want to publish to ADS and pass the
    instance to `AdsProducer.encode_and_send`

    Both `schema_name` and `schema_version` will be embedded into the ADS_DATA envelope, so
    that the receiver knows how the data has been encoded.

    :param payload_schama str: Content of an AVRO schema file as a string to encode the user payload
    :param schema_name str: Name of schema without ".avsc"
    :param schema_version tuple: Version of the payload schema as a tuple (major,minor,patch)
    :param tags dict: Tags to embed into ADS_DATA, e.g. `{ 'monitor': 'channel1' }`
    """

    ads_schema = schema_load_builtin(__file__, "ads_data")

    def __init__(self, payload_schema, schema_name, schema_version, tags):
        schema_dict = json.loads(payload_schema)
        self._payload_schema = fastavro.parse_schema(schema_dict)
        self._schema_name = schema_name
        self._schema_version = schema_version
        self._tags = self.convert_tags(tags)
        self._sequence_number = 0

    def encode(self, app_name, module_id, runtime_id, data):
        """
        Generate an ADS_DATA avro (schemaless) message with an embedded avro payload of using the payload
        schema passed to the constructor.

        The `data` must be a python dict that matches the payload schema.

        :param app_name str: Application name
        :param module_id str: Module id
        :param runtime_id str: Runtime id
        :param data dict: User payload to encode.
        """

        # payload schema version reported in ads data and payload
        schema_version_bytes = self.version_to_bin(self._schema_version)
        data["meta"] = {}
        data["meta"]["version"] = schema_version_bytes

        # encode payload
        payload = schemaless_encode(data, self._payload_schema)

        # encode ADS_DATA
        msg = {
            "meta": {"version": b"\x01\x00\x00"},
            "origin": {
                "app": app_name,
                "module": module_id,
                "runtime": runtime_id,
                "tags": self._tags,
                "sequenceNumber": self._sequence_number,
            },
            "payload": {
                "format": "avro",
                "schema": self._schema_name + ".avsc",
                "schemaVersion": schema_version_bytes,
                "data": payload,
            },
        }
        avro_msg = schemaless_encode(msg, self.ads_schema)
        self._sequence_number += 1
        return avro_msg

    @staticmethod
    def version_to_bin(version):
        if len(version) != 3:
            raise ValueError(f"Wrong format of schema version {version}. Must be (x,y,z)")
        major, minor, patch = version
        return ((major << 16) + (minor << 8) + patch).to_bytes(3, byteorder="big")

    @staticmethod
    def convert_tags(tags):
        ret = []

        for key, value in tags.items():
            ret.append({"key": key, "value": value})
        return ret
