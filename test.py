import discord
from discord.ext import commands
import asyncio
TOKEN = '---'
bot = commands.Bot(command_prefix='!!')
reactions = [':white_check_mark:', ':stop_sign:', ':no_entry_sign:']


@bot.event
async def on_ready():
    print('Bot is ready.')


@bot.command()
async def bug(ctx, desc=None, rep=None):
    user = ctx.author
    await ctx.author.send('```Please explain the bug```')
    responseDesc = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=300)
    description = responseDesc.content
    await ctx.author.send('````Please provide pictures/videos of this bug```')
    responseRep = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=300)
    replicate = responseRep.content
    embed = discord.Embed(title='Bug Report', color=0x00ff00)
    embed.add_field(name='Description', value=description, inline=False)
    embed.add_field(name='Replicate', value=replicate, inline=True)
    embed.add_field(name='Reported By', value=user, inline=True)
    adminBug = bot.get_channel(733721953134837861)
    # Add 3 reaction (different emojis) here bot.run(TOKEN)
    await adminBug.send(embed=embed)
