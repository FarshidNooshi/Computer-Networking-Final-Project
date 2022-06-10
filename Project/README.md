<div align="center">
    <h1>In The Name of GOD</h1>
</div>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Computer Networking Project

The final project of Computer Network course at the Amirkabir University of Technology. The project is the
implementation of a monitoring prometheus metric client that receive metrics from different agent programs and merge
them in prometheus metrics and expose them for Prometheus Scraper.

## What is Prometheus?

Prometheus is an open-source systems monitoring and alerting toolkit originally built at SoundCloud. Since its inception
in 2012, many companies and organizations have adopted Prometheus, and the project has a very active developer and user
community. It is now a standalone open source project and maintained independently of any company. To emphasize this,
and to clarify the project's governance structure, Prometheus joined the Cloud Native Computing Foundation in 2016 as
the second hosted project, after Kubernetes.\
Prometheus collects and stores its metrics as time series data, i.e. metrics information is stored with the timestamp at
which it was recorded, alongside optional key-value pairs called labels.

# Requirements

the following requirements are needed for the project:

```
psutil
colorama
setuptools
prometheus-client
```

you should also download and install the prometheus for your system from the following link:\
<h6>
[Prometheus Download Page](https://prometheus.io/download/)
</h6>
For installation, you can run the following command:
> pip install -r requirements.txt

## How to run the project

1. replace the `Project/prometheus.yml` file with the `prometheus.yml` file of the one you downloaded from the link above.
2. run `prometheus` in your system.

3. inorder to run the project, you should run the following command in the `Project/src/Client` folder:
> python3 main.py

4. In a separate terminal, you should run the following command in the `Project/src/Server` folder:
> python3 main.py

# Metrics

I have implemented 5 metrics, but you can add more metrics by following the following steps:

1. Add the metrics name in `metrics` field in `Project/src/Business/json/data.json` data file.
2. Add the same metrics name in the `metrics` dictionary at the `create_metrics` method in the `client.py` file and give
   its value for each message to server.

 ```python
@staticmethod
def create_metrics():
    metrics = {
        'cpu_utilization_percent': psutil.cpu_percent(interval=1),
        'memory_available': psutil.virtual_memory().available,
        'num_bytes_sent': psutil.net_io_counters().bytes_sent,
        'num_errors_recv': psutil.net_io_counters().errin,
    }
    return metrics
 ```

3. Create the required metric at server side for handling in the `Project/src/Server/Utils/ClientHandler.py` file.
```python
def create_metrics(self):
    self.cpu = Gauge(f'cpu_utilization_percent', 'percentage of cpu usage right now.', labelnames=['client_name'])
    self.mem = Gauge(f'memory_available', 'available memory in bytes.', labelnames=['client_name'])
    self.net = Counter(f'network_usage_total', 'total number of received bytes.', labelnames=['client_name'])
    self.client_net = Counter(f'network_send_total', 'total number of send bytes.', labelnames=['client_name'])
    self.err_net = Counter(f'received_error_total', 'total number of errors while receiving.',
                           labelnames=['client_name'])
```
4. At the same file like 3 you should add the update instruction for each metric like below:
```python
def update_metrics(self, client_name, metrics, sz):
    self.cpu.labels(client_name=client_name).set(metrics['cpu_utilization_percent'])
    self.net.labels(client_name=client_name).inc(sz)
    self.mem.labels(client_name=client_name).set(metrics['memory_available'])
    self.client_net.labels(client_name=client_name).inc(metrics['num_bytes_sent'])
    self.err_net.labels(client_name=client_name).inc(metrics['num_errors_recv'])
```
5. done!

# Screenshots
![](https://i.imgur.com/XqQZQZL.png)

# Contributors
* Farshid Nooshi

