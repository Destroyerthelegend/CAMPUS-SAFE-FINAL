from core.packet import Priority
from core.topology import NetworkTopology, Link
from core.sim import Simulator
 
def build_demo_topology():
    topology = NetworkTopology()
 
    for node in ["N1", "N2", "N3", "N4", "N5"]:
        topology.add_node(node)
 
    # Primary route: N1 -> N2 -> N4
    topology.add_link("N1", "N2", Link(delay_ms=10, loss_prob=0.01))
    topology.add_link("N2", "N4", Link(delay_ms=12, loss_prob=0.01))
 
    # Alternate route: N1 -> N3 -> N5 -> N4
    topology.add_link("N1", "N3", Link(delay_ms=8, loss_prob=0.01))
    topology.add_link("N3", "N5", Link(delay_ms=9, loss_prob=0.01))
    topology.add_link("N5", "N4", Link(delay_ms=10, loss_prob=0.01))
 
    return topology
 
def main():
    topology = build_demo_topology()
    simulator = Simulator(topology, use_priority=True)
 
    print("===== CAMPUS-SAFE DEMO =====")
    print("Initial route:", simulator.router.get_route("N1", "N4"))
 
    packet = simulator.create_packet(
        "N1", "N4", Priority.CRITICAL, "SOS: Medical assistance required"
    )
    simulator.send(packet)
 
    print("\n--- Injecting failure: N2 goes down ---")
    simulator.inject_failure(node_id="N2")
    print("Recovered route:", simulator.router.get_route("N1", "N4"))
 
    packet2 = simulator.create_packet(
        "N1", "N4", Priority.CRITICAL, "SOS: Rerouted after node failure"
    )
    simulator.send(packet2)
 
    print("\n--- Sending different priority messages ---")
    for priority in [Priority.LOW, Priority.NORMAL, Priority.HIGH, Priority.CRITICAL]:
        p = simulator.create_packet(
            "N1", "N4", priority, f"Test message: {priority.name}"
        )
        simulator.send(p)
 
    simulator.print_summary()
 
if __name__ == "__main__":
    main()
