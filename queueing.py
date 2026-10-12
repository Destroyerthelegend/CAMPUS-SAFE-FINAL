from collections import deque
from typing import Optional
from .packet import Packet, Priority
 
class PriorityQueue:
    def __init__(self, capacity: int = 20, aging_seconds: float = 10.0):
        self.capacity = capacity
        self.aging_seconds = aging_seconds
        self._items = deque()
 
    def __len__(self):
        return len(self._items)
 
    def enqueue(self, packet: Packet, current_time: float) -> bool:
        if len(self._items) < self.capacity:
            self._items.append((packet, current_time))
            return True
 
        # If full, drop the lowest-priority packet when the new packet is higher.
        lowest_index = min(
            range(len(self._items)),
            key=lambda i: self._effective_priority(self._items[i][0], self._items[i][1], current_time)
        )
        lowest_packet, _ = self._items[lowest_index]
 
        if packet.priority > lowest_packet.priority:
            del self._items[lowest_index]
            self._items.append((packet, current_time))
            return True
 
        return False
 
    def _effective_priority(self, packet: Packet, queued_at: float, now: float) -> int:
        age_bonus = int(max(0.0, now - queued_at) // self.aging_seconds)
        return min(int(Priority.CRITICAL), int(packet.priority) + age_bonus)
 
    def dequeue(self, current_time: float) -> Optional[Packet]:
        if not self._items:
            return None
 
        best_index = max(
            range(len(self._items)),
            key=lambda i: self._effective_priority(
                self._items[i][0], self._items[i][1], current_time
            )
        )
        packet, _ = self._items[best_index]
        del self._items[best_index]
        return packet
 
    def items(self):
        return [packet for packet, _ in self._items]
 
class FIFOQueue:
    def __init__(self, capacity: int = 20):
        self.capacity = capacity
        self._items = deque()
 
    def __len__(self):
        return len(self._items)
 
    def enqueue(self, packet: Packet, current_time: float) -> bool:
        if len(self._items) >= self.capacity:
            return False
        self._items.append((packet, current_time))
        return True
 
    def dequeue(self, current_time: float) -> Optional[Packet]:
        if not self._items:
            return None
        packet, _ = self._items.popleft()
        return packet
