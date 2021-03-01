# -*-coding:utf-8-*-

AutoReplyMessage = [
    ['爬', '爬！'], ['爪巴', '再这样我可要生气咯！'], ['傻逼机器人', '说的就是你！'], ['不够色', '再色群就没了！'], ['彳亍', "我可能干了~(●'◡'●)"]
]
AutoReplyImage = [
    ['盯', '1.jpg'],
    ['偷看', '3.jpg'],
    ['叮叮', '4.jpg'],
    ['棒', '6.jpg'],
    ['good', '5.jpg'],
    ['咚咚', '9.jpg'],
    ['爱你', '8.jpg'],
    ['好累', '11.jpg'],
    ['自闭', '12.jpg'],
    ['真的吗', '13.jpg'],
    ['早上好', '15.jpg'],
    ['晚安', '16.jpg'],
    ['睡觉', '16.jpg'],
    ['好闲', '17.jpg'],
    ['喂喂', '18.jpg'],
    ['。。。', '19.jpg'],
    ['啊啊啊啊啊', '20.jpg'],
    ['可爱', '21.jpg'],
    ['呜呜呜', '24.jpg'],
    ['疑问', '25.jpg'],
    ['饿了', '26.jpg'],
    ['嚼', '27.jpg'],
    ['哎', '30.jpg'],
    ['OK', '31.jpg'],
    ['不可能', '32.jpg'],
    ['辛苦了', '34.jpg'],
    ['拜托了', '36.jpg'],
    ['喵', '45.jpg'],
    ['tql', '46.jpg'],
    ['respect', '47.jpg'],
    ['明白了', '54.jpg'],
    ['好可怕', '65.jpg'],
    ['加油', '77.jpg'],
    ['恋童', '78.jpg'],
    ['炼铜', '78.jpg'],
    ['就是你', '85.jpg'],
    ['啊这', '92.jpg'],
    ['az', '92.jpg'],
    ['阿这', '92.jpg'],
    ['吃药了', '93.jpg'],
    ['好臭', '109.jpg'],
    ['瑟瑟发抖', '118.jpg'],
    ['哼哼', '136.png'],
    ['有了', '160.png'],
    ['战神', '135.jpg'],
    ['大佬', '140.jpg'],
    ['dalao', '140.jpg']
]


def AutoReply(message):
    a = 0
    for i in range(len(AutoReplyMessage)):
        if message.find(AutoReplyMessage[i][0]) >= 0:
            a = 1
            return AutoReplyMessage[i][1]
    for i in range(len(AutoReplyImage)):
        if message.find(AutoReplyImage[i][0]) >= 0:
            a = 1
            return "./Menhera/" + AutoReplyImage[i][1]
    if a == 0:
        return ""
