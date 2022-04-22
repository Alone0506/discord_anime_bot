# 導入 Discord.py
import discord
# client 是我們與 Discord 連結的橋樑
client = discord.Client()

# 調用 event 函式庫
print('abcde')


@client.event
# 當機器人完成啟動時
async def on_ready():
    print(f'目前登入身份：{client.user}')

# 調用 event 函式庫


@client.event
# 當有訊息時
async def on_message(message):
    # 排除自己的訊息，避免陷入無限循環
    if message.author == client.user:
        return
    # 如果我們說了「嗨」，機器人就會跟我們說「你好呀」
    if message.content == '嗨':
        await message.channel.send('你好呀')

client.run('你的機器人 TOKEN')  # TOKEN 在剛剛 Discord Developer 那邊「BOT」頁面裡面
