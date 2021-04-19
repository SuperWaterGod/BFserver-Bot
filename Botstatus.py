import psutil
import asyncio


async def Botstatus():
    cpuInf = psutil.cpu_percent(interval=1)
    memoryInf = psutil.virtual_memory()
    memory = "%s/%s(%s%%)" % (
        str(int(memoryInf.used / 1024 / 1024)) + "M",
        str(int(memoryInf.total / 1024 / 1024)) + "M",
        memoryInf.percent
    )
    returnStr = [cpuInf, memory]
    return returnStr
