import sys
import time
import hashlib
import requests
import urllib3
import asyncio
from requests.adapters import HTTPAdapter
import aiohttp

from config import Xunorderno, Xunsecret

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
_version = sys.version_info
is_python3 = (_version[0] == 3)


def XunProxy(url):
    timestamp = str(int(time.time()))
    string = "orderno=" + Xunorderno + ",secret=" + Xunsecret + ",timestamp=" + timestamp
    if is_python3:
        string = string.encode()
    sign = hashlib.md5(string).hexdigest().upper()
    auth = "sign=" + sign + "&" + "orderno=" + Xunorderno + "&" + "timestamp=" + timestamp
    proxy = {
        "http": "http://forward.xdaili.cn:80", "https": "https://forward.xdaili.cn:80"
    }
    headers = {
        "Proxy-Authorization": auth,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }

    i = 0
    while i < 5:
        try:
            if (i % 2) == 0:
                html = requests.get(url, headers=headers, proxies=proxy, timeout=5, verify=False, allow_redirects=False)
                return html
            else:
                html = requests.get(url, headers=headers, timeout=5)
                return html
        except requests.exceptions.RequestException:
            i += 1
    return None


async def aioRequest(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    i = 0
    while i < 5:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=5, headers=headers, verify_ssl=False) as resp:
                    return await resp.text()
            except:
                i += 1
    return None


async def PicDownload(url):
    file_name = "./pic" + url[url.rfind('/'):]
    try:
        fp = open(file_name, 'rb')
        fp.close()
        return file_name
    except:
        i = 0
        while i < 3:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url, timeout=5, verify_ssl=False) as resp:
                        pic = await resp.read()
                        fp = open(file_name, 'wb')
                        fp.write(pic)
                        fp.close()
                        return file_name
                except:
                    i += 1
        return "./pic/play.jpg"
