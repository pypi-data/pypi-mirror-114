import pp
from pp.component import Component
from pp.components.bend_circular import bend_circular
from pp.components.extension import line
from pp.components.mmi1x2 import mmi1x2
from pp.components.mzi2x2 import mzi_arm
from pp.components.straight import straight as straight_function
from pp.components.straight_heater import straight_with_heater
from pp.port import select_electrical_ports
from pp.routing.route_ports_to_side import route_ports_to_side
from pp.types import ComponentFactory


@pp.cell
def mzi1x2(
    L0: float = 0.1,
    DL: float = 9.0,
    L2: float = 10.0,
    bend: ComponentFactory = bend_circular,
    straight_heater: ComponentFactory = straight_with_heater,
    straight: ComponentFactory = straight_function,
    coupler_function: ComponentFactory = mmi1x2,
    with_elec_connections: bool = False,
    waveguide="strip",
    **waveguide_settings
) -> Component:
    """Mzi 1x2

    Args:
        L0: vertical length for both and top arms
        DL: bottom arm extra length
        L2: L_top horizontal length
        bend_radius: 10.0
        bend: 90 degrees bend library
        straight_heater: straight_with_heater or straight
        straight_function: straight
        coupler_function: coupler

    .. code::

             __L2__
            |      |
            L0     L0
            |      |
          --|      |--
            |      |
            L0     L0
            |      |
            DL     DL
            |      |
            |__L2__|


             top_arm
        -CP1=       =CP2-
             bot_arm


    """
    if not with_elec_connections:
        straight_heater = straight

    cpl = coupler_function()

    arm_defaults = {
        "L_top": L2,
        "bend": bend,
        "straight_heater": straight_heater,
        "straight": straight,
        "with_elec_connections": with_elec_connections,
        "waveguide": waveguide,
    }

    arm_top = mzi_arm(L0=L0, **arm_defaults, **waveguide_settings)
    arm_bot = mzi_arm(L0=L0, DL=DL, **arm_defaults, **waveguide_settings)

    components = {
        "CP1": (cpl, "None"),
        "CP2": (cpl, "mirror_y"),
        "arm_top": (arm_top, "None"),
        "arm_bot": (arm_bot, "mirror_x"),
    }

    connections = [
        # Bottom arm
        ("CP1", "E0", "arm_bot", "W0"),
        ("arm_bot", "E0", "CP2", "E0"),
        # Top arm
        ("CP1", "E1", "arm_top", "W0"),
        ("arm_top", "E0", "CP2", "E0"),
    ]

    if with_elec_connections:
        ports_map = {
            "W0": ("CP1", "W0"),
            "E0": ("CP2", "W0"),
            "E_TOP_0": ("arm_top", "E_0"),
            "E_TOP_1": ("arm_top", "E_1"),
            "E_TOP_2": ("arm_top", "E_2"),
            "E_TOP_3": ("arm_top", "E_3"),
            "E_BOT_0": ("arm_bot", "E_0"),
            "E_BOT_1": ("arm_bot", "E_1"),
            "E_BOT_2": ("arm_bot", "E_2"),
            "E_BOT_3": ("arm_bot", "E_3"),
        }

        component = pp.component_from.netlist(components, connections, ports_map)
        # Need to connect common ground and redefine electrical ports

        ports = component.ports
        y_elec = ports["E_TOP_0"].y
        for ls, le in [
            ("E_BOT_0", "E_BOT_1"),
            ("E_TOP_0", "E_TOP_1"),
            ("E_BOT_2", "E_TOP_2"),
        ]:
            component.add_polygon(line(ports[ls], ports[le]), layer=ports[ls].layer)

        # Add GND ("E_BOT_2", "E_TOP_2")
        component.add_port(
            name="GND",
            midpoint=0.5 * (ports["E_BOT_2"].midpoint + ports["E_TOP_2"].midpoint),
            orientation=180,
            width=ports["E_BOT_2"].width,
            layer=ports["E_BOT_2"].layer,
        )

        component.ports["E_TOP_3"].orientation = 0
        component.ports["E_BOT_3"].orientation = 0

        # Remove the eletrical ports that we have just used internally
        for lbl in ["E_BOT_0", "E_BOT_1", "E_TOP_0", "E_TOP_1", "E_BOT_2", "E_TOP_2"]:
            component.ports.pop(lbl)

        # Reroute electrical ports
        _e_ports = select_electrical_ports(component)
        routes, e_ports = route_ports_to_side(
            _e_ports, side="north", y=y_elec, radius=2
        )

        for route in routes:
            component.add(route.references)

        for p in e_ports:
            component.ports[p.name] = p

        # Create nice electrical port names
        component.ports["HT1"] = component.ports["E_TOP_3"]
        component.ports.pop("E_TOP_3")

        component.ports["HT2"] = component.ports["E_BOT_3"]
        component.ports.pop("E_BOT_3")

    else:
        ports_map = {"W0": ("CP1", "W0"), "E0": ("CP2", "W0")}
        component = pp.component_from.netlist(components, connections, ports_map)

    return component


if __name__ == "__main__":
    # c = mzi1x2(coupler_function=mmi1x2, with_elec_connections=False)
    c = mzi1x2(coupler_function=mmi1x2, L0=10, with_elec_connections=True)
    # print(c.ports)
    c.show()
    # print(c.get_settings())
