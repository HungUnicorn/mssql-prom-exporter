from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.dead_lock import Deadlock, TOTAL_COUNT


def test_should_collect():
    test_data = {TOTAL_COUNT: 100}

    deadlock = Deadlock(CollectorRegistry())

    deadlock.collect(rows=(_ for _ in [test_data]))

    samples = next(iter(deadlock.metric.collect())).samples

    assert test_data[TOTAL_COUNT] == next(iter(samples)).value
