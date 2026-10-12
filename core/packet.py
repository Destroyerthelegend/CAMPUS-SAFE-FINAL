from dataclasses import dataclass, field
from enum import IntEnum
from time import time
from typing import List
 
class Priority(IntEnum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4
 
@dataclass
class Packet:
    src: str
    dst: str
    msg_id: str
    priority: Priority
    ttl: int
    payload: str
    created_at: float = field(default_factory=time)
    hop_list: List[str] = field(default_factory=list)
    ack_required: bool = True
 
    def add_hop(self, node_id: str) -> None:
        self.hop_list.append(node_id)
 
    def expired(self) -> bool:
        return self.ttl <= 0
 
    def forward(self, node_id: str) -> None:
        self.ttl -= 1
        self.add_hop(node_id)
