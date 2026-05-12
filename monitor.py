import psutil
import datetime


def collect_metrics():
    """返回当前时间点的指标字典"""
    cpu_percent = psutil.cpu_percent(interval=1)

    mem = psutil.virtual_memory()
    mem_total = mem.total
    mem_used = mem.used
    mem_percent = mem.percent

    disk = psutil.disk_usage('/')
    disk_total = disk.total
    disk_used = disk.used
    disk_percent = disk.percent

    net = psutil.net_io_counters()
    net_sent = net.bytes_sent
    net_recv = net.bytes_recv

    return {
        'metric_time': datetime.datetime.now(),
        'cpu_percent': cpu_percent,
        'mem_total': mem_total,
        'mem_used': mem_used,
        'mem_percent': mem_percent,
        'disk_total': disk_total,
        'disk_used': disk_used,
        'disk_percent': disk_percent,
        'net_sent': net_sent,
        'net_recv': net_recv
    }