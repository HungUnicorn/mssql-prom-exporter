from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric

TOTAL_MEM = '''total_mem'''
AVAILABLE_MEM = '''available_mem'''
TOTAL_PAGE = '''total_page'''
AVAILABLE_PAGE = '''available_page'''


class OsSysMemory(AbstractMetric):
    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.total_mem_metric = Gauge('mssql_total_physical_memory_kb',
                                      '''Total physical memory in KB''',
                                      registry=registry)
        self.available_mem_metric = Gauge(
            'mssql_available_physical_memory_kb',
            '''Available physical memory in KB''',
            registry=registry)
        self.total_page_metric = Gauge('mssql_total_page_file_kb',
                                       '''Total page file in KB''',
                                       registry=registry)
        self.available_page_metric = Gauge('mssql_available_page_file_kb',
                                           '''Available page file in KB''',
                                           registry=registry)

        self.query = '''
        SELECT total_physical_memory_kb as %s, available_physical_memory_kb as %s, 
        total_page_file_kb as %s, available_page_file_kb as %s 
        from sys.dm_os_sys_memory
        ''' % (TOTAL_MEM, AVAILABLE_MEM, TOTAL_PAGE, AVAILABLE_PAGE)

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        row = next(rows)
        self.total_mem_metric.set(row[TOTAL_MEM])
        self.available_mem_metric.set(row[AVAILABLE_MEM])
        self.total_page_metric.set(row[TOTAL_PAGE])
        self.available_page_metric.set(row[AVAILABLE_PAGE])
