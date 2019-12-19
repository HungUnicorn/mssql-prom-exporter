from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.io_stall import IOStall, NAME, READ, WRITE, STALL, QUEUED_READ, QUEUED_WRITE


def test_should_collect():
    test_data_1 = {NAME: 'test_1', READ: 300, WRITE: 100, STALL: 500, QUEUED_READ: 100, QUEUED_WRITE: 100}
    test_data_2 = {NAME: 'test_2', READ: 3, WRITE: 1, STALL: 5, QUEUED_READ: 1, QUEUED_WRITE: 1}

    io_stall = IOStall(CollectorRegistry())

    io_stall.collect(rows=(_ for _ in [test_data_1, test_data_2]))

    samples = next(iter(io_stall.metric.collect())).samples
    iter_samples = iter(samples)

    assert_sample_metric(iter_samples, test_data_1, READ)
    assert_sample_metric(iter_samples, test_data_1, WRITE)
    assert_sample_metric(iter_samples, test_data_1, QUEUED_READ)
    assert_sample_metric(iter_samples, test_data_1, QUEUED_WRITE)
    assert_sample_metric(iter_samples, test_data_2, READ)
    assert_sample_metric(iter_samples, test_data_2, WRITE)
    assert_sample_metric(iter_samples, test_data_2, QUEUED_READ)
    assert_sample_metric(iter_samples, test_data_2, QUEUED_WRITE)

    samples = next(iter(io_stall.metric_total.collect())).samples
    iter_samples = iter(samples)
    assert_sample_metric_total(iter_samples, test_data_1)
    assert_sample_metric_total(iter_samples, test_data_2)


def assert_sample_metric(iter_samples, test_data, stall_type):
    sample = next(iter_samples)
    assert test_data[stall_type] == sample.value
    assert test_data[NAME] == sample.labels['database']


def assert_sample_metric_total(iter_samples, test_data_1):
    sample = next(iter_samples)
    assert test_data_1[STALL] == sample.value
    assert test_data_1[NAME] == sample.labels['database']
