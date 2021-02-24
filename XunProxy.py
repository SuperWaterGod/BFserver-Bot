import sys
import time
import hashlib
import requests
import urllib3
from requests.adapters import HTTPAdapter

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
_version = sys.version_info
is_python3 = (_version[0] == 3)


def XunProxy(url):
    orderno = "ZF20212239523CdBejh"
    secret = "e44f1a3ba73a41bbb8477e0250ae45be"

    timestamp = str(int(time.time()))
    string = "orderno=" + orderno + ",secret=" + secret + ",timestamp=" + timestamp
    if is_python3:
        string = string.encode()
    sign = hashlib.md5(string).hexdigest().upper()
    auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
    proxy = {
        "http": "http://forward.xdaili.cn:80", "https": "https://forward.xdaili.cn:80"
    }
    headers = {
        "Proxy-Authorization": auth,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }

    '''session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=2))
    session.mount('https://', HTTPAdapter(max_retries=2))'''
    i = 0
    while i < 3:
        try:
            html = requests.get(url, headers=headers, proxies=proxy, timeout=5, verify=False, allow_redirects=False)
            return html
        except requests.exceptions.RequestException:
            i += 1
    return None


'''if html.status_code == 302 or html.status_code == 301:
    loc = html.headers['Location']
    print(loc)
    html = requests.get(loc, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
    html.encoding = 'utf8'
    print(html.status_code)
    print(html.text)'''
# print(XunProxy("https://api.gametools.network/bf1/servers/?name=LSP"))