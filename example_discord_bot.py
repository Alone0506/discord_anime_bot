import discord
import logging
from discord_components import DiscordComponents, ComponentsBot, Button
from discord.ext import commands, tasks

from web_spider import Anime
from handle_follow_info import Handle_follow_info

bot = commands.Bot(command_prefix='$', help_command=None)
DiscordComponents(bot)
# disord emoji樣式用的跟Twitter一樣
emoji = '\U0001F493'
channel_id = 968883865722716240


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8',
                              mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


@bot.event
# 當機器人完成啟動時
async def on_ready():
    print(f'目前登入身份：{bot.user}')
    game = discord.Game('蘿莉')
    # discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    await bot.change_presence(status=discord.Status.online, activity=game)
    check_update.start()


@bot.event
async def on_guild_join(guild):
    global channel_id
    await guild.create_text_channel("anime-channel")
    channel = discord.utils.get(guild.text_channels, name="anime-channel")
    channel_id = channel.id


@tasks.loop(seconds=5.0, count=2)
async def check_update():
    textchannel = bot.get_channel(channel_id)

    new_anime_dict = Anime().newanime_info()
    user_follow = Handle_follow_info()
    user_follow.txt_to_dict()
    user_follow_dict = user_follow.info_dict
    print(new_anime_dict)
    print(user_follow_dict)
    for user in user_follow_dict:
        for episode, anime_name in user_follow_dict[user]:
            if anime_name in new_anime_dict:
                print("true")
                if episode not in new_anime_dict[anime_name]:
                    await textchannel.send("動漫更新拉")
            else:
                print("false")


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
    # print(bot.user.name, bot.user.id)
    # Alone_anime_bot 965889341991825409
    # print(user_name, user_name.id)
    # Alone#7831 432431174397198339
    episode = interaction.custom_id.split(" ", 1)[0]
    anime_name = interaction.custom_id.split(" ", 1)[1]

    add_follow = Handle_follow_info()
    if add_follow.isnew_user(user_name):
        add_follow.add_follow_info_to_txt(user_name, episode, anime_name)
        await interaction.respond(content=f"{user_name}\t已追隨\t{anime_name}", ephemeral=False)
    else:
        if add_follow.isodd_user_follow(user_name, episode, anime_name):
            await interaction.respond(content=f"{user_name}\t此動漫已在追隨列表中", ephemeral=False)
        else:
            add_follow.add_follow_info_to_txt(user_name, episode, anime_name)
            await interaction.respond(content=f"{user_name}\t已追隨\t{anime_name}", ephemeral=False)


# TOKEN 在剛剛 Discord Developer 那邊「BOT」頁面裡面
bot.run('OTY1ODg5MzQxOTkxODI1NDA5.Yl5wjA.f7olQe8czz1orvxB1_tViKrWksU')
