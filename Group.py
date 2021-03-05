# -*-coding:utf-8-*-
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
from graia.application.friend import Friend
from graia.application.message.elements.internal import At, Plain, Image, Voice
from graia.application.session import Session
from graia.application.group import Group, Member, Optional

import asyncio
import re
import json
from pypinyin import lazy_pinyin

from match import AutoReply, AutoVoice
from battlefield import BFservers, Binding
from Botstatus import Botstatus
from XunProxy import aioRequest

from config import LoliconKey, Admin

WhiteGroup = {454375504, 863715876, 306800820, 1136543076, 781963214}
WhiteId = {1341283988}
BanSetu = {1136543076, 781963214}

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop, use_dispatcher_statistics=True, use_reference_optimization=True)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080",  # 填入 httpapi 服务运行的地址
        authKey="INITKEYfiyhSQvQ",  # 填入 authKey
        account=2781851088,  # 你的机器人的 qq 号
        websocket=True  # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)


@bcc.receiver("GroupMessage")
async def battlefield(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    MessageStr = message.asDisplay()
    if group.id in WhiteGroup:
        if MessageStr.startswith("/服务器") or MessageStr.startswith("/武器") or MessageStr.startswith(
                "/载具") or MessageStr.startswith("/最近"):
            # if member.id in WhiteId:
            await app.sendGroupMessage(group, MessageChain.create(
                [At(member.id), Plain("\n" + await BFservers(member.id, MessageStr))]))
        elif MessageStr.startswith("/战绩"):
            MessageGet = await BFservers(member.id, MessageStr)
            if MessageGet.startswith("头像"):
                avatar = re.findall('头像:(.*)', MessageGet)[0]
                MessageStr = re.findall('昵称:[\s\S]*', MessageGet)[0]
                await app.sendGroupMessage(group, MessageChain.create(
                    [At(member.id), Image.fromNetworkAddress(avatar), Plain("\n" + MessageStr)]))
            else:
                await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("\n" + MessageGet)]))

        elif MessageStr.startswith("/帮助"):
            await app.sendGroupMessage(group, MessageChain.create(
                [At(member.id), Plain("\n" + await BFservers(member.id, MessageStr))]))
        elif MessageStr.startswith("/绑定"):
            await app.sendGroupMessage(group, MessageChain.create(
                [At(member.id), Plain(Binding(member.id, MessageStr.replace("/绑定", "").replace(" ", "")))]))


@bcc.receiver("GroupMessage")  # 自动发送色图
async def pixiv_Group_listener(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    pinyinStr = ""
    for i in range(len(lazy_pinyin(message.asDisplay()))):
        pinyinStr += lazy_pinyin(message.asDisplay())[i]
    if pinyinStr.find("setu") >= 0:
        if group.id not in BanSetu:
            try:
                url = "https://api.lolicon.app/setu/?apikey=" + LoliconKey[0]  # 1号api
                data = json.loads(await aioRequest(url))
                if data['code'] == 0:
                    messageId = await app.sendGroupMessage(group, MessageChain.create(
                        [At(member.id), Image.fromNetworkAddress(data['data'][0]['url'])]))
                    await asyncio.sleep(60)
                    await app.revokeMessage(messageId)
                elif data['code'] == 429:
                    url = "https://api.lolicon.app/setu/?apikey=" + LoliconKey[1]  # 2号api
                    data = json.loads(await aioRequest(url))
                    if data['code'] == 0:
                        messageId = await app.sendGroupMessage(group, MessageChain.create(
                            [At(member.id), Image.fromNetworkAddress(data['data'][0]['url'])]))
                        await asyncio.sleep(60)
                        await app.revokeMessage(messageId)
                    else:
                        await app.sendGroupMessage(group,
                                                   MessageChain.create([At(member.id), Plain("今天发的已经够多了，明天再来吧~")]))
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


@bcc.receiver("MemberJoinEvent")  # 新人加入群
async def Member_join(app: GraiaMiraiApplication, group: Group, member: Member):
    await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("欢迎加入" + str(group.name) + "\n"
                                                                                                           "请将群昵称改为游戏ID!")]))


@bcc.receiver("MemberLeaveEventKick")  # 群员被T
async def Member_kick(app: GraiaMiraiApplication, group: Group, member: Member = "target"):
    await app.sendGroupMessage(group, MessageChain.create(
        [Plain(str(member.name) + "(" + str(member.id) + ")" + "因语言过激，被管理员移出了本群。")]))


@bcc.receiver("MemberLeaveEventQuit")  # 群员离开
async def Member_quit(app: GraiaMiraiApplication, group: Group, member: Member):
    await app.sendGroupMessage(group, MessageChain.create(
        [Plain("一根丧失梦想的薯条" + str(member.name) + "(" + str(member.id) + ")" + "心灰意冷地离开了本群")]))


@bcc.receiver("BotMuteEvent")  # 机器人被禁言
async def Bot_muted(app: GraiaMiraiApplication, group: Group, member: Member):
    await app.sendFriendMessage(Admin,
                                MessageChain.create([Plain("已被" + str(member.name) + "在" + str(group.name) + "禁言")]))


@bcc.receiver("BotUnmuteEvent")  # 机器人解除禁言
async def Bot_unmuted(app: GraiaMiraiApplication, group: Group, member: Member):
    await app.sendFriendMessage(Admin,
                                MessageChain.create([Plain("已被" + str(member.name) + "在" + str(group.name) + "解除禁言")]))


@bcc.receiver("FriendMessage")  # 自动回复好友消息及表情
async def AutoReply_Friend_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    if AutoReply(message.asDisplay()).startswith("./Menhera/"):
        await app.sendFriendMessage(friend, MessageChain.create([Image.fromLocalFile(AutoReply(message.asDisplay()))]))
    elif AutoReply(message.asDisplay()) == "":
        pass
    else:
        await app.sendFriendMessage(friend, MessageChain.create([Plain(AutoReply(message.asDisplay()))]))


app.launch_blocking()
