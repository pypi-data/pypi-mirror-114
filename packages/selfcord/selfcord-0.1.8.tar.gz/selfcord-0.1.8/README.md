# selfcord
The best Discord selfbot API wrapper.
Enhances discord.py selfbots with new functions.

Edit your Discord client settings, account settings and more with code.

### Example
```python
import discord
import selfcord
from discord.ext import commands

bot = commands.Bot(command_prefix=".", self_bot=True)
selfcord.login("TOKEN")

@bot.event
async def on_ready():
    print("Selfcord Example Selfbot Online.")
    print("Use the prefix '.' to control the bot")

@bot.command(name="changetheme", usage="[light/dark]")
async def changetheme(ctx, theme):
    selfcord.User.setTheme(theme)
    selfcord.Messages.sendMessage(f"Changed your Discord client theme to `{theme}`.", ctx.channel.id)

@bot.command(name="customstatus", usage="[text]")
async def customstatus(ctx, *, text):
    selfcord.User.setCustomStatus(text)
    selfcord.Messages.sendMessage(f"Changed your Discord custom status to `{text}`.", ctx.channel.id)

bot.run("TOKEN", bot=False)
```
