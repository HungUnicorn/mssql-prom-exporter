from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.batch_request import BatchRequest, TOTAL_COUNT


class TestBatchRequest(TestCase):

    def test_should_collect(self):
        test_data = {TOTAL_COUNT: 100}

        batch_request = BatchRequest(CollectorRegistry())

        batch_request.collect(rows=(_ for _ in [test_data]))

        samples = next(iter(batch_request.metric.collect())).samples

        self.assertEqual(test_data[TOTAL_COUNT], next(iter(samples)).value)
