from dataclasses import dataclass
 
@dataclass
class MetricReport:
    generated: int
    delivered: int
    dropped: int
    pdr_percent: float
    average_delay_ms: float
    average_hops: float
    throughput_packets: int
 
def collect(simulator) -> MetricReport:
    m = simulator.metrics
    return MetricReport(
        generated=m.generated,
        delivered=m.delivered,
        dropped=m.dropped,
        pdr_percent=m.pdr() * 100,
        average_delay_ms=m.average_delay(),
        average_hops=m.average_hops(),
        throughput_packets=m.throughput(),
    )
