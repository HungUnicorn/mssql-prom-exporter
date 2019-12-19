from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.connection import Connection, DATABASE_NAME, CONNECTION_COUNT


def test_should_collect():
    connection = Connection(CollectorRegistry())
    test_data_1 = {DATABASE_NAME: 'test_1', CONNECTION_COUNT: 300}
    test_data_2 = {DATABASE_NAME: 'test_2', CONNECTION_COUNT: 1}

    connection.collect(rows=(_ for _ in [test_data_1, test_data_2]))

    samples = next(iter(connection.metric.collect())).samples
    iter_samples = iter(samples)

    assert_sample(iter_samples, test_data_1)
    assert_sample(iter_samples, test_data_2)


def assert_sample(iter_samples, test_data):
    sample = next(iter_samples)
    assert test_data[CONNECTION_COUNT] == sample.value
    assert test_data[DATABASE_NAME] == sample.labels['database']
    assert 'current' == sample.labels['state']
