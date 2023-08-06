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
from edgefarm_application.base.avro import schema_decode, schema_encode
from edgefarm_application.base.application_module import application_module_network_nats
from edgefarm_application.base.schema import schema_load_builtin

_logger = logging.getLogger(__name__)


class AlmMqttModuleClient:
    """
    Interact with the `mqtt-bridge`.
    Supports registering and unregistering to MQTT topics proxied over nats
    via `mqtt-bridge`.

    Example usage:
    ``
    import edgefarm_application as ef

    async def handler(msg):
        payload = json.loads(msg["payload"])
        print(f"{msg}: payload={payload}")

    await ef.application_module_init_from_environment(loop)
    mqtt_client = ef.AlmMqttModuleClient()
    await mqtt_client.subscribe("my-subject", subject_handler)
    ``
    """

    def __init__(self):
        self._nc = application_module_network_nats()
        # Internal storage for nats subjects and its corresponding subscription IDs
        self._subjects = {}
        self._subject_handlers = {}

        self._register_sub_request_codec = schema_load_builtin(
            __file__, "registerSubRequest"
        )
        self._unregister_sub_request_codec = schema_load_builtin(
            __file__, "unregisterSubRequest"
        )
        self._pub_request_codec = schema_load_builtin(__file__, "pubRequest")
        self._reqres_request_codec = schema_load_builtin(
            __file__, "reqResRequest")

    async def close(self):
        """Close the connection to `mqtt-bridge` and the nats server.

        Example usage:

        ```
        await mqtt_client.close()
        ```
        """
        try:
            for s in list(self._subjects):
                await self.unsubscribe(s)
        except Exception as e:
            _logger.exception(
                f"Exception {e} while unsubscribing subjects (ignored)")

    async def subscribe(self, topic, handler):
        """Subscribe to a MQTT topic and register a handler function.

        The handler gets called with <msg> which is a python dictionary that
        contains currently: device, acqTime and payload.

        payload is the MQTT message.

        Example usage:
        ```
        async def handler(msg):
            payload = json.loads(msg["payload"])
            print(f"{msg}: payload={payload}")

        await mqttClient.subscribe("mqtt/topic", handler)

        Note: Currently, MQTT wildcards, e.g. + or # don't work.

        ```
        """
        nats_subject = await self._register_mqtt_topic("mqtt-bridge", topic)
        self._subjects[nats_subject] = await self._nc.subscribe(
            subject=nats_subject, cb=self.__nats_handler
        )
        self._subject_handlers[nats_subject] = handler
        _logger.debug(
            f"subscribed to mqtt {topic}, nats subject {nats_subject}")
        return nats_subject

    async def publish(self, mqtt_topic, payload):
        """
        Publish a MQTT message via the ALM MQTT module.

        This call uses NATS req/reply pattern and waits
        until ALM MQTT module has replied

        :param mqtt_topic str: MQTT topic name
        :param payload bytes: payload as bytes
        :raise: RuntimeError if ALM MQTT module reports an error
        """
        request_msg = {"topic": mqtt_topic, "payload": payload}

        data = schema_encode(request_msg, self._pub_request_codec)

        resp_msg = await self._nc.request("mqtt-bridge.publish", data)

        resp = schema_decode(resp_msg.data)
        if len(resp["error"]) > 0:
            raise RuntimeError(
                f"Error publishing MQTT topic {mqtt_topic}: {resp['error']}"
            )

    async def request(self, mqtt_topic, payload, timeout: int):
        """
        Send a MQTT request via the ALM MQTT module and wait for response from
        the peer MQTT client. This feature uses MQTT V5 request/response pattern

        Internally, this call uses NATS req/reply pattern and waits
        until ALM MQTT module has replied

        :param mqtt_topic str: MQTT topic name to send request to
        :param payload bytes: payload as bytes
        :param timeout int: Timeout to wait for response from MQTT peer client in ms
        :return: response from peer MQTT client
        :raise: RuntimeError if ALM MQTT module reports an error
        """
        request_msg = {"topic": mqtt_topic,
                       "payload": payload, "timeout": timeout}

        data = schema_encode(request_msg, self._reqres_request_codec)

        # perform MQTT request/response with a NATS request/reply.
        # Set the NATS timeout 5s longer than the MQTT request/response timeout
        resp_msg = await self._nc.request(
            "mqtt-bridge.request-response", data, timeout=timeout / 1000 + 5
        )
        resp = schema_decode(resp_msg.data)
        if len(resp["error"]) > 0:
            raise RuntimeError(
                f"Error in req/res MQTT topic {mqtt_topic}: {resp['error']}"
            )
        return resp["payload"]

    async def __nats_handler(self, msg):
        _logger.debug(f"__nats_handler: {msg}")
        # Send ACK
        await self._nc.publish(msg.reply, b"")
        # Convert AVRO to dict
        m = schema_decode(msg.data)
        # Call handler
        await self._subject_handlers[msg.subject](m)

    async def unsubscribe(self, subject):
        """Unsubscribe from a previously registered nats subject.
        Raises an ValueError if subject was not found.

        Example usage:

        ```
        subject = await mqttClient.subscribe("mqtt/topic", handler)

        try:
            await mqttClient.unsubscribe(subject)
        except Exception as e:
            print(e)
        ```
        """
        if subject in self._subjects.keys():
            await self._unregister_mqtt_topic("mqtt-bridge", subject)
            await self._nc.unsubscribe(self._subjects[subject])
            del self._subjects[subject]
        else:
            raise ValueError("Subject '{subject}' not subscribed")

    async def _register_mqtt_topic(self, target, topic):
        msg = {"topic": topic}
        data = schema_encode(msg, self._register_sub_request_codec)

        resp_msg = await self._nc.request(target + ".config.register", data, timeout=2)
        resp = schema_decode(resp_msg.data)

        if len(resp["error"]) > 0:
            raise RuntimeError(
                f"Can't register MQTT Topic {topic}: {resp['error']}")

        return resp["subject"]

    async def _unregister_mqtt_topic(self, target, subject):
        msg = {"subject": subject}
        data = schema_encode(msg, self._unregister_sub_request_codec)
        resp_msg = await self._nc.request(
            target + ".config.unregister", data, timeout=2
        )
        resp = schema_decode(resp_msg.data)
        if len(resp["error"]) > 0:
            raise RuntimeError(
                f"Can't unregister MQTT Topic. NATS-subject: {subject}: {resp['error']}"
            )
