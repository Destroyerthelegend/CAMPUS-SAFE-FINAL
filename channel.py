import random
from dataclasses import dataclass
from .packet import Packet
from .topology import NetworkTopology
 
@dataclass
class TransmissionResult:
    success: bool
    delay_ms: float
    reason: str = ""
 
class Channel:
    def __init__(self, topology: NetworkTopology, seed: int = 42):
        self.topology = topology
        self.rng = random.Random(seed)
 
    def transmit(self, packet: Packet, source: str, destination: str) -> TransmissionResult:
        link = self.topology.get_link(source, destination)
 
        if not link.up:
            return TransmissionResult(False, 0.0, "LINK_DOWN")
 
        if self.rng.random() < link.loss_prob:
            return TransmissionResult(False, link.delay_ms, "PACKET_LOSS")
 
        return TransmissionResult(True, link.delay_ms, "DELIVERED")
