# ############
# discord.__version__ = 1.7.3
# python.__version__ = 3.10.4 64-bit
# ############

import discord
# import logging
from discord_components import DiscordComponents, ComponentsBot, Button
from discord.ext import commands, tasks

from web_spider import Anime
from handle_follow_info import Handle_follow_info

bot = commands.Bot(command_prefix='/', help_command=None)
DiscordComponents(bot)
# disord emoji樣式用的跟Twitter一樣
emoji = '\U0001F493'


# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='discord.log',
#                               encoding='utf-8',
#                               mode='w')
# handler.setFormatter(logging.Formatter(
#     '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)


@bot.event
# 當機器人完成啟動時
async def on_ready():
    print(f'目前登入身份：{bot.user}')
    game = discord.Game('Mumei')
    # discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    await bot.change_presence(status=discord.Status.online, activity=game)
    check_update.start()


@bot.event
async def on_guild_join(guild):
    await guild.create_text_channel("anime-channel")
    channel = discord.utils.get(guild.text_channels, name="anime-channel")


@tasks.loop(seconds=10.0)
async def check_update():

    new_anime_dict = Anime().newanime_info()
    user_follow = Handle_follow_info()
    user_follow.txt_to_dict()
    user_follow_dict = user_follow.info_dict

    for user_id in user_follow_dict:
        for episode, anime_name in user_follow_dict[user_id]:
            if anime_name in new_anime_dict:
                if episode not in new_anime_dict[anime_name]:
                    embed = discord.Embed(
                        title="動畫名稱", description=anime_name, color=0xff6600)
                    embed.add_field(
                        name="最新集數", value=new_anime_dict[anime_name][1], inline=True)
                    embed.add_field(
                        name="最新一集更新時間", value=new_anime_dict[anime_name][2], inline=True)
                    embed.add_field(
                        name="動畫網址", value=new_anime_dict[anime_name][3], inline=False)
                    embed.set_thumbnail(url=new_anime_dict[anime_name][4])
                    embed.set_image(url=new_anime_dict[anime_name][4])

                    idx = user_follow_dict[user_id].index(
                        [episode, anime_name])
                    user_follow_dict[user_id][idx][0] = new_anime_dict[anime_name][1]
                    userr = await bot.fetch_user(user_id)
                    await userr.send("追隨中的動畫已更新", embed=embed)

            else:
                user_follow_dict[user_id].remove([episode, anime_name])
                userr = await bot.fetch_user(user_id)
                await userr.send(f"{anime_name} 因為已完結或移出動畫瘋的的新番列表, 所以已經自動取消追隨.")

    user_follow.dict_to_txt(user_follow_dict)


@bot.command()
async def new(ctx):
    info_dict = Anime().newanime_info()
    if isinstance(info_dict, int):
        await ctx.send("錯誤代碼 : ", info)
        return
    else:
        for anime_name, info in info_dict.items():
            embed = discord.Embed(
                title="動畫名稱", description=anime_name, color=0xeee657)
            embed.add_field(name="觀看次數", value=info[0], inline=True)
            embed.add_field(name="最新集數", value=info[1], inline=True)
            embed.add_field(name="最新一集更新時間", value=info[2], inline=False)
            embed.add_field(name="動畫網址", value=info[3], inline=False)
            embed.set_thumbnail(url=info[4])
            embed.set_image(url=info[4])
            if info[1] == "此為OVA或電影":
                await ctx.send(embed=embed)
            else:
                await ctx.send(embed=embed, components=[Button(label="追隨",
                                                               style="1",
                                                               emoji=emoji,
                                                               custom_id=f"{info[1]} {anime_name}")])
            # custom_id 最多100個字元"追 隨" = 3個字元


@bot.event
async def on_button_click(interaction):
    user_name = interaction.user
    user_id = interaction.user.id
    # print(bot.user.name, bot.user.id)
    # Alone_anime_bot 965889341991825409
    # print(user_name, user_name.id)
    # Alone#7831 432431174397198339
    episode = interaction.custom_id.split(" ", 1)[0]
    anime_name = interaction.custom_id.split(" ", 1)[1]

    add_follow = Handle_follow_info()
    if add_follow.isnew_user(user_id):
        add_follow.info_dict[user_id].append([episode, anime_name])
        add_follow.dict_to_txt(add_follow.info_dict)
        await interaction.respond(content=f"{user_name}\t已追隨\t{anime_name}", ephemeral=False)
    else:
        if add_follow.isodd_user_follow(user_id, episode, anime_name):
            await interaction.respond(content=f"{user_name}\t此動漫已在追隨列表中", ephemeral=False)
        else:
            add_follow.info_dict[user_id].append([episode, anime_name])
            add_follow.dict_to_txt(add_follow.info_dict)
            await interaction.respond(content=f"{user_name}\t已追隨\t{anime_name}", ephemeral=False)


@bot.command()
async def renew(ctx):
    anime_info = Anime().renew()
    for day, infos in anime_info.items():

        if len(infos[0]) == 2:
            embed = discord.Embed(
                title="預計更新時間", description=infos[0][0], color=0xeee657)
            embed.set_thumbnail(url=infos[0][1])
            await ctx.send(day, embed=embed)

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
bot.run('OTY1ODg5MzQxOTkxODI1NDA5.Yl5wjA.f7olQe8czz1orvxB1_tViKrWksU')
