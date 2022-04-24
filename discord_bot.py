import discord
from discord.ext import commands

from web_spider import Anime
# import web_spider

bot = commands.Bot(command_prefix='$', help_command=None)

# 調用 event 函式庫


@bot.event
# 當機器人完成啟動時
async def on_ready():
    print(f'目前登入身份：{bot.user}')
    game = discord.Game('努力學習py中')
    # discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    await bot.change_presence(status=discord.Status.online, activity=game)


@bot.command()
async def new(ctx):
    info = Anime().newanime_info()
    if isinstance(info, int):
        await ctx.send("錯誤代碼 : ", info)
        return
    else:
        for i in range(len(info[0])):
            embed = discord.Embed(
                title="動畫名稱", description=info[0][i], color=0xeee657)
            embed.add_field(name="觀看次數", value=info[1][i], inline=True)
            embed.add_field(name="最新集數", value=info[2][i], inline=True)
            embed.add_field(name="最新一集更新時間", value=info[3][i], inline=False)
            embed.add_field(name="動畫網址", value=info[4][i], inline=False)
            embed.set_thumbnail(url=info[5][i])
            embed.set_image(url=info[5][i])
            await ctx.send(embed=embed)
        return


@bot.command()
async def new(ctx):
    info = Anime().newanime_info()
    if isinstance(info, int):
        await ctx.send("錯誤代碼 : ", info)
        return
    else:
        pass


bot.remove_command('help')


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="指令列表", description="目前的指令如下", color=0xc54343)
    embed.add_field(name="$help", value="列出所有指令", inline=False)
    embed.add_field(name="$new", value="列出所有本季新番", inline=False)

    await ctx.send(embed=embed)

# TOKEN 在剛剛 Discord Developer 那邊「BOT」頁面裡面
bot.run('OTY1ODg5MzQxOTkxODI1NDA5.Yl5wjA.bibl9p9ATFlFqaPLC02cTfaiUIY')
