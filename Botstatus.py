import psutil
import asyncio


def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9.8 K'
    >>> bytes2human(100001221)
    '95.4 M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f %s' % (value, s)
    return '%.2f B' % n


async def Botstatus():
    # CPU
    cpuInf = psutil.cpu_percent(interval=1)
    # 内存
    memoryInf = psutil.virtual_memory()
    memory = "%s/%s(%s%%)" % (
        str(int(memoryInf.used / 1024 / 1024)) + "M",
        str(int(memoryInf.total / 1024 / 1024)) + "M",
        memoryInf.percent
    )
    # 网络
    pnic_before = psutil.net_io_counters(pernic=True)
    pnic_after = psutil.net_io_counters(pernic=True)
    # nic_names = pnic_after.keys()
    # print(nic_names)
    name = "以太网"
    stats_before = pnic_before[name]
    stats_after = pnic_after[name]
    sentTOTAL = bytes2human(stats_after.bytes_sent)
    sentPERSEC = bytes2human(stats_after.bytes_sent - stats_before.bytes_sent) + '/s'
    recvTOTAL = bytes2human(stats_after.bytes_recv)
    recvPERSEC = bytes2human(stats_after.bytes_recv - stats_before.bytes_recv) + '/s'
    network = [sentTOTAL, sentPERSEC, recvTOTAL, recvPERSEC]
    returnStr = [cpuInf, memory, network]
    return returnStr
