from typing import Optional
from .packet import Packet
 
class RouterInterface:
    def next_hop(self, source: str, destination: str) -> Optional[str]:
        raise NotImplementedError
 
class QueueInterface:
    def enqueue(self, packet: Packet, current_time: float) -> bool:
        raise NotImplementedError
 
    def dequeue(self, current_time: float) -> Optional[Packet]:
        raise NotImplementedError
 
class ChannelInterface:
    def transmit(self, packet: Packet, source: str, destination: str) -> bool:
        raise NotImplementedError
