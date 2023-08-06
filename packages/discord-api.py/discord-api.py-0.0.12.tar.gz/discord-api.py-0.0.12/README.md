# discord-api.py

## introduction

This is discord api wrapper.

Easy to create a bot

## setup

```bash
discord-api setup main
```

## extension

If you want to create extention module.

Please do like this name.

`discord-api-{name}`

## sample

```python
from discord_api import Client, Command

client = Client(log = False)

client.add_command(Command("ping", "pong."))

@client.event
async def on_ready():
    print("ready")

@client.event
async def on_interaction(i):
    await i.send("Pong!", True)

client.run("token")
```

## license

Watch a `LICENSE`!
