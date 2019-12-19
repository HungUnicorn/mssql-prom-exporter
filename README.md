# mssql-prom-exporter
MSSQL Exporter for Prometheus in python. Metrics are scraped by scheduler, and the interval is configurable via environment variable


## Integration
Run `docker-compose up`. When the image is not build yet, please run `docker-compose up --build`

After launching up, metrics show up in `http://localhost:8000/metrics/prometheus`,
by using promql `{__name__=~".+",app="prometheus-mssql-exporter"}`
[Existing metrics](https://github.com/HungUnicorn/mssql-prom-exporter#existing-metrics)

You can also find metrics in `http://localhost:9090/` in prometheus UI.

To rebuild the image please run `docker-compose up --build`

The default SQL Server is local. If wanted to test with real data, it has to
either pull the data from production or pointing the SQL Server connection to the production one

## Setting up

##### Initialize a virtual environment

Windows:
```
$ python3 -m venv venv
$ venv\Scripts\activate.bat
```

Unix/MacOS:
```
$ python3 -m venv venv
$ source venv/bin/activate
```
Learn more in [the documentation](https://docs.python.org/3/library/venv.html#creating-virtual-environments).

Note: if you are using a python before 3.3, it doesn't come with venv. Install [virtualenv](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv) with pip instead.

##### (If you're on a Mac) Make sure xcode tools are installed

```
$ xcode-select --install
```

##### Install the dependencies

```
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Set Environment Variables

Please check `config.py`. `config.py` describes the environment, and
by setting `FLASK_CONFIG`  you can decide which environment to pick up, e.g.

`FLASK_CONFIG=config.TestingConfig`

or

`FLASK_CONFIG=config.DevelopmentConfig`

or

`FLASK_CONFIG=config.ProductionConfig`

## Running the app

```
$ source env/bin/activate
$ python3 manage.py runserver
```

## Development
Add new Metrics by extending `AbstractMetric`,
under `app/prom/metrics`, either `general`, which is related to system
or `business` that is related to business logic.

Check existing [examples](https://github.com/HungUnicorn/mssql-prom-exporter/tree/master/app/prom/metrics/general)
and the [tests](https://github.com/HungUnicorn/mssql-prom-exporter/tree/master/tests/prom/metrics/general) before adding them.

Before implementing a metric please go through the tips that ensure you
follow the [official guideline](https://prometheus.io/docs/practices/instrumentation/#things-to-watch-out-for)

In general the rules are:
#### Labels
- Use labels when required to aggregate the metrics, e.g. http status code should be one metrics with several labels(200, 400, 500)
- Do not use labels when cardinality is more than 100 and will increase more in the future

#### Existing metrics
```
# HELP mssql_batch_requests Number of Transact-SQL command batches received per second.\n            This statistic is affected by all constraints (such as I/O, number of users, cachesize, \n            complexity of requests, and so on). High batch requests mean good throughput
# TYPE mssql_batch_requests gauge
mssql_batch_requests 1.25149e+02
# HELP mssql_connections Number of connections
# TYPE mssql_connections gauge
mssql_connections{database="master",state="current"} 17.0
# HELP mssql_deadlocks Number of lock requests per second that resulted in a deadlock since last restart
# TYPE mssql_deadlocks gauge
mssql_deadlocks 4.0
# HELP mssql_io_stall Wait time (ms) of stall since last restart
# TYPE mssql_io_stall gauge
mssql_io_stall{database="master",type="stall_read"} 38.0
mssql_io_stall{database="master",type="stall_write"} 16.0
mssql_io_stall{database="master",type="stall_queued_read"} 0.0
mssql_io_stall{database="master",type="stall_queued_write"} 0.0
# HELP mssql_io_stall_total Wait time (ms) of stall since last restart
# TYPE mssql_io_stall_total gauge
mssql_io_stall_total{database="master"} 14.0
# HELP mssql_kill_connection_errors Number of kill connection errors/sec since last restart
# TYPE mssql_kill_connection_errors gauge
mssql_kill_connection_errors 0.0
# HELP mssql_page_fault_count Number of page faults since last restart
# TYPE mssql_page_fault_count gauge
mssql_page_fault_count 1.92751391e+02
# HELP mssql_memory_utilization_percentage Percentage of memory utilization
# TYPE mssql_memory_utilization_percentage gauge
mssql_memory_utilization_percentage 100.0
# HELP mssql_total_physical_memory_kb Total physical memory in KB
# TYPE mssql_total_physical_memory_kb gauge
mssql_total_physical_memory_kb 1.6830676e+02
# HELP mssql_available_physical_memory_kb Available physical memory in KB
# TYPE mssql_available_physical_memory_kb gauge
mssql_available_physical_memory_kb 1.7805416e+02
# HELP mssql_total_page_file_kb Total page file in KB
# TYPE mssql_total_page_file_kb gauge
mssql_total_page_file_kb 1.08152648e+01
# HELP mssql_available_page_file_kb Available page file in KB
# TYPE mssql_available_page_file_kb gauge
mssql_available_page_file_kb 1.745982e+02
# HELP mssql_user_errors Number of user errors/sec since last restart
# TYPE mssql_user_errors gauge
mssql_user_errors 3.0
# HELP up UP status
# TYPE up gauge
up 1.0
```
