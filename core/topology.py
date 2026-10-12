from dataclasses import dataclass
import math
import random
from typing import Dict, List, Tuple
 
@dataclass
class Link:
    delay_ms: float = 10.0
    loss_prob: float = 0.0
    capacity: float = 1.0
    up: bool = True
 
class NetworkTopology:
    def __init__(self):
        self.nodes: Dict[str, Tuple[float, float]] = {}
        self.links: Dict[str, Dict[str, Link]] = {}
 
    def add_node(self, node_id: str, x: float = 0.0, y: float = 0.0):
        self.nodes[node_id] = (x, y)
        self.links.setdefault(node_id, {})
 
    def add_link(self, a: str, b: str, link: Link):
        if a not in self.nodes or b not in self.nodes:
            raise ValueError("Both nodes must exist before adding a link.")
        self.links[a][b] = link
        self.links[b][a] = Link(
            delay_ms=link.delay_ms,
            loss_prob=link.loss_prob,
            capacity=link.capacity,
            up=link.up,
        )
 
    def neighbors(self, node_id: str) -> List[str]:
        return [
            n for n, link in self.links.get(node_id, {}).items()
            if link.up
        ]
 
    def get_link(self, a: str, b: str) -> Link:
        return self.links[a][b]
 
    def set_link_status(self, a: str, b: str, up: bool):
        self.links[a][b].up = up
        self.links[b][a].up = up
 
    def set_node_status(self, node_id: str, up: bool):
        for neighbor in self.links.get(node_id, {}):
            self.links[node_id][neighbor].up = up
            self.links[neighbor][node_id].up = up
 
    @classmethod
    def random_geometric(cls, n=12, radius=0.42, seed=42):
        rng = random.Random(seed)
        topology = cls()
 
        for i in range(n):
            topology.add_node(f"N{i+1}", rng.random(), rng.random())
 
        ids = list(topology.nodes)
        for i, a in enumerate(ids):
            for b in ids[i+1:]:
                ax, ay = topology.nodes[a]
                bx, by = topology.nodes[b]
                distance = math.hypot(ax - bx, ay - by)
                if distance <= radius:
                    delay = round(5 + distance * 30, 2)
                    loss = round(rng.uniform(0.0, 0.08), 3)
                    topology.add_link(
                        a, b,
                        Link(delay_ms=delay, loss_prob=loss, capacity=1.0)
                    )
        return topology
