# Copyright 2019 The Blueqat Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utilities for convenient."""
from collections import Counter
import typing
from typing import Dict, Tuple, Union

import numpy as np

if typing.TYPE_CHECKING:
    from . import Circuit


def to_inttuple(
    bitstr: Union[str, Counter, Dict[str, int]]
) -> Union[Tuple, Counter, Dict[Tuple, int]]:
    """Convert from bit string likes '01011' to int tuple likes (0, 1, 0, 1, 1)

    Args:
        bitstr (str, Counter, dict): String which is written in "0" or "1".
            If all keys are bitstr, Counter or dict are also can be converted by this function.

    Returns:
        tuple of int, Counter, dict: Converted bits.
            If bitstr is Counter or dict, returns the Counter or dict
            which contains {converted key: original value}.

    Raises:
        ValueError: If bitstr type is unexpected or bitstr contains illegal character.
    """
    if isinstance(bitstr, str):
        return tuple(int(b) for b in bitstr)
    if isinstance(bitstr, Counter):
        return Counter(
            {tuple(int(b) for b in k): v
             for k, v in bitstr.items()})
    if isinstance(bitstr, dict):
        return {tuple(int(b) for b in k): v for k, v in bitstr.items()}
    raise ValueError("bitstr type shall be `str`, `Counter` or `dict`")


def ignore_global_phase(statevec: np.ndarray) -> np.ndarray:
    """Multiple e^-iθ to `statevec` where θ is a phase of first non-zero element.

    Args:
        statevec np.ndarray: Statevector.

    Returns:
        np.ndarray: `statevec` is returned.
    """
    for q in statevec:
        if abs(q) > 0.0000001:
            ang = abs(q) / q
            statevec *= ang
            break
    return statevec


def check_unitarity(mat: np.ndarray) -> bool:
    """Check whether mat is a unitary matrix."""
    shape = mat.shape
    if len(shape) != 2 or shape[0] != shape[1]:
        # Not a square matrix.
        return False
    return np.allclose(mat @ mat.T.conjugate(), np.eye(shape[0]))


def circuit_to_unitary(circ: 'Circuit', *runargs, **runkwargs):
    """Make circuit to unitary. This function is experimental feature and
    may changed or deleted in the future."""

    # To avoid circuilar import, import here.
    from . import Circuit

    runkwargs.setdefault('returns', 'statevector')
    runkwargs.setdefault('ignore_global', False)
    n_qubits = circ.n_qubits
    vecs = []
    if n_qubits == 0:
        return np.array([[1]])
    for i in range(1 << n_qubits):
        bitmask = tuple(k for k in range(n_qubits) if (1 << k) & i)
        c = Circuit()
        if bitmask:
            c.x[bitmask]
        c += circ
        vecs.append(c.run(*runargs, **runkwargs))
    return np.array(vecs).T
