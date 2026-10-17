import discord
from discord.ext import commands
import subprocess
import os

# Placeholder for your bot token
TOKEN = "REDACTED"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def shell(ctx, *, cmd):
    # DANGEROUS: Only use this for your private bot
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    await ctx.send(f"Output:\n{result.stdout}\nError:\n{result.stderr}")

@bot.command()
async def edit(ctx, filepath, *, content):
    with open(filepath, 'w') as f:
        f.write(content)
    await ctx.send(f"File {filepath} updated.")

bot.run(TOKEN)
