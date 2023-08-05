from typing import List

from phidl.device_layout import Label

from pp.add_labels import get_input_label
from pp.component import ComponentReference
from pp.port import Port
from pp.types import Layer


def get_input_labels(
    io_gratings: List[ComponentReference],
    ordered_ports: List[Port],
    component_name: str,
    layer_label: Layer,
    gc_port_name: str,
) -> List[Label]:
    """Returns list of labels for a list of grating coupler references.

    Args:
        io_gratings: grating coupler references
        ordered_ports: list of ordered_ports
        component_name:
        layer_label:
        gc_port_name: gc_port_name port name
    """
    elements = []
    for i, g in enumerate(io_gratings):
        label = get_input_label(
            port=ordered_ports[i],
            gc=g,
            gc_index=i,
            component_name=component_name,
            layer_label=layer_label,
            gc_port_name=gc_port_name,
        )
        elements += [label]

    return elements
