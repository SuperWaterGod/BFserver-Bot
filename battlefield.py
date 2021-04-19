import requests
import json
import opencc
import csv
import re
import time
import asyncio
import random
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
from XunProxy import aioRequest, PicDownload

cc = opencc.OpenCC('t2s')


async def ServerList(name):
    if name == "":
        name = "[LSP]"
    url = "https://api.gametools.network/bf1/servers/?name=" + name + "&lang=zh-TW"
    html = await aioRequest(url)
    if html is not None:
        data = json.loads(cc.convert(html))
        if len(data['servers']) == 0:
            return "未能搜索到相关服务器。"
        else:
            returnStr = ""
            for i in range(len(data['servers'])):
                returnStr = returnStr + str(data['servers'][i]['prefix']) + "\n" + "在线人数:" + str(
                    data['servers'][i]['serverInfo']) + "\n" + "当前地图:" + str(
                    data['servers'][i]['currentMap']) + "\n" + "===================" + "\n"
            returnStr = returnStr + "\n"
            return returnStr.replace("\n\n", "")
    else:
        return "查询超时，请稍后再试！"


async def PicServerList(name):
    if name == "":
        name = "[LSP]"
    url = "https://api.gametools.network/bf1/servers/?name=" + name + "&lang=zh-TW"
    bg = "./pic/server_bg" + str(random.randint(1, 4)) + ".jpg"
    SavePic = "./Temp/" + str(int(time.time())) + ".jpg"

    html = await aioRequest(url)
    if html is not None:
        titleFont = ImageFont.truetype(u"./font/DFP_sougeitai_W5-d813b437.ttf", size=70)
        searchFont = ImageFont.truetype(u"./font/DFP_sougeitai_W5-d813b437.ttf", size=35)
        nameFont = ImageFont.truetype(u"./font/DFP_sougeitai_W5-d813b437.ttf", size=25)
        detailFont = ImageFont.truetype(u"./font/DFP_sougeitai_W5-d813b437.ttf", size=20)
        im = Image.open(bg)
        draw = ImageDraw.Draw(im)
        draw.text((300, 40), "伺服器列表", font=titleFont)
        draw.text((300, 120), "搜索内容：" + name.replace("%20", " "), font=searchFont)
        data = json.loads(html)
        if len(data['servers']) == 0:
            draw.text((800, 500), "找不到伺服器", font=searchFont)
            draw.text((795, 545), "變更篩選條件並重試", font=nameFont)
            im.save(SavePic)
        else:
            for i in range(len(data['servers'])):
                title = str(data['servers'][i]['prefix'])
                queue = str(data['servers'][i]['serverInfo']) + "[" + str(data['servers'][i]['inQue']) + "]"
                pic = str(data['servers'][i]['url'])
                detail = str(data['servers'][i]['mode']) + " - " + str(data['servers'][i]['currentMap']) + " - 60HZ"

                PicUrl = await PicDownload(pic)
                im1 = Image.open(PicUrl)
                im1.thumbnail((144, 84))
                im.paste(im1, (250, 200 + 100 * i))

                draw.text((400, 210 + 100 * i), title, font=nameFont)
                draw.text((1400, 210 + 100 * i), queue, font=nameFont)
                draw.text((400, 250 + 100 * i), detail, font=detailFont)

                if PicUrl == "./pic/play.jpg":
                    png = Image.open("./pic/ping-unknown.png").convert('RGBA')
                    im.paste(png, (1510, 210 + 100 * i), png)
                else:
                    png = Image.open("./pic/ping-best.png").convert('RGBA')
                    im.paste(png, (1510, 210 + 100 * i), png)
                if i >= 7:
                    break
            im.save(SavePic)
        return SavePic
    else:
        return "查询超时，请稍后再试！"


async def TempStats(name):
    if name is None:
        return "未绑定昵称！请使用“/绑定+（空格）+[ID]”绑定昵称"
    url = "https://battlefieldtracker.com/bf1/profile/pc/" + name
    html = await aioRequest(url)
    if html is not None:
        bs = BeautifulSoup(html, "html.parser")
        try:
            data = bs.find(name="div", attrs={"class": "card player-general"})
            rank = data.find_all(name="span", attrs={"class": "title"})
            content = []
            content.append(''.join(re.findall('[0-9]', rank[0].string)))
            details = data.find_all(name="div", attrs={"class": "value"})
            content.append(details[1].string)
            content.append(details[2].string)
            content.append(details[4].string)
            stats = bs.find_all(name="div", attrs={"class": "stats-large"})
            performance = stats[0].find_all(name="div", attrs={"class": "value"})
            content.append(''.join(re.findall('[0-9.,%]', performance[2].string)))
            content.append(''.join(re.findall('[0-9.,%]', performance[6].string)))
            content.append(''.join(re.findall('[0-9.,%]', performance[7].string)))
            general = stats[1].find_all(name="div", attrs={"class": "value"})
            content.append(''.join(re.findall('[0-9.,%]', general[5].string)))
            content.append(''.join(re.findall('[0-9.,%]', general[6].string)))
            returnStr = "昵称:" + name + "\n等级:" + content[0] + "\nKD:" + content[1] + "\n胜率:" + content[2] + "\n游戏时间:" + content[3] + "\nSPM:" + content[4] + \
                        "\n场均击杀:" + content[5] + "\nKPM:" + content[6] + "\n技巧值:" + content[7] + "\n精准度:" + content[8]
        except:
            return "查询昵称有误！"
        return returnStr
    else:
        return "查询超时，请稍后再试！"


async def Stats(name):
    if name is None:
        return "未绑定昵称！请使用“/绑定+（空格）+[ID]”绑定昵称"
    url = "https://api.gametools.network/bf1/stats/?name=" + name
    html = await aioRequest(url)
    if html is not None:
        try:
            data = json.loads(html)
            if 'error' not in data:
                returnStr = str("头像:" + str(data['avatar'])) + \
                            str("\n昵称:" + str(data['userName'])) + \
                            str("\n等级:" + str(data['Rank'])) + \
                            str("\nKD:" + str(data['K/D'])) + \
                            str("\nSPM:" + str(data['SPM'])) + \
                            str("\nKPM:" + str(data['KPM'])) + \
                            str("\n胜率:" + str(data['Win'])) + \
                            str("\n技巧值:" + str(data['Skill'])) + \
                            str("\n精准度:" + str(data['Accuracy'])) + \
                            str("\n爆头率:" + str(data['Headshots'])) + \
                            str("\n总击杀:" + str(data['Kills'])) + \
                            str("\n游戏局数:" + str(data['roundsPlayed'])) + \
                            str("\n场均击杀:" + str(format(data['Kills'] / data['roundsPlayed'], '.1f')))
                return returnStr
            else:
                return "查询昵称有误！"
        except:
            return await TempStats(name)
    else:
        return "查询超时，请稍后再试！"


async def Weapons(name):
    if name is None:
        return "未绑定昵称！请使用“/绑定+（空格）+[ID]”绑定昵称"
    url = "https://api.gametools.network/bf1/weapons/?name=" + name + "&lang=zh-TW"
    html = await aioRequest(url)
    if html is not None:
        data = json.loads(cc.convert(html))
        if 'error' not in data:
            weaponsData = data['weapons']
            weaponsList = sorted(weaponsData, key=lambda student: student['kills'], reverse=True)
            returnStr = ""
            for i in range(6):
                returnStr = returnStr + str("武器：" + str(weaponsList[i]['weaponName'])) + "\n" + str(
                    "击杀数：" + str(weaponsList[i]['kills'])) + "\n" + str(
                    "KPM：" + str(weaponsList[i]['killsPerMinute'])) + "\n" + str(
                    "精准度：" + str(weaponsList[i]['accuracy'])) + "\n" + str(
                    "爆头率：" + str(weaponsList[i]['headshots'])) + "\n"
            returnStr = returnStr + "\n"
            return returnStr.replace("\n\n", "")
            pass
        else:
            return "查询昵称有误！"
    else:
        return "查询超时，请稍后再试！"


async def PicWeapons(name):
    if name is None:
        return "未绑定昵称！请使用“/绑定+（空格）+[ID]”绑定昵称"
    url = "https://api.gametools.network/bf1/weapons/?name=" + name + "&lang=zh-TW"
    bg = "./pic/weapons" + str(random.randint(1, 8)) + ".jpg"
    SavePic = "./Temp/" + str(int(time.time())) + ".jpg"

    html = await aioRequest(url)
    if html is not None:
        data = json.loads(html)
        if 'error' not in data:
            im = Image.open(bg)
            draw = ImageDraw.Draw(im)
            nameFont = ImageFont.truetype(u"./font/DFP_sougeitai_W5-d813b437.ttf", size=35)
            titleFont = ImageFont.truetype(u"./font/Deng.ttf", size=20)
            detailFont = ImageFont.truetype(u"./font/Deng.ttf", size=16)

            draw.text((50, 30), name, font=nameFont)
            weaponsData = data['weapons']
            weaponsList = sorted(weaponsData, key=lambda student: student['kills'], reverse=True)

            for i in range(5):
                star = int(weaponsList[i]['kills'] / 100)
                weaponsStar = "★ " + str(star)
                weaponsName = str(weaponsList[i]['weaponName'])
                weaponsKills = "击杀数：" + str(weaponsList[i]['kills'])
                weaponsKpm = "K P M：" + str(weaponsList[i]['killsPerMinute'])
                weaponsAcc = "精准度：" + str(weaponsList[i]['accuracy'])
                weaponsHs = "爆头率：" + str(weaponsList[i]['headshots'])
                pic = str(weaponsList[i]['image'])
                PicUrl = await PicDownload(pic)
                w, h = titleFont.getsize(weaponsName)

                draw.text(((562 - w) / 2, 200 + 228 * i), weaponsName, font=titleFont)
                if star >= 100:
                    draw.text((90, 95 + 228 * i), weaponsStar, font=titleFont, fill=(255, 132, 0))
                    png = Image.open("./pic/medium_orange.png").convert('RGBA')
                    im.paste(png, (180, 40 + 228 * i), png)

                elif 100 > star >= 60:
                    draw.text((90, 95 + 228 * i), weaponsStar, font=titleFont)
                    png = Image.open("./pic/medium_blue.png").convert('RGBA')
                    im.paste(png, (180, 40 + 228 * i), png)

                elif 60 > star >= 40:
                    draw.text((90, 95 + 228 * i), weaponsStar, font=titleFont)
                    png = Image.open("./pic/medium_white.png").convert('RGBA')
                    im.paste(png, (180, 40 + 228 * i), png)
                elif star > 0:
                    draw.text((90, 95 + 228 * i), weaponsStar, font=titleFont)
                draw.text((160, 230 + 228 * i), weaponsKills, font=detailFont)
                draw.text((300, 230 + 228 * i), weaponsAcc, font=detailFont)
                draw.text((160, 250 + 228 * i), weaponsKpm, font=detailFont)
                draw.text((300, 250 + 228 * i), weaponsHs, font=detailFont)

                png = Image.open(PicUrl).convert('RGBA')
                im.paste(png, (150, 110 + 228 * i), png)
            im.save(SavePic, 'JPEG', quality=100)
            return SavePic

        else:
            return "查询昵称有误！"
    else:
        return "查询超时，请稍后再试！"


async def Vehicles(name):
    if name is None:
        return "未绑定昵称！请使用“/绑定+（空格）+[ID]”绑定昵称"
    url = "https://api.gametools.network/bf1/vehicles/?name=" + name + "&lang=zh-TW"
    html = await aioRequest(url)
    if html is not None:
        data = json.loads(cc.convert(html))
        if 'error' not in data:
            vehiclesData = data['vehicles']
            vehiclesList = sorted(vehiclesData, key=lambda student: student['kills'], reverse=True)
            returnStr = ""
            for i in range(6):
                returnStr = returnStr + "载具：" + str(vehiclesList[i]['vehicleName']) + "\n" + "击杀数：" + str(
                    vehiclesList[i]['kills']) + "\n" + "KPM：" + str(vehiclesList[i]['killsPerMinute']) + "\n"
            returnStr = returnStr + "\n"
            return returnStr.replace("\n\n", "")
            pass
        else:
            return "查询昵称有误！"
    else:
        return "查询超时，请稍后再试！"


async def PicVehicles(name):
    if name is None:
        return "未绑定昵称！请使用“/绑定+（空格）+[ID]”绑定昵称"
    url = "https://api.gametools.network/bf1/vehicles/?name=" + name + "&lang=zh-TW"
    bg = "./pic/vehicles" + str(random.randint(1, 8)) + ".jpg"
    SavePic = "./Temp/" + str(int(time.time())) + ".jpg"

    html = await aioRequest(url)
    if html is not None:
        data = json.loads(html)
        if 'error' not in data:
            im = Image.open(bg)
            draw = ImageDraw.Draw(im)
            nameFont = ImageFont.truetype(u"./font/DFP_sougeitai_W5-d813b437.ttf", size=35)
            titleFont = ImageFont.truetype(u"./font/Deng.ttf", size=20)
            detailFont = ImageFont.truetype(u"./font/Deng.ttf", size=16)

            draw.text((50, 30), name, font=nameFont)
            vehiclesData = data['vehicles']
            vehiclesList = sorted(vehiclesData, key=lambda student: student['kills'], reverse=True)

            for i in range(5):
                star = int(vehiclesList[i]['kills'] / 100)
                vehiclesStar = "★ " + str(star)
                vehiclesName = str(vehiclesList[i]['vehicleName'])
                vehiclesKills = "击杀数：" + str(vehiclesList[i]['kills'])
                vehiclesKpm = "K P M：" + str(vehiclesList[i]['killsPerMinute'])

                pic = str(vehiclesList[i]['image'])
                PicUrl = await PicDownload(pic)
                w, h = titleFont.getsize(vehiclesName)

                draw.text(((562 - w) / 2, 200 + 228 * i), vehiclesName, font=titleFont)
                if star >= 100:
                    draw.text((90, 95 + 228 * i), vehiclesStar, font=titleFont, fill=(255, 132, 0))
                    png = Image.open("./pic/medium_orange.png").convert('RGBA')
                    im.paste(png, (180, 40 + 228 * i), png)

                elif 100 > star >= 60:
                    draw.text((90, 95 + 228 * i), vehiclesStar, font=titleFont)
                    png = Image.open("./pic/medium_blue.png").convert('RGBA')
                    im.paste(png, (180, 40 + 228 * i), png)

                elif 60 > star >= 40:
                    draw.text((90, 95 + 228 * i), vehiclesStar, font=titleFont)
                    png = Image.open("./pic/medium_white.png").convert('RGBA')
                    im.paste(png, (180, 40 + 228 * i), png)
                elif star > 0:
                    draw.text((90, 95 + 228 * i), vehiclesStar, font=titleFont)
                draw.text((160, 230 + 228 * i), vehiclesKills, font=detailFont)
                draw.text((160, 250 + 228 * i), vehiclesKpm, font=detailFont)

                png = Image.open(PicUrl).convert('RGBA')
                im.paste(png, (150, 110 + 228 * i), png)
            im.save(SavePic, 'JPEG', quality=100)
            return SavePic

        else:
            return "查询昵称有误！"
    else:
        return "查询超时，请稍后再试！"


async def Recent(name):
    if name is None:
        return "未绑定昵称！请使用“/绑定+（空格）+[ID]”绑定昵称"
    url = "https://battlefieldtracker.com/bf1/profile/pc/" + name
    html = await aioRequest(url)
    if html is not None:
        bs = BeautifulSoup(html, "html.parser")
        try:
            index = bs.find(name="div", attrs={"class": "card-body player-sessions"}).find_all(name="div", attrs={"class": "sessions"})  # 判断目录
            times = 1
            returnStr = ""
            for i in range(len(index)):
                data = index[i].find(name="div", attrs={"class": "session-stats"}).find_all(name="div", attrs={"style": "", "class": ""})
                returnStr = returnStr + \
                            "更新日期:" + index[i].find('span')['data-livestamp'][0:10] + \
                            "\nSPM:" + data[0].string + \
                            "\nKD:" + data[1].string + \
                            "\nKPM:" + data[2].string + \
                            "\n游戏时间:" + data[5].string + \
                            "\n===================" + "\n"
                times = times + 1
                if times > 3:
                    break
        except:
            settings = json.load(open("./Settings.json", encoding='utf-8'))
            return settings["Msg"]["Error"]["battletracker"]
        returnStr = returnStr + "\n"
        return returnStr.replace("\n\n", "")
    else:
        return "查询超时，请稍后再试！"


def Binding(id, name):
    line = -1
    idList = []
    nameList = []
    CorrectName = ''.join(re.findall('[a-zA-Z0-9-_]', name))
    if CorrectName == "":
        return "绑定失败：请勿绑定空昵称！"
    print(CorrectName)
    f = open('id.csv', 'r', encoding="utf-8")
    read = csv.reader(f)
    for index, info in enumerate(read):
        if str(id) == info[0]:
            line = index
            idList.append(info[0])
            nameList.append(CorrectName)
        else:
            idList.append(info[0])
            nameList.append(info[1])
        # print(index, info[1])
    if line == -1:
        idList.append(id)
        nameList.append(CorrectName)

    f1 = open('id.csv', 'w+', newline='', encoding="utf-8")
    writer = csv.writer(f1)

    csvList = []
    for i in range(len(idList)):
        csvList = csvList + [(idList[i], nameList[i])]
    for j in csvList:
        writer.writerow(j)
    return "当前QQ绑定的ID为：[" + str(CorrectName) + "]"


def FindBinding(id):
    f = open('id.csv', 'r')
    read = csv.reader(f)
    for index, info in enumerate(read):
        if str(id) == info[0]:
            return info[1]


async def BFservers(id, command):
    if command.startswith("/服务器"):
        return await PicServerList(command.replace("/服务器 ", "").replace("/服务器", "").replace(" ", "%20"))
    elif command.startswith("/战绩"):
        if command.replace("/战绩", "") == "":
            return await Stats(FindBinding(id))
        else:
            return await Stats(command.replace("/战绩", "").replace(" ", ""))
    elif command.startswith("/武器"):
        if command.replace("/武器", "") == "":
            return await PicWeapons(FindBinding(id))
        else:
            return await PicWeapons(command.replace("/武器", "").replace(" ", ""))
    elif command.startswith("/载具"):
        if command.replace("/载具", "") == "":
            return await PicVehicles(FindBinding(id))
        else:
            return await PicVehicles(command.replace("/载具", "").replace(" ", ""))
    elif command.startswith("/最近"):
        if command.replace("/最近", "") == "":
            return await Recent(FindBinding(id))
        else:
            return await Recent(command.replace("/最近", "").replace(" ", ""))
    elif command.startswith("/帮助"):
        return "本程序由Super水神编写，作者QQ:1341283988。\n" \
               "目前支持的战地1功能为：\n" \
               "“/绑定+（空格）+[ID]”\n" \
               "“/服务器+（空格）+[名称]”\n" \
               "“/战绩+（空格）+[ID]”\n" \
               "“/武器+（空格）+[ID]”\n" \
               "“/载具+（id）”\n" \
               "“/最近+（id）”\n" \
               "“/帮助”\n" \
               "以上命令无需输入+和（）\n" \
               "由于该程序相当简陋，请温柔对待哦(●'◡'●) "
    else:
        pass
