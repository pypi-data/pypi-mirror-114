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

from io import BytesIO
from fastavro import writer, reader, schemaless_writer, schemaless_reader


def schema_encode(msg, schema):
    """
    Binary encoding of message which must be a python dictionary.
    Schema will be part of binary.
    Return binary as bytes.
    """
    records = [msg]
    fo = BytesIO()
    writer(fo=fo, schema=schema, records=records)
    fo.seek(0)
    return fo.read()


def schema_decode(data):
    """
    Decoding of an Avro binary that contains the schema.
    <data> must be bytes.
    Only the first message in data is considered. Further messages
    are ignored
    """
    fo = BytesIO(data)
    m = reader(fo)
    return m.next()


def schemaless_encode(msg, schema):
    """
    Binary encoding of message, which must be a python dictionary.
    Schema is NOT part of binary.
    Return binary as bytes.
    """
    fo = BytesIO()
    schemaless_writer(fo=fo, schema=schema, record=msg)
    fo.seek(0)
    return fo.read()


def schemaless_decode(data, schema):
    """
    Decoding of a schemaless Avro binary.
    <data> must be bytes.

    """
    fo = BytesIO(data)
    m = schemaless_reader(fo, schema)
    return m
