"""Initialize prom"""

from prometheus_client import Gauge
from prometheus_client.registry import CollectorRegistry

from app.prom.collector import Collector
from app.prom.metrics.abstract_metric import AbstractMetric


class PromInitializer:
    """
    Initialize prom that should be used during app creation and shared in flask context(current_app)
    """
    def __init__(self):
        self.registry = CollectorRegistry()

        self.metrics = [
            obj(self.registry) for obj in AbstractMetric.__subclasses__()
        ]

        assert len(
            self.metrics) != 0, "At least one metric should be initialized"

        # Prometheus setup
        self.up_gauge = Gauge('up', 'UP status', registry=self.registry)
        self.collector = Collector(self.metrics)
