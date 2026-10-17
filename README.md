# DiscordBots

Two single-file Discord bots written in Python with `discord.py`. Both exist for the same reason: to reach the machine they run on from a Discord client, so that a shell command or a quick file edit can be issued from a phone without opening an SSH session. `ai_assistant/bot.py` runs a shell command or overwrites a file on request; `shell_executor/bot.py` is a sketch of the same idea built around a real pseudo-terminal so that interactive programs could one day be driven from chat.

## Where it is used

These bots are the earliest, simplest form of the "control my laptop from Discord" idea that the later `abrar-assistant` and `system-control-bot` projects grew out of. They are meant for a private server where the only members are the owner's own accounts.

## How it works

### `ai_assistant/bot.py`

- Creates a `commands.Bot` with prefix `!` and the message-content intent.
- `!shell <cmd>` runs the text through `subprocess.run(cmd, shell=True)` with output captured and replies with both stdout and stderr in one message.
- `!edit <filepath> <content>` opens the given path for writing (creating or truncating it) and writes the rest of the message into it, then confirms.
- The bot token is a constant named `TOKEN` at the top of the file.

### `shell_executor/bot.py`

- Creates a `commands.Bot` with prefix `$`.
- In `on_message`, any message starting with `$` is treated as a command: the bot opens a pseudo-terminal with `pty.openpty()`, forks, and in the child redirects stdin/stdout/stderr to the PTY slave and `execvp`s the command.
- The parent process only replies `Executing: <cmd>`. Nothing is read back from the PTY master and no input is forwarded, so the output never reaches Discord; the file documents that a long-running session manager would be needed for that.
- The bot token is likewise a constant named `TOKEN`.

Neither bot has configuration files, persistence or external services beyond Discord itself.

| File | Role |
|---|---|
| `ai_assistant/bot.py` | `!shell` and `!edit` commands, blocking subprocess execution |
| `shell_executor/bot.py` | PTY-based command launcher, output not yet relayed |

## Setup

Requirements: Python 3.8+, a Discord application with a bot user and the Message Content intent enabled.

```bash
cd ~/Workspace/DiscordBots
python3 -m venv venv && source venv/bin/activate
pip install discord.py
```

Open the bot file you want to run and replace the `TOKEN` constant with your own bot token (the values in the files are placeholders and must be changed). A safer pattern is to read it from the environment:

```python
import os
TOKEN = os.environ["DISCORD_BOT_TOKEN"]
```

## Usage

```bash
python ai_assistant/bot.py
# or
python shell_executor/bot.py
```

In Discord (ai_assistant):

```
!shell uptime
!shell ls ~/Downloads | head
!edit /tmp/notes.txt remember to back up the VM tonight
```

In Discord (shell_executor):

```
$nano /tmp/test.txt      -> bot replies "Executing: nano /tmp/test.txt"
```

## Project structure

```
DiscordBots/
├── ai_assistant/
│   └── bot.py        # !shell, !edit
└── shell_executor/
    └── bot.py        # $<cmd> in a PTY (launch only)
```

## Limitations and notes

- There is no authorisation check at all: anyone who can post in a channel the bot reads can run commands as the user the bot runs as. Only use these in a server where you are the sole member.
- `!shell` uses `shell=True` and blocks the event loop until the command finishes; long or interactive commands will stall the bot.
- `!edit` overwrites files without confirmation and does not restrict the path.
- `shell_executor` forks a child process for every `$` message and never reaps it or relays its output; it is a prototype, not a working remote terminal.
- Discord messages are limited to 2000 characters; large outputs from `!shell` will fail to send.
- Tokens are hard-coded in the source. Rotate any token that has ever been committed and move it to an environment variable before publishing.
