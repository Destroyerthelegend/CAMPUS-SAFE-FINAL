import heapq
from typing import Dict, List, Optional, Tuple
from .topology import NetworkTopology
 
class DijkstraRouter:
    def __init__(self, topology: NetworkTopology):
        self.topology = topology
        self.route_tables: Dict[str, Dict[str, str]] = {}
        self.recompute_all()
 
    def edge_cost(self, a: str, b: str) -> float:
        link = self.topology.get_link(a, b)
        # Delay is the main routing cost; loss is a small penalty.
        return link.delay_ms * (1.0 + link.loss_prob)
 
    def shortest_path(self, source: str, destination: str) -> Optional[List[str]]:
        if source not in self.topology.nodes or destination not in self.topology.nodes:
            return None
 
        distances = {node: float("inf") for node in self.topology.nodes}
        previous = {}
        distances[source] = 0.0
        heap = [(0.0, source)]
 
        while heap:
            distance, current = heapq.heappop(heap)
            if distance != distances[current]:
                continue
            if current == destination:
                break
 
            for neighbor in self.topology.neighbors(current):
                new_distance = distance + self.edge_cost(current, neighbor)
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current
                    heapq.heappush(heap, (new_distance, neighbor))
 
        if distances[destination] == float("inf"):
            return None
 
        path = []
        current = destination
        while current != source:
            path.append(current)
            current = previous[current]
        path.append(source)
        path.reverse()
        return path
 
    def recompute_all(self):
        self.route_tables = {}
        for source in self.topology.nodes:
            table = {}
            for destination in self.topology.nodes:
                if source == destination:
                    continue
                path = self.shortest_path(source, destination)
                if path and len(path) >= 2:
                    table[destination] = path[1]
            self.route_tables[source] = table
 
    def invalidate_and_recompute(self):
        self.recompute_all()
 
    def next_hop(self, source: str, destination: str) -> Optional[str]:
        if source not in self.route_tables:
            self.recompute_all()
        return self.route_tables.get(source, {}).get(destination)
 
    def get_route(self, source: str, destination: str) -> Optional[List[str]]:
        return self.shortest_path(source, destination)
