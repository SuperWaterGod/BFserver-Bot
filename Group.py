# -*-coding:utf-8-*-
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain

from graia.application.friend import Friend

from graia.application.message.elements.internal import At, Plain, Image
from graia.application.session import Session
from graia.application.group import Group, Member, Optional

import asyncio
import re

from match import AutoReply
from battlefield import BFservers, Binding
from Botstatus import Botstatus

WhiteGroup = {454375504, 863715876, 306800820, 1136543076}
WhiteId = {1341283988}

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
            await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("\n" + BFservers(member.id, MessageStr))]))
        elif MessageStr.startswith("/战绩"):
            MessageGet = BFservers(member.id, MessageStr)
            if MessageGet.startswith("头像"):
                avatar = re.findall('头像:(.*)', MessageGet)[0]
                MessageStr = re.findall('昵称:[\s\S]*', MessageGet)[0]
                await app.sendGroupMessage(group, MessageChain.create(
                    [At(member.id), Image.fromNetworkAddress(avatar), Plain("\n" + MessageStr)]))
            else:
                await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("\n" + MessageGet)]))

        elif MessageStr.startswith("/帮助"):
            await app.sendGroupMessage(group, MessageChain.create(
                [At(member.id), Plain("\n" + BFservers(member.id, MessageStr))]))
        elif MessageStr.startswith("/绑定"):
            await app.sendGroupMessage(group, MessageChain.create(
                [At(member.id), Plain(Binding(member.id, MessageStr.replace("/绑定", "").replace(" ", "")))]))


@bcc.receiver("GroupMessage")  # 自动发送色图
async def pixiv_Group_listener(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    if message.asDisplay().find("色图") >= 0 or message.asDisplay().find("涩图") >= 0:
        await app.sendGroupMessage(group, MessageChain.create(
            [At(member.id), Image.fromNetworkAddress("https://api.ixiaowai.cn/api/api.php")]))


@bcc.receiver("GroupMessage")  # 自动回复群消息及表情
async def AutoReply_Group_listener(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    if AutoReply(message.asDisplay()).startswith("./Menhera/"):
        await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile(AutoReply(message.asDisplay()))]))
    elif AutoReply(message.asDisplay()) == "":
        pass
    else:
        await app.sendGroupMessage(group, MessageChain.create([Plain(AutoReply(message.asDisplay()))]))


@bcc.receiver("MemberJoinEvent")  # 新人加入群
async def Member_join(app: GraiaMiraiApplication, group: Group, member: Member):
    await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("欢迎加入" + str(group.name) + "\n"
                                                                                                           "请将群昵称改为游戏ID!")]))


@bcc.receiver("MemberLeaveEventKick")  # 群员被T
async def Member_kick(app: GraiaMiraiApplication, group: Group, member: Member):
    await app.sendGroupMessage(group, MessageChain.create(
        [Plain(str(operator.name) + "(" + str(operator.id) + ")" + "因语言过激，被管理员移出了本群。")]))


@bcc.receiver("MemberLeaveEventQuit")  # 群员离开
async def Member_quit(app: GraiaMiraiApplication, group: Group, member: Member):
    await app.sendGroupMessage(group, MessageChain.create(
        [Plain("一根丧失梦想的薯条" + str(member.name) + "(" + str(member.id) + ")" + "心灰意冷地离开了本群")]))


@bcc.receiver("FriendMessage")  # 自动回复好友消息及表情
async def AutoReply_Friend_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    if AutoReply(message.asDisplay()).startswith("./Menhera/"):
        await app.sendFriendMessage(friend, MessageChain.create([Image.fromLocalFile(AutoReply(message.asDisplay()))]))
    elif AutoReply(message.asDisplay()) == "":
        pass
    else:
        await app.sendFriendMessage(friend, MessageChain.create([Plain(AutoReply(message.asDisplay()))]))


app.launch_blocking()