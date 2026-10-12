import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional
 
from .packet import Packet, Priority
from .topology import NetworkTopology
from .routing import DijkstraRouter
from .queueing import PriorityQueue, FIFOQueue
from .channel import Channel
from .failure import FailureManager
 
@dataclass
class SimulationMetrics:
    generated: int = 0
    delivered: int = 0
    dropped: int = 0
    total_delay_ms: float = 0.0
    total_hops: int = 0
    by_priority: Dict[str, Dict[str, float]] = field(default_factory=dict)
    recovery_events: List[float] = field(default_factory=list)
 
    def record_generated(self, priority: Priority):
        self.generated += 1
        key = priority.name
        self.by_priority.setdefault(key, {"generated": 0, "delivered": 0, "delay_ms": 0.0})
        self.by_priority[key]["generated"] += 1
 
    def record_delivery(self, packet: Packet, delay_ms: float):
        self.delivered += 1
        self.total_delay_ms += delay_ms
        self.total_hops += max(0, len(packet.hop_list) - 1)
        key = packet.priority.name
        self.by_priority.setdefault(key, {"generated": 0, "delivered": 0, "delay_ms": 0.0})
        self.by_priority[key]["delivered"] += 1
        self.by_priority[key]["delay_ms"] += delay_ms
 
    def record_drop(self):
        self.dropped += 1
 
    def pdr(self):
        return self.delivered / self.generated if self.generated else 0.0
 
    def throughput(self):
        return self.delivered
 
    def average_delay(self):
        return self.total_delay_ms / self.delivered if self.delivered else 0.0
 
    def average_hops(self):
        return self.total_hops / self.delivered if self.delivered else 0.0
 
class Simulator:
    def __init__(self, topology: NetworkTopology, use_priority=True, queue_capacity=20):
        self.topology = topology
        self.router = DijkstraRouter(topology)
        self.failure = FailureManager(topology, self.router)
        self.channel = Channel(topology)
        self.use_priority = use_priority
        self.queues = {
            node: (PriorityQueue(queue_capacity) if use_priority else FIFOQueue(queue_capacity))
            for node in topology.nodes
        }
        self.metrics = SimulationMetrics()
        self.clock_ms = 0.0
        self.packet_counter = 0
 
    def create_packet(self, src: str, dst: str, priority: Priority, payload: str, ttl=12):
        self.packet_counter += 1
        packet = Packet(
            src=src,
            dst=dst,
            msg_id=f"MSG-{self.packet_counter:04d}",
            priority=priority,
            ttl=ttl,
            payload=payload,
        )
        self.metrics.record_generated(priority)
        return packet
 
    def send(self, packet: Packet, verbose=True) -> bool:
        current = packet.src
        packet.add_hop(current)
 
        while current != packet.dst:
            if packet.expired():
                self.metrics.record_drop()
                if verbose:
                    print(f"{packet.msg_id}: TTL expired")
                return False
 
            next_hop = self.router.next_hop(current, packet.dst)
 
            if next_hop is None:
                self.metrics.record_drop()
                if verbose:
                    print(f"{packet.msg_id}: no route from {current} to {packet.dst}")
                return False
 
            result = self.channel.transmit(packet, current, next_hop)
            self.clock_ms += result.delay_ms
 
            if not result.success:
                self.metrics.record_drop()
                if verbose:
                    print(f"{packet.msg_id}: {result.reason} on {current}->{next_hop}")
                return False
 
            packet.forward(next_hop)
            current = next_hop
 
        delay = self.clock_ms - (packet.created_at * 1000.0 % 1000000)
        # Use deterministic simulation delay instead of wall-clock time.
        delay = sum(
            self.topology.get_link(packet.hop_list[i], packet.hop_list[i+1]).delay_ms
            for i in range(len(packet.hop_list) - 1)
        )
 
        self.metrics.record_delivery(packet, delay)
 
        if verbose:
            print(
                f"{packet.msg_id}: DELIVERED | "
                f"priority={packet.priority.name} | "
                f"route={' -> '.join(packet.hop_list)} | "
                f"delay={delay:.2f} ms | hops={len(packet.hop_list)-1}"
            )
        return True
 
    def inject_failure(self, node_id: Optional[str] = None, link=None):
        start = self.clock_ms
        if node_id:
            self.failure.fail_node(node_id)
        elif link:
            self.failure.fail_link(link[0], link[1])
        recovery_time = self.clock_ms - start
        self.metrics.recovery_events.append(recovery_time)
        return recovery_time
 
    def print_summary(self):
        print("\n===== CAMPUS-SAFE SIMULATION SUMMARY =====")
        print(f"Generated packets : {self.metrics.generated}")
        print(f"Delivered packets : {self.metrics.delivered}")
        print(f"Dropped packets   : {self.metrics.dropped}")
        print(f"Packet Delivery Ratio: {self.metrics.pdr()*100:.2f}%")
        print(f"Average delay     : {self.metrics.average_delay():.2f} ms")
        print(f"Average hops      : {self.metrics.average_hops():.2f}")
        print(f"Throughput        : {self.metrics.throughput()} packets")
        print("\nPriority-wise results:")
        for priority, values in self.metrics.by_priority.items():
            delay = values["delay_ms"] / values["delivered"] if values["delivered"] else 0
            print(
                f"{priority:10s} | generated={int(values['generated']):2d} "
                f"| delivered={int(values['delivered']):2d} | avg_delay={delay:.2f} ms"
            )
