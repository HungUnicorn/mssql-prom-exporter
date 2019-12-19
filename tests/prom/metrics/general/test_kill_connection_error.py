from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.kill_connection_error import KillConnectionError, TOTAL_COUNT


def test_should_collect():
    test_data = {TOTAL_COUNT: 100}

    kill_connection_error = KillConnectionError(CollectorRegistry())

    kill_connection_error.collect(rows=(_ for _ in [test_data]))

    samples = next(iter(kill_connection_error.metric.collect())).samples

    assert test_data[TOTAL_COUNT] == next(iter(samples)).value
