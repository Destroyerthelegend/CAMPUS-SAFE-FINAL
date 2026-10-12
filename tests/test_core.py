
import pytest

from core.packet import Packet, Priority
from core.topology import Link, NetworkTopology
from core.routing import DijkstraRouter
from core.failure import FailureManager


def build_network():
    topology = NetworkTopology()

    for node in ["N1", "N2", "N3", "N4"]:
        topology.add_node(node)

    topology.add_link("N1", "N2", Link(delay_ms=5))
    topology.add_link("N2", "N4", Link(delay_ms=5))
    topology.add_link("N1", "N3", Link(delay_ms=10))
    topology.add_link("N3", "N4", Link(delay_ms=10))

    return topology


def test_packet_priority_values():
    assert Priority.LOW == 1
    assert Priority.NORMAL == 2
    assert Priority.HIGH == 3
    assert Priority.CRITICAL == 4


def test_packet_tracks_hops():
    packet = Packet(
        src="N1",
        dst="N4",
        msg_id="TEST-001",
        priority=Priority.CRITICAL,
        ttl=5,
        payload="Emergency",
    )

    packet.add_hop("N2")

    assert packet.hop_list == ["N2"]


def test_packet_expires_when_ttl_is_zero():
    packet = Packet(
        src="N1",
        dst="N4",
        msg_id="TEST-002",
        priority=Priority.HIGH,
        ttl=0,
        payload="Test",
    )

    assert packet.expired()


def test_packet_forwarding_decrements_ttl():
    packet = Packet(
        src="N1",
        dst="N4",
        msg_id="TEST-003",
        priority=Priority.NORMAL,
        ttl=3,
        payload="Test",
    )

    packet.forward("N2")

    assert packet.ttl == 2
    assert packet.hop_list == ["N2"]


def test_links_are_bidirectional():
    topology = build_network()

    assert "N2" in topology.neighbors("N1")
    assert "N1" in topology.neighbors("N2")


def test_router_selects_shortest_path():
    topology = build_network()
    router = DijkstraRouter(topology)

    assert router.shortest_path("N1", "N4") == [
        "N1", "N2", "N4"
    ]


def test_router_returns_none_for_unreachable_node():
    topology = NetworkTopology()
    topology.add_node("N1")
    topology.add_node("N2")

    router = DijkstraRouter(topology)

    assert router.shortest_path("N1", "N2") is None


def test_router_uses_alternate_path_after_node_failure():
    topology = build_network()
    router = DijkstraRouter(topology)
    failure_manager = FailureManager(topology, router)

    assert router.shortest_path("N1", "N4") == [
        "N1", "N2", "N4"
    ]

    failure_manager.fail_node("N2")

    assert router.shortest_path("N1", "N4") == [
        "N1", "N3", "N4"
    ]


def test_failed_link_is_not_used():
    topology = build_network()
    router = DijkstraRouter(topology)
    failure_manager = FailureManager(topology, router)

    failure_manager.fail_link("N1", "N2")

    path = router.shortest_path("N1", "N4")

    assert path == ["N1", "N3", "N4"]
