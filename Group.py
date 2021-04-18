# -*-coding:utf-8-*-
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
from graia.application.friend import Friend
from graia.application.message.elements.internal import At, Plain, Image, Voice, Quote, Source
from graia.application.session import Session
from graia.broadcast.interrupt import InterruptControl
from graia.broadcast.interrupt.waiter import Waiter
from graia.application.event.messages import GroupMessage
from graia.application.event.mirai import BotInvitedJoinGroupRequestEvent
from graia.application.group import Group, Member, Optional
from graia.scheduler import timers
import graia.scheduler as scheduler
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import FullMatch, OptionalParam, RequireParam

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
from Botstatus import Botstatus

from config import LoliconKey, SearchSetting

settings = json.load(open("./Settings.json", encoding='utf-8'))
Admin = settings["Admin"]
Bot = settings["Bot"]
ScheduleGroup = []
TestGroup = []
BlackId = set()
StartTime = time.time()
for i in settings["Group"]:
    if i["function"]["Schedule"]:
        ScheduleGroup.append(i["id"])
    if i["function"]["test"]:
        TestGroup.append(i["id"])
print("配置文件载入成功！")

BFUid = [18706000, 287122113, 526559715]

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop, use_dispatcher_statistics=True, use_reference_optimization=True)
sche = scheduler.GraiaScheduler(loop=loop, broadcast=bcc)
inc = InterruptControl(bcc)
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
        if any([MessageStr.startswith("/最近"), MessageStr.startswith("/战绩"), MessageStr.startswith("/服务器"), MessageStr.startswith("/武器"), MessageStr.startswith("/载具"),
                MessageStr.startswith("/帮助"), MessageStr.startswith("/绑定")]):
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
                            await app.sendGroupMessage(group, MessageChain.create([At(member.id), Image.fromNetworkAddress(avatar), Plain("\n" + MessageStr)]),
                                                       quote=message[Source][0])
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
    if not pinyinStr.startswith("/"):
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


@bcc.receiver("GroupMessage")  # 自动回复群消息表情及语音
async def AutoReply_Group_listener(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    if SearchSetting(group.id)["function"]["AutoReply"]:
        if member.id not in BlackId:
            MessageGet = AutoReply(message.asDisplay())
            if MessageGet.startswith("./Menhera/"):
                await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile(MessageGet)]))
            elif MessageGet == "":
                pass
            else:
                await app.sendGroupMessage(group, MessageChain.create([Plain(MessageGet)]))
            MessageGet = AutoVoice(message.asDisplay())
            if MessageGet.startswith("./voice/"):
                await app.sendGroupMessage(group, MessageChain.create([Voice().fromLocalFile(MessageGet)]))
            elif MessageGet == "":
                pass


@bcc.receiver("GroupMessage")  # 加入/移除黑名单
async def BlackId_Group_listener(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    if message.has(At):
        AtLsit = []
        for i in range(len(message.get(At))):
            AtLsit.append(int(re.findall('target=(.*) ', str(message.get(At)[i]))[0]))
        MessageGet = message.asDisplay().replace(" ", "")
        for i in range(len(AtLsit)):
            if AtLsit[i] == Bot:
                pinyinStr = ""
                for i in range(len(lazy_pinyin(MessageGet))):
                    pinyinStr += lazy_pinyin(MessageGet)[i]
                if pinyinStr.find("shabi") >= 0 or pinyinStr.find("hanhan") >= 0 or pinyinStr.find("bendan") >= 0:
                    if pinyinStr.find("woshishabi") < 0:
                        await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("不理你了！")]), quote=message[Source][0])
                        BlackId.add(member.id)
                elif MessageGet.find("对不起") >= 0 or MessageGet.find("我错了") >= 0 or MessageGet.find("抱歉") >= 0:
                    if member.id in BlackId:
                        await app.sendGroupMessage(group, MessageChain.create([At(member.id), Image.fromLocalFile("./Menhera/37.jpg"), Plain("想让我原谅你？请问谁是傻逼？")]))

                        @Waiter.create_using_function([GroupMessage])
                        async def Remove_Blacklist(event: GroupMessage, waiter_group: Group, waiter_member: Member, waiter_message: MessageChain):
                            if waiter_group.id == group.id and waiter_member.id == member.id and waiter_message.asDisplay().find("我是傻逼") >= 0:
                                await app.sendGroupMessage(group, MessageChain.create([At(member.id), Image.fromLocalFile("./Menhera/110.jpg"), Plain("哼，这还差不多┑(￣Д ￣)┍")]))
                                BlackId.remove(member.id)
                                await app.sendGroupMessage(group, MessageChain.create([Plain("这次就算了，下不为例哦╰(￣ω￣ｏ)")]))
                                return event

                        try:
                            await asyncio.wait_for(inc.wait(Remove_Blacklist), timeout=30)
                        except asyncio.TimeoutError:
                            await app.sendGroupMessage(group, MessageChain.create([At(member.id), Image.fromLocalFile("./Menhera/63.jpg"), Plain("\n不承认自己是傻逼就算了(* ￣︿￣)")]))
                        pass
                    else:
                        await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile("./Menhera/139.png")]), quote=message[Source][0])
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


@bcc.receiver(BotInvitedJoinGroupRequestEvent)  # 机器人邀请进群
async def Bot_Join_Group(app: GraiaMiraiApplication, event: BotInvitedJoinGroupRequestEvent):
    if event.supplicant == Admin:
        await app.sendFriendMessage(Admin, MessageChain.create([Plain("已同意加入" + event.groupName + "（" + str(event.groupId) + "）")]))
        await event.accept()
    else:
        await app.sendFriendMessage(Admin, MessageChain.create([Plain("已拒绝" + str(event.supplicant) + "加入" + event.groupName + "（" + str(event.groupId) + "）")]))
        await event.reject("请联系作者QQ:1341283988")


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
        if message.asDisplay().startswith("/test_need_confirm"):
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain("发送 /confirm 以继续运行")
            ]))

            @Waiter.create_using_function([GroupMessage])
            async def waiter(
                    event: GroupMessage, waiter_group: Group,
                    waiter_member: Member, waiter_message: MessageChain
            ):
                if all([
                    waiter_group.id == group.id,
                    waiter_member.id == member.id,
                    waiter_message.asDisplay().startswith("/confirm")
                ]):
                    await app.sendGroupMessage(group, MessageChain.create([Plain("开始执行.")]))
                    return event

            # await asyncio.wait_for(waiter, 60)
            try:
                await asyncio.wait_for(inc.wait(waiter), timeout=10)
            except asyncio.TimeoutError:
                await app.sendGroupMessage(group, MessageChain.create([Plain("命令超时")]))
            await app.sendGroupMessage(group, MessageChain.create([Plain("执行完毕.")]))


@bcc.receiver("GroupMessage", dispatchers=[Kanata([FullMatch("/"), RequireParam(name="command")])])  # 配置工具
async def group_settings(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member, command: MessageChain):
    if member.id == Admin:
        commands = command.asDisplay().split(" ")
        # await app.sendGroupMessage(group, MessageChain.create([Plain("执行命令ing")]))
        if commands[0] == "reload":
            settings = json.load(open("./Settings.json", encoding='utf-8'))
            ScheduleGroup = []
            TestGroup = []
            for i in settings["Group"]:
                if i["function"]["Schedule"]:
                    ScheduleGroup.append(i["id"])
                if i["function"]["test"]:
                    TestGroup.append(i["id"])
            await app.sendGroupMessage(group, MessageChain.create([Plain("重新载入配置文件成功")]))
        elif commands[0] == "addgroup":
            try:
                setting = json.load(open("./Settings.json", encoding='utf-8'))
                if SearchSetting(group.id) is None:
                    NullSetting = [{"name": "", "nickname": group.name, "id": group.id, "blacklist": [2267088317, 1753013648],
                                    "function": {"AutoReply": True, "battlefield": True, "setu": False, "Schedule": True, "Record": True, "bilibili": False, "test": False}}]
                    setting["Group"].extend(NullSetting)
                    json.dump(setting, open("./Settings.json", "w", encoding='utf-8'), ensure_ascii=False, indent=4)
                    await app.sendGroupMessage(group, MessageChain.create([Plain("已成功配置本群")]))
                else:
                    await app.sendGroupMessage(group, MessageChain.create([Plain("本群已有配置文件")]))
            except:
                await app.sendGroupMessage(group, MessageChain.create([Plain("诶呀，发生一个未知的错误(ˉ▽ˉ；)...")]))
        elif commands[0] == "set":
            try:
                if commands[1] in ["AutoReply", "battlefield", "setu", "Schedule", "Record", "bilibili", "test"]:
                    setting = json.load(open("./Settings.json", encoding='utf-8'))
                    if commands[2] == "true":
                        for i in setting["Group"]:
                            if group.id == i["id"]:
                                i["function"][commands[1]] = True
                                json.dump(setting, open("./Settings.json", "w", encoding='utf-8'), ensure_ascii=False, indent=4)
                                await app.sendGroupMessage(group, MessageChain.create([Plain(f"{commands[1]}功能已开启")]))
                    elif commands[2] == "false":
                        for i in setting["Group"]:
                            if group.id == i["id"]:
                                i["function"][commands[1]] = False
                                json.dump(setting, open("./Settings.json", "w", encoding='utf-8'), ensure_ascii=False, indent=4)
                                await app.sendGroupMessage(group, MessageChain.create([Plain(f"{commands[1]}功能已关闭")]))
            except:
                await app.sendGroupMessage(group, MessageChain.create([Plain("参数错误")]))
        elif commands[0] == "status":
            try:
                setting = json.load(open("./Settings.json", encoding='utf-8'))
                counts = len(setting["Group"])
                EndTime = int((time.time()-StartTime)/60)
                await app.sendGroupMessage(group, MessageChain.create([Plain(f"CPU占用率:{Botstatus()[0]}%\n内存占用率:{Botstatus()[1]}%\n目前已在{counts}个群内服务\nMenhera酱已经运行了{EndTime}分钟")]))
            except:
                await app.sendGroupMessage(group, MessageChain.create([Plain("参数错误")]))
        elif commands[0] in ["最近", "服务器", "武器", "载具", "战绩", "绑定", "帮助"]:
            pass
        else:
            await app.sendGroupMessage(group, MessageChain.create([Plain("指令错误")]))


app.launch_blocking()
