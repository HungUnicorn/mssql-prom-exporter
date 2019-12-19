from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.os_proc_memory import OsProcessMemory, COUNT, PERCENTAGE


def test_should_collect():
    test_data = {COUNT: 100, PERCENTAGE: 90}

    os_process_memory = OsProcessMemory(CollectorRegistry())

    os_process_memory.collect(rows=(_ for _ in [test_data]))

    samples = next(iter(os_process_memory.count_metric.collect())).samples

    assert test_data[COUNT] == next(iter(samples)).value

    samples = next(iter(os_process_memory.percentage_metric.collect())).samples

    assert test_data[PERCENTAGE] == next(iter(samples)).value
