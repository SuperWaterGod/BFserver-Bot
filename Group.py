# -*-coding:utf-8-*-
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
from graia.application.friend import Friend
from graia.application.message.elements.internal import At, Plain, Image, Voice, Quote, Source
from graia.application.session import Session
from graia.application.group import Group, Member, Optional
from graia.scheduler import timers
import graia.scheduler as scheduler

import asyncio
import os
import re
import json
import time
import jieba
from pypinyin import lazy_pinyin

from match import AutoReply, AutoVoice
from battlefield import BFservers, Binding
from Botstatus import Botstatus
from XunProxy import aioRequest, PicDownload
from video import NewVideo

from config import LoliconKey, SearchSetting

settings = json.load(open("./Settings.json"))
Admin = settings["Admin"]
Bot = settings["Bot"]
ScheduleGroup = []
TestGroup = []
BlackId = []
for i in range(len(settings["Group"])):
    if settings["Group"][i]["function"]["Schedule"]:
        ScheduleGroup.append(settings["Group"][i]["id"])
    if settings["Group"][i]["function"]["test"]:
        TestGroup.append(settings["Group"][i]["id"])
print("配置文件载入成功！")

WhiteGroup = [454375504, 863715876, 306800820, 1136543076, 781963214, 1153476318]
BanSetu = [1136543076, 781963214]
BFUid = [18706000, 287122113, 526559715]

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop, use_dispatcher_statistics=True, use_reference_optimization=True)
sche = scheduler.GraiaScheduler(loop=loop, broadcast=bcc)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080",  # 填入 httpapi 服务运行的地址
        authKey="INITKEYfiyhSQvQ",  # 填入 authKey
        account=Bot,  # 你的机器人的 qq 号
        websocket=True  # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)


@sche.schedule(timers.every_custom_seconds(60))
async def Schedule_Task():
    UseTime = time.strftime('%H:%M', time.localtime(time.time()))
    if UseTime == "08:00":
        for i in range(len(ScheduleGroup)):
            await app.sendGroupMessage(ScheduleGroup[i], MessageChain.create([Image.fromLocalFile("./Menhera/121.png"), Plain("早早早(*´▽｀)ノノ")]))
    elif UseTime == "12:00":
        for i in range(len(ScheduleGroup)):
            await app.sendGroupMessage(ScheduleGroup[i], MessageChain.create([Image.fromLocalFile("./Menhera/44.jpg"), Plain("干饭时间到，开始干饭啦ヾ(^▽^*)))~")]))
    elif UseTime == "23:00":
        for i in range(len(ScheduleGroup)):
            await app.sendGroupMessage(ScheduleGroup[i], MessageChain.create([Image.fromLocalFile("./Menhera/122.png"), Plain("米娜桑，晚安(￣o￣) . z Z")]))
    VideoDetail = None
    if VideoDetail is not None:
        VideoMessage = "你关注的UP主:" + VideoDetail[2] + "发布了新的视频:\n" + VideoDetail[0] + "\n视频链接：https://www.bilibili.com/video/" + VideoDetail[1] + "\n快去给他一个三连吧o(*////▽////*)q"
        for i in range(len(ScheduleGroup)):
            await app.sendGroupMessage(ScheduleGroup[i], MessageChain.create([Image.fromNetworkAddress("http://" + VideoDetail[3]), Plain(VideoMessage)]))
    pass


@bcc.receiver("GroupMessage")
async def battlefield(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    if SearchSetting(group.id)["function"]["battlefield"]:
        MessageStr = message.asDisplay()
        if MessageStr.startswith("/最近") or MessageStr.startswith("/战绩") or MessageStr.startswith("/服务器") or MessageStr.startswith("/武器") or MessageStr.startswith("/载具"):
            if member.id in BlackId:
                await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("哼(╯▔皿▔)╯，不理你了！")]), quote=message[Source][0])
            else:
                if MessageStr.startswith("/最近"):
                    await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("\n" + await BFservers(member.id, MessageStr))]), quote=message[Source][0])
                elif MessageStr.startswith("/战绩"):
                    MessageGet = await BFservers(member.id, MessageStr)
                    if MessageGet.startswith("头像"):
                        avatar = re.findall('头像:(.*)', MessageGet)[0]
                        MessageStr = re.findall('昵称:[\s\S]*', MessageGet)[0]
                        try:
                            await app.sendGroupMessage(group, MessageChain.create([At(member.id), Image.fromNetworkAddress(avatar), Plain("\n" + MessageStr)]), quote=message[Source][0])
                        except:
                            await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("\n" + MessageGet)]), quote=message[Source][0])
                    else:
                        await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("\n" + MessageGet)]), quote=message[Source][0])
                elif MessageStr.startswith("/服务器") or MessageStr.startswith("/武器") or MessageStr.startswith("/载具"):
                    if MessageStr == "/服务器":
                        MessageStr += SearchSetting(group.id)["name"]
                    MessageGet = await BFservers(member.id, MessageStr)
                    if MessageGet.startswith("./"):
                        await app.sendGroupMessage(group, MessageChain.create([At(member.id), Image.fromLocalFile(MessageGet)]), quote=message[Source][0])
                        await asyncio.sleep(30)
                        os.remove(MessageGet)
                    else:
                        await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("\n" + MessageGet)]), quote=message[Source][0])
                elif MessageStr.startswith("/帮助"):
                    await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("\n" + await BFservers(member.id, MessageStr))]), quote=message[Source][0])
                elif MessageStr.startswith("/绑定"):
                    await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain(Binding(member.id, MessageStr.replace("/绑定", "").replace(" ", "")))]),
                                               quote=message[Source][0])


@bcc.receiver("GroupMessage")  # 收集群消息
async def message_log(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    if SearchSetting(group.id)["function"]["Record"]:
        if member.id not in SearchSetting(group.id)["blacklist"]:
            messageStr = message.asDisplay()
            name = "./log/" + str(group.id) + ".log"
            try:
                fp = open(name, 'a+', encoding='utf-8')
                fp.write(messageStr)
            except:
                fp = open(name, 'w', encoding='utf-8')
                fp.write(messageStr)
            fp.close()
            if member.id == Admin:
                if messageStr == "/词云":
                    txt = open(name, "r", encoding='utf-8').read()
                    words = jieba.lcut(txt)  # 使用精确模式对文本进行分词
                    counts = {}  # 通过键值对的形式存储词语及其出现的次数

                    for word in words:
                        if len(word) == 1:  # 单个词语不计算在内
                            continue
                        else:
                            counts[word] = counts.get(word, 0) + 1  # 遍历所有词语，每出现一次其对应的值加 1

                    items = list(counts.items())
                    items.sort(key=lambda x: x[1], reverse=True)  # 根据词语出现的次数进行从大到小排序

                    for i in range(20):
                        word, count = items[i]
                        print("{0:<5}{1:>5}".format(word, count))


@bcc.receiver("GroupMessage")  # 自动发送色图
async def pixiv_Group_listener(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    pinyinStr = ""
    for i in range(len(lazy_pinyin(message.asDisplay()))):
        pinyinStr += lazy_pinyin(message.asDisplay())[i]
    if pinyinStr.find("setu") >= 0:
        if member.id in BlackId:
            await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("哼(╯▔皿▔)╯，不理你了！")]))
        else:
            if SearchSetting(group.id)["function"]["setu"]:
                try:
                    url = "https://api.lolicon.app/setu/?apikey=" + LoliconKey[0]  # 1号api
                    data = json.loads(await aioRequest(url))
                    if data['code'] == 0:
                        messageId = await app.sendGroupMessage(group, MessageChain.create([At(member.id), Image.fromNetworkAddress(data['data'][0]['url'])]))
                        await asyncio.sleep(60)
                        await app.revokeMessage(messageId)
                    elif data['code'] == 429:
                        url = "https://api.lolicon.app/setu/?apikey=" + LoliconKey[1]  # 2号api
                        data = json.loads(await aioRequest(url))
                        if data['code'] == 0:
                            messageId = await app.sendGroupMessage(group, MessageChain.create([At(member.id), Image.fromNetworkAddress(data['data'][0]['url'])]))
                            await asyncio.sleep(60)
                            await app.revokeMessage(messageId)
                        else:
                            await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("今天发的已经够多了，明天再来吧~")]))
                    else:
                        await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("今天发的已经够多了，明天再来吧~")]))
                except:
                    await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("诶呀，发生一个未知的错误(ˉ▽ˉ；)...")]))
            else:
                await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("本群因管理要求已禁止使用色图功能╮(╯▽╰)╭")]))


@bcc.receiver("GroupMessage")  # 自动回复群消息及表情
async def AutoReply_Group_listener(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    MessageGet = AutoReply(message.asDisplay())
    if MessageGet.startswith("./Menhera/"):
        await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile(MessageGet)]))
    elif MessageGet == "":
        pass
    else:
        await app.sendGroupMessage(group, MessageChain.create([Plain(MessageGet)]))


@bcc.receiver("GroupMessage")  # 自动回复语音
async def AutoVoice_Group_listener(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    MessageGet = AutoVoice(message.asDisplay())
    if MessageGet.startswith("./voice/"):
        await app.sendGroupMessage(group, MessageChain.create([Voice().fromLocalFile(MessageGet)]))
    elif MessageGet == "":
        pass


@bcc.receiver("GroupMessage")  # 加入黑名单
async def BlackId_Group_listener(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    if message.has(At):
        AtLsit = []
        for i in range(len(message.get(At))):
            AtLsit.append(int(re.findall('target=(.*) ', str(message.get(At)[i]))[0]))
        for i in range(len(AtLsit)):
            if AtLsit[i] == Bot:
                pinyinStr = ""
                for i in range(len(lazy_pinyin(message.asDisplay()))):
                    pinyinStr += lazy_pinyin(message.asDisplay())[i]
                if pinyinStr.find("shabi") >= 0:
                    await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("不理你了！")]), quote=message[Source][0])
                    BlackId.append(member.id)
                else:
                    await app.sendGroupMessage(group, MessageChain.create([Plain("@我没有用哦~")]), quote=message[Source][0])


@bcc.receiver("MemberJoinEvent")  # 新人加入群
async def Member_join(app: GraiaMiraiApplication, group: Group, member: Member):
    await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("欢迎加入" + str(group.name) + "\n请将群昵称改为游戏ID!")]))


@bcc.receiver("MemberLeaveEventKick")  # 群员被T
async def Member_kick(app: GraiaMiraiApplication, group: Group, member: Member = "target"):
    await app.sendGroupMessage(group, MessageChain.create([Plain(str(member.name) + "(" + str(member.id) + ")" + "因语言过激，被管理员移出了本群。")]))


@bcc.receiver("MemberLeaveEventQuit")  # 群员离开
async def Member_quit(app: GraiaMiraiApplication, group: Group, member: Member):
    await app.sendGroupMessage(group, MessageChain.create([Plain("一根丧失梦想的薯条" + str(member.name) + "(" + str(member.id) + ")" + "心灰意冷地离开了本群")]))


@bcc.receiver("BotMuteEvent")  # 机器人被禁言
async def Bot_muted(app: GraiaMiraiApplication, group: Group, member: Member):
    await app.sendFriendMessage(Admin, MessageChain.create([Plain("已被" + str(member.name) + "在" + str(group.name) + "禁言")]))


@bcc.receiver("BotUnmuteEvent")  # 机器人解除禁言
async def Bot_unmuted(app: GraiaMiraiApplication, group: Group, member: Member):
    await app.sendFriendMessage(Admin, MessageChain.create([Plain("已被" + str(member.name) + "在" + str(group.name) + "解除禁言")]))


@bcc.receiver("FriendMessage")  # 自动回复好友消息及表情
async def AutoReply_Friend_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    MessageGet = AutoReply(message.asDisplay())
    if MessageGet.startswith("./Menhera/"):
        await app.sendFriendMessage(friend, MessageChain.create([Image.fromLocalFile(MessageGet)]))
    elif MessageGet == "":
        pass
    else:
        await app.sendFriendMessage(friend, MessageChain.create([Plain(MessageGet)]))


@bcc.receiver("FriendMessage")  # 好友TEST
async def Admin_Friend_Test(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    if friend.id == Admin:
        if message.asDisplay().startswith("/test"):
            await app.sendFriendMessage(friend, MessageChain.create([Plain(await PicDownload(message.asDisplay().replace("/test ")))]))


@bcc.receiver("GroupMessage")  # 群TEST
async def Admin_Group_Test(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    if group.id in TestGroup:
        await app.sendGroupMessage(group, MessageChain.create([Plain("test")]), quote=message[Source][0])


app.launch_blocking()
