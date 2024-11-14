from discord.ext import commands
import discord
import config
import requests


countdown = discord.File

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
@bot.event
async def on_ready():
    channel = bot.get_channel(config.channel_id)
    await channel.send(file=discord.File('C:/Users/W10/Documents/Omarball_OnFire-New/on-fire-omarball/dame.jpg'))

bot.run(config.discord_token)