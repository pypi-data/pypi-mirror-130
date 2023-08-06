import numpy as np
from quantumsim.sparsedm import *
from quantumsim.circuit import *
from quantumsim.ptm import *
import random
import math

# from .quantumsim_wrapper import interface_quantumsim
from .if_qubit_sim import If_qubit_sim
from pyqcas.utils import get_logger
import re

import logging

logger = get_logger((__name__).split(".")[-1])

round_precision = 4

SINGLE_QUBIT_GATE_HELPER = {
    "h": (hadamard_ptm, ()),
    "x": (rotate_x_ptm, (np.pi,)),
    "y": (rotate_y_ptm, (np.pi,)),
    "z": (rotate_z_ptm, (np.pi,)),
    "s": (rotate_z_ptm, (np.pi / 2,)),
    "sdg": (rotate_z_ptm, (-np.pi / 2,)),
    "t": (rotate_z_ptm, (np.pi / 4,)),
    "tdg": (rotate_z_ptm, (-np.pi / 4,)),
}

logger = get_logger((__name__).split(".")[-1])


def arb_rotate_ptm(opcode):
    """Function for generating single qubit arbitrary-angle rotation ptm."""

    # In eqasm, '.' is represented by '_'
    # For RX/RY/RZ, direction should be empty
    # For X/Y/Z, direction should be 'M' or empty
    pattern = re.compile(
        r"(R)?(?P<axis>[XYZ])(?P<direction>(?(1)\B|M?))(?P<angle>\d+(\_\d+)?)",
        re.IGNORECASE,
    )
    m = pattern.fullmatch(opcode)
    if m == None:
        raise ValueError("Invalid quantum operation code")

    axis = m.group("axis").lower()
    f = float(m.group("angle").replace("_", "."))
    angle = -f if m.group("direction") != "" else f

    radian = math.radians(angle)
    ptm_gen = SINGLE_QUBIT_GATE_HELPER[axis][0]
    ptm = ptm_gen(radian)
    return ptm


class Quantumsim(If_qubit_sim):
    def __init__(self, no_qubits: int, log_level=logging.WARNING):
        """
        Interface for the qubit state simulator .
        """
        self._no_qubits = no_qubits
        self._sdm = SparseDM(no_qubits)
        self.res = None

        # Qubits physical attributes for quantifying phase damping
        self.t1 = np.inf
        self.t2 = np.inf

        self.set_log_level(log_level)
        logger.info("initialize quantumsim")

    def set_log_level(self, log_level):
        logger.setLevel(log_level)

    def _idle_ptm(self, idle_duration):
        """Return phase damping ptm for a given idle duration."""
        t1 = self.t1
        t2 = self.t2

        if t2 == 2 * t1:
            t_phi = np.inf
        else:
            t_phi = 1 / (1 / t2 - 1 / (2 * t1)) / 2

        gamma = 1 - np.exp(-idle_duration / t1)
        lamda = 1 - np.exp(-idle_duration / t_phi)

        return amp_ph_damping_ptm(gamma, lamda)

    def apply_idle_gate(self, idle_duration, qubit):
        """Apply phase damping gate for all qubits."""
        # Note: This method has no reference in this project!!
        #! I don't know how to test this method due to lack of knowledge about idle gate
        # TODO Add tests for this method
        for qubit in self._no_qubits:
            self._sdm.apply_ptm(self._idle_ptm(idle_duration), qubit)

    def apply_single_qubit_gate(self, operation, qubit):
        logger.info("apply operation {} on qubit {}".format(operation, qubit))

        if operation.lower() == "null":
            return

        if operation.lower() in SINGLE_QUBIT_GATE_HELPER.keys():
            ptm_gen, args = SINGLE_QUBIT_GATE_HELPER[operation.lower()]
            self._sdm.apply_ptm(qubit, ptm_gen(*args))
            return

        # Invalid quantum operation code will raise an error in this func
        self._sdm.apply_ptm(qubit, arb_rotate_ptm(operation))

    def apply_two_qubit_gate(self, qubit0, qubit1):
        logger.info("apply CZ on qubit pair ({}, {})".format(qubit0, qubit1))
        self._sdm.cphase(
            qubit0, qubit1
        )  # Execute all pending single qubit gates and the CZ

    def measure_qubit(self, qubit, ph_damp=0):
        logger.info("measure qubit: {}".format(qubit))
        self._sdm.apply_ptm(qubit, self._idle_ptm(ph_damp))

        logger.debug("Prepare to measure qubit %s", qubit)
        logger.debug(
            "The full density matrix before applying measurement: \n\t{}".format(
                "{}".format(
                    self._sdm.full_dm.to_array().round(round_precision)
                ).replace("\n", "\n\t")
            )
        )

        # Obtain the two partial traces (p0, p1) that define the probabilities
        # for measuring bit in state (0, 1)
        p0, p1 = self._sdm.peak_measurement(qubit)
        logger.debug("partial traces for this measurement: {}, {}".format(p0, p1))

        # Sample from these two possibilities

        # using default sample with seed random
        # declare, project, cond_prob = self.sampler.send((p0, p1))

        # using fully random
        r = random.random()
        logger.debug("the random value for measuremnt: {}".format(r))

        if r < p0 / (p0 + p1):
            project = 0
        else:
            project = 1

        # Project a bit to a fixed state, making it classical and reducing the size of the full density matrix.
        self._sdm.project_measurement(qubit, project)
        logger.info("The state of qubit %s is measured. The result is: %d", qubit, project)
        self._sdm.renormalize()

        return project

    def get_quantum_state(self, seperate=True):
        """Take the quantum state before measurements."""
        # Apply all rest cached single qubit gates
        self._sdm.apply_all_pending()

        if seperate:
            return {
                "classical": self._sdm.classical,
                "quantum": self._dm_to_vec(self._sdm.full_dm, self._sdm.idx_in_full_dm),
            }
        else:
            for qubit in self._sdm.names:
                self._sdm.ensure_dense(qubit)
            return self._dm_to_vec(self._sdm.full_dm, self._sdm.idx_in_full_dm)

    def _dm_to_vec(self, full_dm, idx_in_full_dm):
        """Method turning a pure state density matrix into state vector."""
        dm_array = full_dm.to_array()
        assert (
            2 ** (len(idx_in_full_dm.items())) == dm_array.shape[0] == dm_array.shape[1]
        )

        # The case where all qubits are non-quantum and dm is empty
        if idx_in_full_dm == {}:
            return [], 1  # Return empty qubits list and a trivial number

        num_col = dm_array.shape[1]  # Number of columns
        # The target state vector got from normalizing the column with the largest norm.
        # Mathematically, a colunm with non-zero norm is enough, but in real computer *some almost zero number is not zero*.
        # Thus, we choose the-largest-norm column to get away from that situation.
        state_vec = None
        cur_max_norm = 0
        for i in range(0, num_col):
            col_vec = dm_array[:, i]
            # This norm is just the norm of the current col's common (one-of-amplitude)* factor
            norm = np.linalg.norm(col_vec)
            if norm > cur_max_norm:
                state_vec = col_vec / norm
                cur_max_norm = norm

        # Get the corresponding qubit names list for the state vector
        names_indices = list(zip(idx_in_full_dm.keys(), idx_in_full_dm.values()))
        names_indices.sort(key=lambda pair: pair[1])

        names_seq = [pair[0] for pair in names_indices]
        return names_seq, state_vec
