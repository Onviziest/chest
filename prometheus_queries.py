# 结合 cAdvisor
queries_container = dict(
    cpu_usage_query='sum(rate(container_cpu_usage_seconds_total{name=~".+", image!="", image!="google/cadvisor:latest"}[1m])) by (name) * 100',
    # 查询容器内存使用量（单位：字节）
    memory_usage_query='container_memory_usage_bytes{image!="", image!="google/cadvisor:latest"}',
    # 查询容器网络接收量速率（单位：字节/秒）
    network_receive_query='sum(rate(container_network_receive_bytes_total{image!="", image!="google/cadvisor:latest"}[1m])) without (interface)',
    # 查询容器网络传输量速率（单位：字节/秒）
    network_transmit_query='sum(rate(container_network_transmit_bytes_total{image!="", image!="google/cadvisor:latest"}[1m])) without (interface)',
    # 查询容器文件系统读取速率（单位：字节/秒）
    fs_read_query='sum(rate(container_fs_reads_bytes_total{image!="", image!="google/cadvisor:latest"}[1m])) without (device)',
    # 查询容器文件系统写入速率（单位：字节/秒）
    fs_write_query='sum(rate(container_fs_writes_bytes_total{image!="", image!="google/cadvisor:latest"}[1m])) without (device)'
)
