import requests
import json
import opencc
import csv
from bs4 import BeautifulSoup
from XunProxy import XunProxy
cc = opencc.OpenCC('t2s')


def ServerList(name):
    if name == "":
        name = "[LSP]"
    url = "https://api.gametools.network/bf1/servers/?name=" + name + "&lang=zh-TW"
    html = XunProxy(url)
    if html is not None:
        data = json.loads(cc.convert(html.text))
        if len(data['servers']) == 0:
            return "未搜索到相关服务器或者EA服务器已经崩溃！"
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


def Stats(name):
    if name is None:
        return "未绑定昵称！"
    url = "https://api.gametools.network/bf1/stats/?name=" + name
    html = XunProxy(url)
    if html is not None:
        data = json.loads(cc.convert(html.text))
        if 'error' not in data:
            returnStr = str("头像:" + str(data['avatar'])) + "\n" + str("昵称:" + str(data['userName'])) + "\n" + str(
                "等级:" + str(data['Rank'])) + "\n" + str("技巧值:" + str(data['Skill'])) + "\n" + str(
                "SPM:" + str(data['SPM'])) + "\n" + str("KPM:" + str(data['KPM'])) + "\n" + str(
                "胜率:" + str(data['Win'])) + "\n" + str("精准度:" + str(data['Accuracy'])) + "\n" + str(
                "爆头率:" + str(data['Headshots'])) + "\n" + str("KD:" + str(data['K/D']))
            return returnStr
        else:
            return "查询昵称有误！"
    else:
        return "查询超时，请稍后再试！"


def Weapons(name):
    if name is None:
        return "未绑定昵称！"
    url = "https://api.gametools.network/bf1/weapons/?name=" + name + "&lang=zh-TW"
    html = XunProxy(url)
    if html is not None:
        data = json.loads(cc.convert(html.text))
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


def Vehicles(name):
    if name is None:
        return "未绑定昵称！"
    url = "https://api.gametools.network/bf1/vehicles/?name=" + name + "&lang=zh-TW"
    html = XunProxy(url)
    if html is not None:
        data = json.loads(cc.convert(html.text))
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


def Recent(name):
    if name is None:
        return "未绑定昵称！"
    url = "https://battlefieldtracker.com/bf1/profile/pc/" + name
    html = XunProxy(url)
    if html is not None:
        bs = BeautifulSoup(html.text, "html.parser")
        error = bs.find(name="div", attrs={"class": "alert alert-danger alert-dismissable"})
        if error is None:
            index = bs.find(name="div", attrs={"class": "card-body player-sessions"}).find_all(name="div", attrs={
                "class": "sessions"})  # 判断目录
            times = 1
            returnStr = ""
            for i in range(len(index)):
                data = index[i].find(name="div", attrs={"class": "session-stats"}).find_all(name="div",
                                                                                            attrs={"style": "",
                                                                                                   "class": ""})
                returnStr = returnStr + "更新日期:" + index[i].find('span')['data-livestamp'][0:10] + "\n" + "SPM:" + data[
                    0].string + "\n" + "KD:" + data[1].string + "\n" + "KPM:" + data[2].string + "\n" + "游戏时间:" + data[
                                5].string + "\n" + "===================" + "\n"
                times = times + 1
                if times > 3:
                    break
        else:
            return "查询昵称有误或战绩网站已经崩溃！"
        returnStr = returnStr + "\n"
        return returnStr.replace("\n\n", "")
    else:
        return "查询超时，请稍后再试！"


def Binding(id, name):
    line = -1
    idList = []
    nameList = []
    f = open('id.csv', 'r')
    read = csv.reader(f)
    for index, info in enumerate(read):
        if str(id) == info[0]:
            line = index
            idList.append(info[0])
            nameList.append(name)
        else:
            idList.append(info[0])
            nameList.append(info[1])
        # print(index, info[1])
    if line == -1:
        idList.append(id)
        nameList.append(name)

    f1 = open('id.csv', 'w+', newline='', encoding="utf-8")
    writer = csv.writer(f1)

    csvList = []
    for i in range(len(idList)):
        csvList = csvList + [(idList[i], nameList[i])]
    for j in csvList:
        writer.writerow(j)
    return "当前QQ绑定的ID为：[" + str(name) + "]"


def FindBinding(id):
    f = open('id.csv', 'r')
    read = csv.reader(f)
    for index, info in enumerate(read):
        if str(id) == info[0]:
            return info[1]


def BFservers(id, command):
    if command.startswith("/服务器"):
        return ServerList(command.replace("/服务器", "").replace(" ", ""))
    elif command.startswith("/战绩"):
        if command.replace("/战绩", "") == "":
            return Stats(FindBinding(id))
        else:
            return Stats(command.replace("/战绩", "").replace(" ", ""))
    elif command.startswith("/武器"):
        if command.replace("/武器", "") == "":
            return Weapons(FindBinding(id))
        else:
            return Weapons(command.replace("/武器", "").replace(" ", ""))
    elif command.startswith("/载具"):
        if command.replace("/载具", "") == "":
            return Vehicles(FindBinding(id))
        else:
            return Vehicles(command.replace("/载具", "").replace(" ", ""))
    elif command.startswith("/最近"):
        if command.replace("/最近", "") == "":
            return Recent(FindBinding(id))
        else:
            return Recent(command.replace("/最近", "").replace(" ", ""))
    elif command.startswith("/帮助"):
        return "本程序由Super水神编写，暂时仅供LSP和PKEM服务器使用。\n目前支持的战地1功能为：\n“/绑定+（空格）+[ID]”、\n“/服务器+（空格）+[名称]”、\n“/战绩+（空格）+[ID]”、\n“/武器+（空格）+[ID]”、\n" \
               "“/载具+（id）”、\n“/最近+（id）”、\n“/帮助”\n由于该程序相当简陋，请温柔对待哦(●'◡'●) "
    else:
        pass
