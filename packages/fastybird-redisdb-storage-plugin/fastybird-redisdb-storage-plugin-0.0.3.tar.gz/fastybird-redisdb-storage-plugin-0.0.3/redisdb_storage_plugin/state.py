#!/usr/bin/python3

#     Copyright 2021. FastyBird s.r.o.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

# Library dependencies
import uuid
from abc import ABC
from typing import Dict, List


#
# Storage item record
#
# @package        FastyBird:RedisDbStoragePlugin!
# @subpackage     State
#
# @author         Adam Kadlec <adam.kadlec@fastybird.com>
#
class StorageItem(ABC):
    _id: uuid.UUID
    _raw: Dict

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        item_id: uuid.UUID,
        raw: Dict,
    ) -> None:
        self._id = item_id
        self._raw = raw

    # -----------------------------------------------------------------------------

    @property
    def id(self) -> uuid.UUID:
        return self._id

    # -----------------------------------------------------------------------------

    @property
    def raw(self) -> Dict:
        return self._raw

    # -----------------------------------------------------------------------------

    @staticmethod
    def create_fields() -> Dict[str or int, str or int or float]:
        return {
            0: "id",
        }

    # -----------------------------------------------------------------------------

    @staticmethod
    def update_fields() -> List[str]:
        return []
