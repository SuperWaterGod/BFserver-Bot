import psutil


def Botstatus():
    returnStr = [psutil.cpu_percent(interval=1), psutil.virtual_memory().percent]
    return returnStr


print(Botstatus())
