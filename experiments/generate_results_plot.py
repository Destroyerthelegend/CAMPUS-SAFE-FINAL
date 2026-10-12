
import matplotlib.pyplot as plt

from experiments.run_experiment import build_demo_topology
from core.sim import Simulator
from core.packet import Priority


def main():
    topology = build_demo_topology()
    simulator = Simulator(topology, use_priority=True)

    # Match the experiment runner's packet sequence.
    packet = simulator.create_packet(
        "N1", "N4", Priority.CRITICAL,
        "SOS: Medical assistance required"
    )
    simulator.send(packet)

    simulator.inject_failure(node_id="N2")

    packet2 = simulator.create_packet(
        "N1", "N4", Priority.CRITICAL,
        "SOS: Rerouted after node failure"
    )
    simulator.send(packet2)

    for priority in [
        Priority.LOW,
        Priority.NORMAL,
        Priority.HIGH,
        Priority.CRITICAL,
    ]:
        p = simulator.create_packet(
            "N1", "N4", priority,
            f"Test message: {priority.name}"
        )
        simulator.send(p)

    metrics = simulator.metrics
    results = {}

    for priority, values in metrics.by_priority.items():
        delivered = values["delivered"]
        if delivered:
            results[priority] = values["delay_ms"] / delivered

    if not results:
        raise RuntimeError("No delivered packets to plot.")

    labels = list(results.keys())
    delays = list(results.values())

    plt.figure(figsize=(8, 5))
    plt.bar(labels, delays)
    plt.xlabel("Priority")
    plt.ylabel("Average end-to-end delay (ms)")
    plt.title("CAMPUS-SAFE: Measured Delay by Priority")
    plt.tight_layout()
    plt.savefig("docs/results/review3_priority_delay.png", dpi=200)
    plt.show()


if __name__ == "__main__":
    main()
