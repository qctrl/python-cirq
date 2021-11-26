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
============
cirq.circuit
============
"""

import numpy as np

import cirq

from qctrlopencontrols import DynamicDecouplingSequence

from qctrlopencontrols.exceptions import ArgumentsValueError

FIX_DURATION_UNITARY = "fixed duration unitary"
INSTANT_UNITARY = "instant unitary"


def convert_dds_to_cirq_circuit(
    dynamic_decoupling_sequence,
    target_qubits=None,
    gate_time=0.1,
    add_measurement=True,
    algorithm=INSTANT_UNITARY,
):
    """Converts a Dynamic Decoupling Sequence into quantum circuit
    as defined in cirq

    Parameters
    ----------
    dynamic_decoupling_sequence : DynamicDecouplingSequence
        The dynamic decoupling sequence
    target_qubits : list, optional
        List of target qubits for the sequence operation; the qubits must be
        cirq.Qid type; defaults to None in which case a 1-D lattice of one
        qubit is used (indexed as 0).
    gate_time : float, optional
        Time (in seconds) delay introduced by a gate; defaults to 0.1
    add_measurement : bool, optional
        If True, the circuit contains a measurement operation for each of the
        target qubits. Measurement from each of the qubits is associated
        with a string as key. The string is formatted as 'qubit-X' where
        X is a number between 0 and len(target_qubits).
    algorithm : str, optional
        One of 'fixed duration unitary' or 'instant unitary'; In the case of
        'fixed duration unitary', the sequence operations are assumed to be
        taking the amount of gate_time while 'instant unitary' assumes the sequence
        operations are instantaneous (and hence does not contribute to the delay between
        offsets). Defaults to 'instant unitary'.

    Returns
    -------
    cirq.Circuit
        The circuit containing gates corresponding to sequence operation.

    Raises
    ------
    ArgumentsValueError
        If any of the input parameters result in an invalid operation.

    Notes
    -----

    Dynamic Decoupling Sequences (DDS) consist of idealized pulse operation. Theoretically,
    these operations (pi-pulses in X,Y or Z) occur instantaneously. However, in practice,
    pulses require time. Therefore, this method of converting an idealized sequence
    results to a circuit that is only an approximate implementation of the idealized sequence.

    In idealized definition of DDS, `offsets` represents the instances within sequence
    `duration` where a pulse occurs instantaneously. A series of appropriate circuit components
    is placed in order to represent these pulses.

    In 'standard circuit', the `gaps` or idle time in between active pulses are filled up
    with `identity` gates. Each identity gate introduces a delay of `gate_time`. In this
    implementation, the number of identity gates is determined by
    :math:`int(np.floor(offset\\_distance / gate\\_time))`. As a consequence,
    :math:`int(np.floor(offset\\_distance / gate\\_time))`. As a consequence,
    the duration of the real-circuit is :math:`gate\\_time \\times number\\_of\\_identity\\_gates +
    pulse\\_gate\\_time \\times number\\_of\\_pulses`.

    Q-CTRL Cirq Adapter supports operation resulting in rotation around at most one axis at
    any offset.
    """

    if dynamic_decoupling_sequence is None:
        raise ArgumentsValueError(
            "No dynamic decoupling sequence provided.",
            {"dynamic_decoupling_sequence": dynamic_decoupling_sequence},
        )

    if not isinstance(dynamic_decoupling_sequence, DynamicDecouplingSequence):
        raise ArgumentsValueError(
            "Dynamical decoupling sequence is not recognized."
            "Expected DynamicDecouplingSequence instance",
            {"type(dynamic_decoupling_sequence)": type(dynamic_decoupling_sequence)},
        )

    if gate_time <= 0:
        raise ArgumentsValueError(
            "Time delay of gates must be greater than zero.", {"gate_time": gate_time}
        )

    target_qubits = target_qubits or [cirq.LineQubit(0)]

    if algorithm not in [FIX_DURATION_UNITARY, INSTANT_UNITARY]:
        raise ArgumentsValueError(
            "Algorithm must be one of {} or {}".format(
                INSTANT_UNITARY, FIX_DURATION_UNITARY
            ),
            {"algorithm": algorithm},
        )

    unitary_time = 0.0
    if algorithm == FIX_DURATION_UNITARY:
        unitary_time = gate_time

    rabi_rotations = dynamic_decoupling_sequence.rabi_rotations
    azimuthal_angles = dynamic_decoupling_sequence.azimuthal_angles
    detuning_rotations = dynamic_decoupling_sequence.detuning_rotations

    offsets = dynamic_decoupling_sequence.offsets

    time_covered = 0
    circuit = cirq.Circuit()
    for offset, rabi_rotation, azimuthal_angle, detuning_rotation in zip(
        list(offsets),
        list(rabi_rotations),
        list(azimuthal_angles),
        list(detuning_rotations),
    ):

        offset_distance = offset - time_covered

        if np.isclose(offset_distance, 0.0):
            offset_distance = 0.0

        if offset_distance < 0:
            raise ArgumentsValueError(
                "Offsets cannot be placed properly. Spacing between the rotations"
                "is smaller than the time required to perform the rotation. Provide"
                "a longer dynamic decoupling sequence or shorted gate time.",
                {
                    "dynamic_decoupling_sequence": dynamic_decoupling_sequence,
                    "gate_time": gate_time,
                },
            )

        while (time_covered + gate_time) <= offset:
            gate_list = []
            for qubit in target_qubits:
                gate_list.append(cirq.I(qubit))
            time_covered += gate_time
            circuit.append(gate_list)

        rotations = np.array(
            [
                rabi_rotation * np.cos(azimuthal_angle),
                rabi_rotation * np.sin(azimuthal_angle),
                detuning_rotation,
            ]
        )

        if np.sum(np.isclose(rotations, 0.0).astype(int)) == 1:
            raise ArgumentsValueError(
                "Open Controls support a sequence with one "
                "valid rotation at any offset. Found a sequence "
                "with multiple rotation operations at an offset.",
                {"dynamic_decoupling_sequence": dynamic_decoupling_sequence},
                extras={
                    "offset": offset,
                    "rabi_rotation": rabi_rotation,
                    "azimuthal_angle": azimuthal_angle,
                    "detuning_rotation": detuning_rotation,
                },
            )

        gate_list = []
        for qubit in target_qubits:
            if np.sum(np.isclose(rotations, 0.0).astype(int)) == 3:
                gate_list.append(cirq.I(qubit))
            else:
                if not np.isclose(rotations[0], 0.0):
                    gate_list.append(cirq.Rx(rotations[0])(qubit))
                elif not np.isclose(rotations[1], 0.0):
                    gate_list.append(cirq.Ry(rotations[1])(qubit))
                elif not np.isclose(rotations[2], 0.0):
                    gate_list.append(cirq.Rz(rotations[2])(qubit))
        circuit.append(gate_list)

        time_covered = offset + unitary_time

    if add_measurement:
        gate_list = []
        for idx, qubit in enumerate(target_qubits):
            gate_list.append(cirq.measure(qubit, key="qubit-{}".format(idx)))
        circuit.append(gate_list)

    return circuit
