# -*-coding:utf-8-*-
import requests
from match import AutoReply
import opencc
cc = opencc.OpenCC('t2s')
url = "https://www.google.com/"
urlList = ["https://yingserver.cn/open/acgimg/acgurl.php", "https://api.ixiaowai.cn/api/api.php",
           "https://api.ixiaowai.cn/mcapi/mcapi.php",
           "https://open.pixivic.net/wallpaper/pc/random?size=large&domain=https://i.pixiv.cat&webp=0&detail=1"]
p = "https://pixiv.cat/"
proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}
head = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
}
try:
    html = requests.get(url, proxies=proxies, headers=head,verify=False,timeout=5)
    print(html.text)
except requests.exceptions.RequestException:
    print("超时")
    
print (cc.convert(u'Open Chinese Convert（OpenCC）「開放中文轉換」，是一個致力於中文簡繁轉換的項目，提供高質量詞庫和函數庫(libopencc)。'))
while 1:
    pass