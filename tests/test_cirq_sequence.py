# Copyright 2021 Q-CTRL
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
===================================
Tests converstion to Cirq Circuit
===================================
"""

import cirq
import numpy as np
from qctrlcirq import convert_dds_to_cirq_circuit, convert_dds_to_cirq_schedule
from qctrlopencontrols import (
    new_carr_purcell_sequence,
    new_cpmg_sequence,
    new_periodic_sequence,
    new_quadratic_sequence,
    new_spin_echo_sequence,
    new_uhrig_sequence,
    new_walsh_sequence,
    new_x_concatenated_sequence,
    new_xy_concatenated_sequence,
)

_callable = {
    "Spin echo": new_spin_echo_sequence,
    "Carr-Purcell": new_carr_purcell_sequence,
    "Carr-Purcell-Meiboom-Gill": new_cpmg_sequence,
    "Uhrig single-axis": new_uhrig_sequence,
    "periodic single-axis": new_periodic_sequence,
    "quadratic": new_quadratic_sequence,
    "Walsh single-axis": new_walsh_sequence,
    "Quadratic": new_quadratic_sequence,
    "X concatenated": new_x_concatenated_sequence,
    "XY concatenated": new_xy_concatenated_sequence,
}


def _create_test_sequence(sequence_scheme, pre_post_rotation):

    """
    Create a DD sequence of choice.

    Parameters
    ----------
    sequence_scheme : str
        One of 'Spin echo', 'Carr-Purcell', 'Carr-Purcell-Meiboom-Gill',
        'Uhrig single-axis', 'Periodic single-axis', 'Walsh single-axis',
        'Quadratic', 'X concatenated',
        'XY concatenated'
    pre_post_rotation : bool
        If True, adds a :math:`X_{\\pi/2}` gate on either ends

    Returns
    -------
    DynamicDecouplingSequence
        The Dynamical Decoupling Sequence instance built from supplied
        schema information
    """

    dd_sequence_params = {}
    dd_sequence_params["duration"] = 4
    dd_sequence_params["pre_post_rotation"] = pre_post_rotation

    # 'spin_echo' does not need any additional parameter

    if sequence_scheme in [
        "Carr-Purcell",
        "Carr-Purcell-Meiboom-Gill",
        "Uhrig single-axis",
        "periodic single-axis",
    ]:

        dd_sequence_params["offset_count"] = 2

    elif sequence_scheme in ["Walsh single-axis"]:

        dd_sequence_params["paley_order"] = 5

    elif sequence_scheme in ["quadratic"]:

        dd_sequence_params["duration"] = 16
        dd_sequence_params["outer_offset_count"] = 4
        dd_sequence_params["inner_offset_count"] = 4

    elif sequence_scheme in ["X concatenated", "XY concatenated"]:

        dd_sequence_params["duration"] = 16
        dd_sequence_params["concatenation_order"] = 2

    sequence = _callable[sequence_scheme](**dd_sequence_params)
    return sequence


def _check_circuit_output(pre_post_rotation, conversion_method, expected_state):
    """Check the outcome of a circuit against expected outcome"""

    simulator = cirq.Simulator()
    for sequence_scheme in [
        "Carr-Purcell",
        "Carr-Purcell-Meiboom-Gill",
        "Uhrig single-axis",
        "periodic single-axis",
        "Walsh single-axis",
        "quadratic",
        "X concatenated",
        "XY concatenated",
    ]:
        sequence = _create_test_sequence(sequence_scheme, pre_post_rotation)
        cirq_circuit = conversion_method(
            dynamic_decoupling_sequence=sequence, add_measurement=True
        )

        results = simulator.run(cirq_circuit)
        assert results.measurements["qubit-0"] == expected_state


def test_cirq_circuit_operation():

    """Tests if the Dynamic Decoupling Sequence gives rise to expected
    state with different pre-post gates parameters in cirq circuits
    """
    _check_circuit_output(False, convert_dds_to_cirq_circuit, 0)
    _check_circuit_output(True, convert_dds_to_cirq_circuit, 0)

    _check_circuit_output(False, convert_dds_to_cirq_schedule, 0)
    _check_circuit_output(True, convert_dds_to_cirq_schedule, 0)


if __name__ == "__main__":
    pass
