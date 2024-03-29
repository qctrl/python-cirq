# Copyright 2022 Q-CTRL
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
===========
qctrlcirq
===========
"""

__version__ = "0.0.5"

from .circuit import convert_dds_to_cirq_circuit

from .schedule import convert_dds_to_cirq_schedule

__all__ = [
    "convert_dds_to_cirq_circuit",
    "convert_dds_to_cirq_schedule",
]
