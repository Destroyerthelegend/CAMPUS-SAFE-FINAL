from .topology import NetworkTopology
from .routing import DijkstraRouter
 
class FailureManager:
    def __init__(self, topology: NetworkTopology, router: DijkstraRouter):
        self.topology = topology
        self.router = router
 
    def fail_node(self, node_id: str):
        self.topology.set_node_status(node_id, False)
        self.router.invalidate_and_recompute()
 
    def recover_node(self, node_id: str):
        self.topology.set_node_status(node_id, True)
        self.router.invalidate_and_recompute()
 
    def fail_link(self, a: str, b: str):
        self.topology.set_link_status(a, b, False)
        self.router.invalidate_and_recompute()
 
    def recover_link(self, a: str, b: str):
        self.topology.set_link_status(a, b, True)
        self.router.invalidate_and_recompute()
