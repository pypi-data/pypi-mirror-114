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
import fastavro


def schema_load_builtin(code_rel_path, schema_filename):
    """
    Load Avro schema file built into this library.
    <schema_filename> schema file name without ".avsc" extension,
    relative to the caller's directory.

    Example usage
    ```
    codec = schema_load_builtin(__file__, "example")
    ```
    """
    code_dir_path = os.path.dirname(os.path.abspath(code_rel_path))
    return schema_load(os.path.join(code_dir_path, f"{schema_filename}.avsc"))


def schema_load(schema_file):
    return fastavro.schema.load_schema(schema_file)


def schema_read_builtin(code_rel_path, filename):
    """
    Read Avro schema file built into this library,
    but don't parse it by fastavro.

    Usefull to read a built-in file and pass it to AdsEncoder.

    <schema_filename> schema file name without ".avsc" extension,
    relative to the caller's directory.

    Example usage
    ```
    codec = schema_read_builtin(__file__, "example")
    ```
    """
    code_dir_path = os.path.dirname(os.path.abspath(code_rel_path))
    with open(os.path.join(code_dir_path, filename)) as fd:
        content = fd.read()
    return content
