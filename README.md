# CAMPUS-SAFE

## Priority-Based Emergency Communication and Alert System Using Wireless Mesh Concepts

### 1. Project Overview

CAMPUS-SAFE is a Python-based network simulation that models priority-based emergency communication using wireless mesh networking concepts. It explores priority-based message handling, shortest-path routing, and route recovery when network nodes fail.

### 2. Objectives

- Simulate a wireless mesh network with nodes and communication links.
- Model messages with different priority levels.
- Select routes using shortest-path routing.
- Simulate node and link failures.
- Evaluate packet delivery, delay, and hop count.

### 3. Project Structure

- `core/` — Network topology, routing, failure handling, packets, queueing, channel, interfaces, and simulation modules.
- `experiments/` — Experiment runner and plotting scripts.
- `metrics/` — Performance metric collection.
- `tests/` — Automated tests.
- `docs/results/` — Review and testing evidence.

### 4. Running the Simulation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

From the repository root, run:

```bash
python -m experiments.run_experiment
```

### 5. Review 2 Baseline Results

The baseline simulation recorded:

- Packets generated: 6
- Packets delivered: 6
- Packets dropped: 0
- Packet delivery ratio: 100%
- Average delay: 26.17 ms
- Average hop count: 2.83

When node `N2` failed, the simulation demonstrated an alternate route from `N1` to `N4`.

These values describe the recorded simulation run and are not a guarantee of performance under all network conditions.

### 6. Testing

Automated tests cover packet priority and TTL handling, bidirectional links, shortest-path routing, unreachable destinations, alternate routing after node failure, and failed-link handling.

Run the tests using:

```bash
python -m pytest -v
```

### 7. Team Contributions

**Kavin**
- Network topology representation.
- Shortest-path routing.
- Node and link failure handling.
- Integration and testing.

**Prithvi**
- Priority queueing.
- Channel transmission simulation.
- Performance metrics.
- Experiment execution and plotting.

### 8. Limitations and Future Work

The current project is a software-based simulation. Results depend on the implemented model and test scenarios. Future work could include larger network experiments, more extensive performance comparisons, mobility support, and integration with physical wireless hardware.

### 9. Scope

CAMPUS-SAFE demonstrates networking concepts through simulation. It is not yet a deployed emergency communication system.
