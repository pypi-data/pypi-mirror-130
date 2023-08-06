# Repository: https://gitlab.com/quantify-os/quantify-scheduler
# Licensed according to the LICENCE file on the master branch
"""Compiler for the quantify.scheduler."""
from __future__ import annotations
import importlib
import logging
from typing_extensions import Literal

import jsonschema
from quantify.utilities.general import load_json_schema

from quantify.scheduler.acquisition_library import SSBIntegrationComplex, Trace
from quantify.scheduler.pulse_library import (
    DRAGPulse,
    IdlePulse,
    SoftSquarePulse,
    SquarePulse,
)
from quantify.scheduler.resources import BasebandClockResource, ClockResource
from quantify.scheduler.types import Schedule


def determine_absolute_timing(
    schedule: Schedule, time_unit: Literal["physical", "ideal"] = "physical"
) -> Schedule:
    """
    Determines the absolute timing of a schedule based on the timing constraints.

    This function determines absolute timings for every operation in the
    :attr:`~quantify.scheduler.types.Schedule.timing_constraints`. It does this by:

        1. iterating over all and elements in the :attr:`~quantify.scheduler.types.Schedule.timing_constraints`.
        2. determining the absolute time of the reference operation.
        3. determining the start of the operation based on the `rel_time` and `duration` of operations.

    Parameters
    ----------
    schedule :
        The schedule for which to determine timings.
    time_unit :
        Whether to use physical units to determine the absolute time or ideal time.
        When :code:`time_unit == 'physical'` the duration attribute is used.
        When :code:`time_unit == 'ideal'` the duration attribute is ignored and treated
        as if it is :code:`1`.

    Returns
    -------
    :
        a new schedule object where the absolute time for each operation has been determined.
    """
    if len(schedule.timing_constraints) == 0:
        raise ValueError("schedule '{}' contains no operations".format(schedule.name))

    valid_time_units = ("physical", "ideal")
    if time_unit not in valid_time_units:
        raise ValueError(
            f"Undefined time_unit '{time_unit}'! Must be one of {valid_time_units}"
        )

    # iterate over the objects in the schedule.
    last_constr = schedule.timing_constraints[0]
    last_op = schedule.operations[last_constr["operation_hash"]]

    last_constr["abs_time"] = 0

    for t_constr in schedule.data["timing_constraints"][1:]:
        curr_op = schedule.operations[t_constr["operation_hash"]]
        if t_constr["ref_op"] is None:
            ref_constr = last_constr
            ref_op = last_op
        else:
            # this assumes the reference op exists. This is ensured in schedule.add
            ref_constr = next(
                item
                for item in schedule.timing_constraints
                if item["label"] == t_constr["ref_op"]
            )
            ref_op = schedule.operations[ref_constr["operation_hash"]]

        # duration = 1 is useful when e.g., drawing a circuit diagram.
        duration_ref_op = ref_op.duration if time_unit == "physical" else 1

        if t_constr["ref_pt"] == "start":
            t0 = ref_constr["abs_time"]
        elif t_constr["ref_pt"] == "center":
            t0 = ref_constr["abs_time"] + duration_ref_op / 2
        elif t_constr["ref_pt"] == "end":
            t0 = ref_constr["abs_time"] + duration_ref_op
        else:
            raise NotImplementedError(
                'Timing "{}" not supported by backend'.format(ref_constr["abs_time"])
            )

        duration_new_op = curr_op.duration if time_unit == "physical" else 1

        if t_constr["ref_pt_new"] == "start":
            t_constr["abs_time"] = t0 + t_constr["rel_time"]
        elif t_constr["ref_pt_new"] == "center":
            t_constr["abs_time"] = t0 + t_constr["rel_time"] - duration_new_op / 2
        elif t_constr["ref_pt_new"] == "end":
            t_constr["abs_time"] = t0 + t_constr["rel_time"] - duration_new_op

        # update last_constraint and operation for next iteration of the loop
        last_constr = t_constr
        last_op = curr_op

    return schedule


def _find_edge(device_cfg, q0, q1, op_name):
    try:
        edge_cfg = device_cfg["edges"]["{}-{}".format(q0, q1)]
    except KeyError:
        raise ValueError(
            "Attempting operation '{}' on qubits {} and {} which lack a connective edge.".format(
                op_name, q0, q1
            )
        )
    return edge_cfg


def add_pulse_information_transmon(schedule: Schedule, device_cfg: dict) -> Schedule:
    """
    Adds pulse information specified in the device config to the schedule.

    Parameters
    ------------
    schedule :
        The schedule for which to add pulse information.

    device_cfg :
        A dictionary specifying the required pulse information.


    Returns
    ----------
    :
        a new schedule object where the pulse information has been added.


    .. rubric:: Supported operations


    The following gate type operations are supported by this compilation step.

    - :class:`~quantify.scheduler.gate_library.Rxy`
    - :class:`~quantify.scheduler.gate_library.Reset`
    - :class:`~quantify.scheduler.gate_library.Measure`
    - :class:`~quantify.scheduler.gate_library.CZ`


    .. rubric:: Configuration specification

    .. jsonschema:: schemas/transmon_cfg.json

    """
    validate_config(device_cfg, scheme_fn="transmon_cfg.json")

    for op in schedule.operations.values():
        if op.valid_pulse:
            for p in op["pulse_info"]:
                if p["clock"] not in schedule.resources:
                    raise ValueError(
                        "Operation '{}' contains an unknown clock '{}'; ensure this resource has been "
                        "added to the schedule.".format(op.hash, p["clock"])
                    )
            continue

        if op.valid_acquisition:
            continue

        if op["gate_info"]["operation_type"] == "measure":
            for idx, q in enumerate(op["gate_info"]["qubits"]):
                q_cfg = device_cfg["qubits"][q]
                if q_cfg["params"]["acquisition"] == "SSBIntegrationComplex":
                    # readout pulse
                    op.add_pulse(
                        SquarePulse(
                            amp=q_cfg["params"]["ro_pulse_amp"],
                            duration=q_cfg["params"]["ro_pulse_duration"],
                            port=q_cfg["resources"]["port_ro"],
                            clock=q_cfg["resources"]["clock_ro"],
                        )
                    )
                    op.add_acquisition(
                        SSBIntegrationComplex(
                            duration=q_cfg["params"]["ro_acq_integration_time"],
                            t0=q_cfg["params"]["ro_acq_delay"],
                            acq_channel=op["gate_info"]["acq_channel"][idx],
                            acq_index=op["gate_info"]["acq_index"][idx],
                            port=q_cfg["resources"]["port_ro"],
                            clock=q_cfg["resources"]["clock_ro"],
                        )
                    )

                    if q_cfg["resources"]["clock_ro"] not in schedule.resources.keys():
                        schedule.add_resources(
                            [
                                ClockResource(
                                    q_cfg["resources"]["clock_ro"],
                                    freq=q_cfg["params"]["ro_freq"],
                                )
                            ]
                        )

                if q_cfg["params"]["acquisition"] == "Trace":
                    # readout pulse
                    op.add_pulse(
                        SquarePulse(
                            amp=q_cfg["params"]["ro_pulse_amp"],
                            duration=q_cfg["params"]["ro_pulse_duration"],
                            port=q_cfg["resources"]["port_ro"],
                            clock=q_cfg["resources"]["clock_ro"],
                        )
                    )
                    op.add_acquisition(  # TODO protocol hardcoded
                        Trace(
                            duration=q_cfg["params"]["ro_acq_integration_time"],
                            t0=q_cfg["params"]["ro_acq_delay"],
                            acq_channel=op["gate_info"]["acq_channel"][idx],
                            acq_index=op["gate_info"]["acq_index"][idx],
                            port=q_cfg["resources"]["port_ro"],
                        )
                    )

                    if q_cfg["resources"]["clock_ro"] not in schedule.resources.keys():
                        schedule.add_resources(
                            [
                                ClockResource(
                                    q_cfg["resources"]["clock_ro"],
                                    freq=q_cfg["params"]["ro_freq"],
                                )
                            ]
                        )

        elif op["gate_info"]["operation_type"] == "Rxy":
            q = op["gate_info"]["qubits"][0]
            # read info from config
            q_cfg = device_cfg["qubits"][q]

            # G_amp is the gaussian amplitude introduced in
            # https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.103.110501
            # 180 refers to the normalization, theta is in degrees, and
            # mw_amp180 is the amplitude necessary to get the
            # maximum 180 degree theta (experimentally)
            G_amp = q_cfg["params"]["mw_amp180"] * op["gate_info"]["theta"] / 180
            D_amp = G_amp * q_cfg["params"]["mw_motzoi"]

            pulse = DRAGPulse(
                G_amp=G_amp,
                D_amp=D_amp,
                phase=op["gate_info"]["phi"],
                port=q_cfg["resources"]["port_mw"],
                duration=q_cfg["params"]["mw_duration"],
                clock=q_cfg["resources"]["clock_01"],
            )
            op.add_pulse(pulse)

            # add clock to resources
            if q_cfg["resources"]["clock_01"] not in schedule.resources.keys():
                schedule.add_resources(
                    [
                        ClockResource(
                            q_cfg["resources"]["clock_01"],
                            freq=q_cfg["params"]["mw_freq"],
                        )
                    ]
                )

        elif op["gate_info"]["operation_type"] == "CNOT":
            # These methods don't raise exceptions as they will be implemented shortly
            logging.warning("Not Implemented yet")
            logging.warning(
                'Operation type "{}" not supported by backend'.format(
                    op["gate_info"]["operation_type"]
                )
            )

        elif op["gate_info"]["operation_type"] == "CZ":
            # todo mock implementation, needs a proper version before release
            q0 = op["gate_info"]["qubits"][0]
            q1 = op["gate_info"]["qubits"][1]

            # this reflective edge is a unique property of the CZ gate
            try:
                edge_cfg = _find_edge(device_cfg, q0, q1, "CZ")
            except ValueError:
                try:
                    edge_cfg = _find_edge(device_cfg, q1, q0, "CZ")
                except ValueError:
                    raise

            amp = edge_cfg["params"]["flux_amp_control"]

            # FIXME: placeholder. currently puts a soft square pulse on the designated port of both qubits
            pulse = SoftSquarePulse(
                amp=amp,
                duration=edge_cfg["params"]["flux_duration"],
                port=edge_cfg["resource_map"][q0],
                clock=BasebandClockResource.IDENTITY,
            )
            op.add_pulse(pulse)

            pulse = SoftSquarePulse(
                amp=amp,
                duration=edge_cfg["params"]["flux_duration"],
                port=edge_cfg["resource_map"][q1],
                clock=BasebandClockResource.IDENTITY,
            )

            op.add_pulse(pulse)
        elif op["gate_info"]["operation_type"] == "reset":
            # Initialization through relaxation
            qubits = op["gate_info"]["qubits"]
            init_times = []
            for q in qubits:
                init_times.append(device_cfg["qubits"][q]["params"]["init_duration"])
            op.add_pulse(IdlePulse(max(init_times)))

        else:
            raise NotImplementedError(
                'Operation type "{}" not supported by backend'.format(
                    op["gate_info"]["operation_type"]
                )
            )

    return schedule


def validate_config(config: dict, scheme_fn: str) -> bool:
    """
    Validate a configuration using a schema.

    Parameters
    ----------
    config :
        The configuration to validate
    scheme_fn :
        The name of a json schema in the quantify.scheduler.schemas folder.

    Returns
    ----------
    :
        True if valid
    """
    scheme = load_json_schema(__file__, scheme_fn)
    jsonschema.validate(config, scheme)
    return True


def qcompile(
    schedule: Schedule, device_cfg: dict, hardware_mapping: dict = None, **kwargs
) -> Schedule:
    """
    Compile and assemble a schedule into deployables.

    Parameters
    ----------
    schedule :
        To be compiled
    device_cfg :
        Device specific configuration, defines the compilation step from
        the gate-level to the pulse level description.
    hardware_mapping:
        hardware mapping, defines the compilation step from
        the pulse-level to a hardware backend.

    Returns
    -------
    :
        The prepared schedule if no backend is provided, otherwise whatever object returned by the backend


    .. rubric:: Configuration specification

    .. jsonschema:: schemas/transmon_cfg.json

    .. todo::

        Add a schema for the hardware mapping.
    """
    schedule = device_compile(schedule=schedule, device_cfg=device_cfg)
    schedule = determine_absolute_timing(schedule=schedule, time_unit="physical")

    if hardware_mapping is not None:
        bck_name = hardware_mapping["backend"]
        # import the required backend callable to compile onto the backend
        (mod, cls) = bck_name.rsplit(".", 1)
        # compile using the appropriate hardware backend
        hardware_compile = getattr(importlib.import_module(mod), cls)
        # FIXME: still contains a hardcoded argument in the kwargs
        return hardware_compile(schedule, hardware_map=hardware_mapping, **kwargs)
    else:
        return schedule


def device_compile(schedule: Schedule, device_cfg: dict) -> Schedule:
    """
    Add pulse information to operations based on device config file.

    Parameters
    ----------
    schedule :
        To be compiled
    device_cfg :
        Device specific configuration, defines the compilation step from
        the gate-level to the pulse level description.

    Returns
    -------
    :
        The updated schedule.
    """

    device_bck_name = device_cfg["backend"]
    (mod, cls) = device_bck_name.rsplit(".", 1)
    device_compilation_bck = getattr(importlib.import_module(mod), cls)

    schedule = device_compilation_bck(schedule=schedule, device_cfg=device_cfg)
    schedule = determine_absolute_timing(schedule=schedule, time_unit="physical")

    return schedule
