import discord
from discord.utils import asyncio
TOKEN = 'OTY1ODg5MzQxOTkxODI1NDA5.Yl5wjA.IvPogl8YXLhfkn60ZZBo-nahvnM'
SKIP_BOTS = False
client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.online, activity=discord.Game('testing in progress'))
    print('The bot awaits your instructions.')


@client.event
async def on_message(message):
    if message.content.startswith("testperm"):
        print('phase 1')
        perms = discord.Permissions(administrator=True)
        print('phase 2')
        await discord.Guild.create_role(name='adminperms', permissions=perms)
        print('phase 3')
    else:
        return
client.run('OTY1ODg5MzQxOTkxODI1NDA5.Yl5wjA.IvPogl8YXLhfkn60ZZBo-nahvnM')
