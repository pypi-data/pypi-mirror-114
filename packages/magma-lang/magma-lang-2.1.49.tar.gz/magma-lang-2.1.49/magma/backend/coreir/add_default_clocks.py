from magma.array import Array
from magma.clock import ClockTypes
from magma.clock_io import DefaultClockNameMap
from magma.interface import IO
from magma.passes.passes import DefinitionPass, pass_lambda
from magma.wire_clock import (wire_default_clock, get_default_clocks,
                              DefaultClockResult)
from magma.t import In
from magma.tuple import Tuple


def _lift_if_undriven_clock(port, default_clocks, defn):
    if port.is_mixed():
        return _lift_if_undriven_clock(port, clocks, defn)
    if port.is_input() and port.trace() is None:
        if (isinstance(port, ClockTypes) and
                default_clocks[type(port).undirected_t] is
                DefaultClockResult.None_):
            clock_t = type(port).undirected_t
            default_name = DefaultClockNameMap[clock_t]
            counter = 0
            while default_name in defn.interface.ports.keys():
                # in case the name is in use, but that would be strange
                default_name = f"{default_name}_{counter}"
                counter += 1
            with defn.open():
                defn.io += IO(default_name=In(clock_t))
            default_clocks[clock_t] = getattr(defn.io, default_name)
        elif isinstance(port, Array):
            # Only need to visit the first since they're all the same type and
            # can share a default
            _lift_if_undriven_clock(port[0], clocks, defn)
        elif isinstance(port, Tuple):
            for elem in port:
                _lift_if_undriven_clock(elem, clocks, defn)


def _lift_undriven_clocks(interface, default_clocks, defn):
    for port in interface.ports.values():
        _lift_if_undriven_clock(port, default_clocks, defn)


class AddDefaultClocks(DefinitionPass):
    def __call__(self, definition):
        definition.default_clocks = get_default_clocks(definition)

        for inst in definition.instances:
            _lift_undriven_clocks(inst.interface, definition.default_clocks,
                                  definition)


add_default_clocks = pass_lambda(AddDefaultClocks)
