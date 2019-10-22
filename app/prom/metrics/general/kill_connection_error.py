from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric

TOTAL_COUNT = '''total_count'''


class KillConnectionError(AbstractMetric):
    def __init__(self, registry):
        """
        Initialize query and metrics
        """

        self.metric = Gauge(
            'mssql_kill_connection_errors',
            'Number of kill connection errors/sec since last restart',
            registry=registry)
        self.query = '''
        SELECT cntr_value as %s
        FROM sys.dm_os_performance_counters
        where counter_name = 'Errors/sec' AND instance_name = 'Kill Connection Errors'
        ''' % TOTAL_COUNT

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        self.metric.set(next(rows)[TOTAL_COUNT])
