import json
import csv
from XunProxy import aioRequest


async def NewVideo(UidList):
    for a in range(len(UidList)):
        url = "http://api.bilibili.com/x/space/arc/search?mid=" + str(UidList[a]) + "&ps=4&pn=1"
        html = await aioRequest(url)
        if html is not None:
            json_str = json.loads(html)
            with open('./videolist.csv', 'r', encoding='utf-8') as f:
                data = list(csv.reader(f))
            vlist = json_str["data"]["list"]["vlist"]
            for video in vlist:
                n = 0
                for i in range(0, len(data)):
                    if data[i][0] == video["bvid"]:
                        n = n + 1
                if n == 0:
                    csvList = [(video["bvid"])]
                    with open('./videolist.csv', 'a+', encoding='utf-8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(csvList)
                    returnVideo = [video["title"], video["bvid"], video["author"], video["pic"].replace("//", "")]
                    return returnVideo
        else:
            return None
