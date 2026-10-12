# CAMPUS-SAFE
### Priority-Based Emergency Communication and Alert System Using a Wireless Mesh Network

## 1. Project Overview
CAMPUS-SAFE is a Python-based network simulation project that models an emergency communication system using a wireless mesh topology. It explores priority-based message handling, shortest-path routing, and route recovery when network nodes fail.

## 2. Objectives
- Simulate a wireless mesh network with nodes and communication links.
- Model messages with different priority levels.
- Select routes using shortest-path routing.
- Simulate node and link failures.
- Evaluate packet delivery, delay, and hop count.

## 3. Project Structure

- `core/` — Network topology, routing, failure handling, packets, queueing, channel, interfaces, and simulation modules.
- `experiments/` — Experiment runner and plotting scripts.
- `metrics/` — Performance metric collection.

## 4. Running the Simulation

From the repository root, run:

```bash
python experiments/run_experiment.py
```

Install any required dependencies listed in `requirements.txt` before execution.

## 5. Review 2 Baseline Demonstration

The baseline simulation demonstrated route selection and recovery after a node failure.

- Initial route: `N1 → N2 → N4`
- After node N2 failed: `N1 → N3 → N5 → N4`

### Baseline Results

| Metric | Result |
|---|---:|
| Packets generated | 6 |
| Packets delivered | 6 |
| Packets dropped | 0 |
| Packet Delivery Ratio | 100% |
| Average delay | 26.17 ms |
| Average hops | 2.83 |

These values represent one simulation run and do not guarantee the same performance under all network conditions.

## 6. Testing and Results

Testing should cover route selection, message delivery, node-failure recovery, supported priority levels, and metric calculations. Record actual test results and final Review 3 outputs after executing the implementation.

## 7. Current Scope and Limitations

The project focuses on software-based network simulation. The results do not establish real-world wireless performance or physical hardware validation.

Distributed UDP communication, a live dashboard, database storage, mobility, store-and-forward behaviour, and ESP32/LoRa integration should be described as implemented only if they are present and verified in the submitted code. Otherwise, they remain potential future extensions.

## 8. Future Work

Potential extensions include distributed communication, additional failure scenarios, repeated performance experiments, improved visualization, persistent result storage, and physical hardware validation.

## 9. Team Contributions

- **Kavin (24BCE2722):** Network topology, routing, failure recovery, and related integration/testing.
- **Prithvi (24BCE2778):** Queueing, channel modelling, metric collection, and experiments.

## 10. Repository

Source code, experiment scripts, and supporting documentation are maintained in this repository.
