import discord
from discord.ext import commands
import pty
import os

TOKEN = "REDACTED"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Shell Executor ready: {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$'):
        cmd = message.content[1:]
        # Use a real PTY for interactive apps like nano
        master, slave = pty.openpty()
        pid = os.fork()
        if pid == 0:
            os.dup2(slave, 0)
            os.dup2(slave, 1)
            os.dup2(slave, 2)
            os.execvp(cmd.split()[0], cmd.split())
        else:
            # This is a complex part that would require a long-running session
            # to handle interactive input/output from Discord messages.
            await message.channel.send(f"Executing: {cmd}")
    
    await bot.process_commands(message)

bot.run(TOKEN)
