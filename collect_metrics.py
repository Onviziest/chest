"""
Collect containers' metrics from Prometheus.

Usage:
1. Install `matplotlib`
2. Change the IP and the port in `prometheus_url` of `config`
3. Create `metrics` directory
"""

from __future__ import annotations

import time
from datetime import datetime

from multiprocessing import Process
from requests import get
import matplotlib.pyplot as plt

config = dict(
    prometheus_url='http://192.168.1.183:9090/api/v1/query_range',
    # 容器的 CPU 使用率
    cpu_usage_query='sum(irate(container_cpu_usage_seconds_total{image!="", image!="google/cadvisor:latest"}[5s])) without (cpu)',
    # 查询容器内存使用量（单位：字节）
    memory_usage_query='container_memory_usage_bytes{image!="", image!="google/cadvisor:latest"}',
    # 查询容器网络接收量速率（单位：字节/秒）
    network_receive_query='sum(rate(container_network_receive_bytes_total{image!="", image!="google/cadvisor:latest"}[5s])) without (interface)',
    # 查询容器网络传输量速率（单位：字节/秒）
    network_transmit_query='sum(rate(container_network_transmit_bytes_total{image!="", image!="google/cadvisor:latest"}[5s])) without (interface)',
    # 查询容器文件系统读取速率（单位：字节/秒）
    fs_read_query='sum(rate(container_fs_reads_bytes_total{image!="", image!="google/cadvisor:latest"}[5s])) without (device)',
    # 查询容器文件系统写入速率（单位：字节/秒）
    fs_write_query='sum(rate(container_fs_writes_bytes_total{image!="", image!="google/cadvisor:latest"}[5s])) without (device)'
)


def log(*args, **kwargs):
    print(*args, **kwargs)


def ensure(condition, description):
    assert condition, description


def float_of_mb(number_of_bytes: str):
    f = float(number_of_bytes) / (1024 ** 2)
    return f


def container_metrics(query):
    # time_range 的单位是秒
    time_range = 60 * 15
    now = int(time.time())
    start = now - time_range
    params = dict(
        query=query,
        start=start,
        end=now,
        step='3s',
    )
    url = config['prometheus_url']
    response = get(url, params=params)
    r = response.json()['data']['result']

    data = dict()
    for v in r:
        # instance = v['metric']['instance']
        container_name = v['metric']['name']
        values = v['values']
        data[container_name] = values
    return data


def save_plot(plot_id, plot_type, function_for_parsing_metric, title):
    fp = function_for_parsing_metric

    queries = dict(
        cpu=config['cpu_usage_query'],
        memory=config['memory_usage_query'],
        network_receive=config['network_receive_query'],
        network_transmit=config['network_transmit_query'],
        fs_read=config['fs_read_query'],
        fs_write=config['fs_write_query'],
    )
    query = queries[plot_type]

    plt.figure(plot_id)
    plt.ticklabel_format(style='plain')

    data = container_metrics(query)
    length = 0

    plots = []
    labels = []
    for i, (name, values) in enumerate(data.items()):
        times = []
        metrics = []
        if length == 0:
            length = len(values)
        for timestamp, metric in values:
            t = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
            times.append(t)
            m = fp(metric)
            metrics.append(m)
        # docs for specifying colors: https://matplotlib.org/users/colors.html
        color = 'C{}'.format(i)
        l = plt.plot(times, metrics, color, label=name)[0]
        plots.append(l)
        # e.g. 'lizardfs_chunkserver1' -> 'chunkserver1'
        n = name.replace('lizardfs_', '')
        labels.append(n)
    # 表示将 label 放在右下角
    location = (1.01, 0)
    plt.legend(handles=plots, labels=labels, loc=location)

    step = 20
    plt.xticks(range(0, length, step))

    x_label, y_label = 'Time', title
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    p = plt.gcf()
    w, h = 20, 5
    p.set_size_inches(w, h)
    f = '../metrics/{}.jpg'.format(plot_type)
    p.savefig(f, dpi=100)


def save_cpu_plot():
    id = 1
    type = 'cpu'
    title = 'CPU Usage(%)'
    save_plot(id, type, float, title)


def save_memory_plot():
    id = 2
    type = 'memory'
    title = 'Memory Usage(MB)'
    save_plot(id, type, float_of_mb, title)


def save_network_receive_plot():
    id = 3
    type = 'network_receive'
    title = 'Network Receive(MB/s)'
    save_plot(id, type, float_of_mb, title)


def save_network_transmit_plot():
    id = 4
    type = 'network_transmit'
    title = 'Network Transmit(MB/s)'
    save_plot(id, type, float_of_mb, title)


def save_fs_read_plot():
    id = 5
    type = 'fs_read'
    title = 'FS Read(MB/s)'
    save_plot(id, type, float_of_mb, title)


def save_fs_write_plot():
    id = 6
    type = 'fs_write'
    title = 'FS Write(MB/s)'
    save_plot(id, type, float_of_mb, title)


def multi_process(tasks):
    ps = []
    for t in tasks:
        n = t.__name__
        p = Process(target=t, name=n)
        p.start()
        ps.append(p)
    for p in ps:
        p.join()


def main():
    tasks = [
        save_cpu_plot,
        save_memory_plot,
        save_network_receive_plot,
        save_network_transmit_plot,
        save_fs_read_plot,
        save_fs_write_plot,
    ]
    multi_process(tasks)


if __name__ == '__main__':
    main()
