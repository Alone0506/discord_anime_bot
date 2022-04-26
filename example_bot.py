import discord
from discord_components import DiscordComponents, ComponentsBot, Button
from discord.ext import commands
from web_spider import Anime
# import web_spider

bot = commands.Bot(command_prefix='$', help_command=None)
DiscordComponents(bot)
token = 'OTY1ODg5MzQxOTkxODI1NDA5.Yl5wjA.QGJVy25aqas2ODQZ6ePAaGRUUn8'
# disord emoji樣式用的跟Twitter一樣
emoji = '\U0001F493'


@bot.event
# 當機器人完成啟動時
async def on_ready():
    print(f'目前登入身份：{bot.user}')
    game = discord.Game('蘿莉')
    # discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    await bot.change_presence(status=discord.Status.online, activity=game)


@bot.command()
async def test(ctx):
    for i in range(5):
        ticket = await ctx.send("_ _", components=[Button(label="Test Button",
                                                          style='1',
                                                          custom_id="test")])
        interaction = await bot.wait_for("button_click", check=lambda i: i.custom_id == "test")
        await interaction.send(content='Test push')


@bot.command()
async def button(ctx):
    for i in range(5):
        await ctx.send("Buttons!", components=[Button(label="Test", custom_id=f"button{i}")])
        interaction = await bot.wait_for("button_click", check=lambda i: i.custom_id == "test")
        await interaction.send(content='Button Test')


# @bot.event
# async def on_button_click(interaction):
#     await interaction.respond(content=f"Button Clicked")


@bot.command()
async def new(ctx):
    info = Anime().newanime_info()
    count = 0
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
            # await ctx.send(embed=embed, components=[Button(label="追隨",
            #                                                style="1",
            #                                                emoji=emoji,
            #                                                custom_id=f"follow_btn{count}")])

            # interaction = await bot.wait_for("button_click", check=lambda i: i.custom_id == f"follow_btn{count}")
            # await interaction.send(content="已追蹤此動漫!", ephemeral=False)
            # count += 1


@bot.command()
async def renew(ctx):
    anime_info = Anime().renew()
    for day, infos in anime_info.items():

        if len(infos[0]) == 2:
            embed = discord.Embed(
                title="預計更新時間", description=infos[0][0], color=0xeee657)
            embed.set_thumbnail(url=infos[0][1])
            await ctx.send(day, embed=embed)
            # add_emoji = await ctx.send(day, embed=embed)
            # await add_emoji.add_reaction(emoji)
            # return

        else:
            for info in infos:
                embed = discord.Embed(
                    title="動畫名稱", description=info[0], color=0xeee657)
                embed.add_field(name="預計更新時間", value=info[1], inline=True)
                embed.add_field(name="集數", value=info[2], inline=True)
                await ctx.send(day, embed=embed)


bot.remove_command('help')


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="指令列表", description="目前的指令如下", color=0xc54343)
    embed.add_field(name="$help", value="列出所有指令", inline=False)
    embed.add_field(name="$new", value="列出已更新的本季新番", inline=False)
    embed.add_field(name="$renew", value="列出這周預訂更新的新番列表", inline=False)
    await ctx.send(embed=embed)

# TOKEN 在剛剛 Discord Developer 那邊「BOT」頁面裡面
bot.run(token)
