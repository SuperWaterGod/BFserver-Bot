import requests

proxies = {
    'https': 'https://127.0.0.1:1080',
    'http': 'http://127.0.0.1:1080'
}
head = {
        'authority': 'search.jd.com',
        'method': 'GET',
        'path': '/Search?keyword=%E7%94%B5%E8%84%91&enc=utf-8&pvid=d4a3fce8a4e8424ba3a11de05bbdd443',
        'scheme': 'https',
        'referer': 'https://search.jd.com/Search?keyword=%E7%94%B5%E8%84%91&enc=utf-8&wq=%E7%94%B5%E8%84%91&pvid=097a8dead9704f0d85ba224fce56c8c1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'Cookie': 'areaId=22; ipLoc-djd=22-1930-50947-0; PCSYCityID=CN_510000_510100_510107; shshshfpa=3c696b4b-4db5-8688-b7bf-53d8ef2639d1-1577169256; shshshfpb=3c696b4b-4db5-8688-b7bf-53d8ef2639d1-1577169256; xtest=7978.cf6b6759; unpl=V2_ZzNtbUVVRUVxDREGL0taBWJWGlkSVEcRIghGXSkdW1ViAEdbclRCFX0URldnGlgUZwAZWEBcQxdFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHsaWgZvBRRVQFZzJXI4dmR9GFgHYAsiXHJWc1chVERUfR1dByoDEVtBX0UTfQpHZHopXw%3d%3d; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_637a54fcec714d95a255f118c56a42d7|1577248990400; qrsc=3; __jdu=1272977930; user-key=66522f02-f902-4764-8693-0eefdd7745bd; cn=0; __jda=122270672.1272977930.1577169251.1577257496.1577326776.5; __jdb=122270672.4.1272977930|5.1577326776; __jdc=122270672; shshshfp=7324c276d86c51251dbc81623c455052; shshshsID=febb1869dc62c6b7318e4bec8bb1e058_4_1577326815219; rkv=V0700; 3AB9D23F7A4B3C9B=WNBES7CO6JKYVHCHPD7S6VLV7PWVDFBTPTRJ4M6VCTBXXQAQWP2OXRZ6O4TNGNQCNETV57IOKIGZSUWHGMX32TMH2Y'

        }

response = requests.get("https://www.google.com/", proxies=proxies, timeout= 10)
html = requests.get("https://api.gametools.network/bf1/stats/?name=fpseelenoob", timeout= 10, headers=head, proxies=proxies)
print(response.text)
print(html.text)

while 1:
    pass