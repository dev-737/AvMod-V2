import discord
import sys
import logging
from typing import Mapping
import typing
import datetime
import asyncio
import random
import json
import os
from discord.ext import commands


import cogs._json
from imports import StaticEmoji, animatedEmojis, statusEmojis

# cwd = Path(__file__).parents[0]
# wd = str(cwd)
# print(f"{cwd}\n-----")

# Define emojis for file

tick = StaticEmoji.tick
online = statusEmojis.anim_online
no = StaticEmoji.no
animatedDnd = statusEmojis.anim_dnd

async def get_prefix(client, message):
    if message.guild is None:
        prefixes = ["av!", "AV!", "!av "]
    elif message.author.id == 701727675311587358:
        #prefixes = ["av!", "Av!", "!av", '']
        data = cogs._json.read_json("mypre")
        prefixes=data["prefixes"]
    elif message.author.id == 736482645931720765: 
        data = cogs._json.read_json("mypre")
        prefixes=data["prefixes"]      
    else:
        prefixes = ["av!", "Av!", "AV!", "!av "]

    return commands.when_mentioned_or(*prefixes)(client, message)
    

# Defining a few things
# secret_file = json.load(open(cwd+'/bot_config/.env'))
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, owner_ids={ 736482645931720765, 701727675311587358}, intents=discord.Intents.all())

bot.remove_command('help')

logging.basicConfig(level=logging.INFO)
bot.blacklisted_users = []
bot.launch_time = datetime.datetime.utcnow()
# bot.cwd = cwd

def callable_pref(bot, message):
    prefix_return = ["av!"]
    return commands.when_mentioned_or(bot.prefixes[message.guild.id])(bot, message)

bot.version = '2.4.4'

@bot.event
async def on_ready():
    print(f"Logged in As {bot.user}.")
    await bot.change_presence(status=discord.Status.idle,
                              activity=discord.Activity(type=discord.ActivityType.listening, name="av!help"))
    chan = await bot.fetch_channel(972083876811931669)
    msg = await chan.fetch_message(972084220304457768)
    try:
        data = cogs._json.read_json("restart")
        chan1 = data["channelId"]
        msg1 = data["messageId"]

        chan2 = await bot.fetch_channel(chan1)
        msg2 = await chan2.fetch_message(msg1)
        print("\n")
        
        await msg2.edit(content='Restarted!')
        data["channelId"] = ""
        data["messageId"] = ""
        cogs._json.write_json(data, "restart")

    except Exception:
        pass
    await msg.edit(content=f"""
**{online} Online**
------------------------------

{tick} Cogs: Loaded
------------------------------

{tick} Commands: Fully Functional 
------------------------------

{tick}  Maintenance Mode: False
------------------------------

{tick} Errors: 0""")


@bot.event
async def on_message(message):
    # Ignore messages sent by yourself
    if message.author.id == bot.user.id:
        return

    # A way to blacklist users from the bot by not processing commands if the author is in the blacklisted_users list
    data = cogs._json.read_json("blacklist")
    if message.author.id in data["blacklistedUsers"]:
        return
    if message.guild.id == 801671810730426418:
      await message.channel.send("Guild is blacklisted for violating ToS.")
      return

    # Whenever the bot is tagged, respond with its prefix #in message.content
    if message.content.startswith(f"<@!{bot.user.id}>"):
        data = cogs._json.read_json('prefixes')
        if str(message.guild.id) in data:
            prefix = data[str(message.guild.id)]
        else:
            prefix = 'av!'
        await message.channel.send(f"My prefix here is `{prefix}`")

    await bot.process_commands(message)



    
bot.load_extension("jishaku")

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"



@bot.event
async def on_message_edit(before, after):
    try:
      await bot.process_commands(after) 
    except:
        return



"""deletelog={}

@bot.event
async def on_message_delete(message):
    if message.id in deletelog:
        dellog = deletelog[message.id]
        await dellog.delete()
        del deletelog[message.id]"""



  
@bot.command(hidden=True, aliases=['rs'])
@commands.is_owner()
async def restart(ctx):
  chan = await bot.fetch_channel(972083876811931669)
  msg = await chan.fetch_message(972084220304457768)
  message = await ctx.reply("Restarting...")

  data = cogs._json.read_json("restart")
  data["channelId"] = ctx.channel.id
  data["messageId"] = message.id
  cogs._json.write_json(data, "restart")
  
  
  await msg.edit(content=f"""
**{animatedDnd} Restarting...**
------------------------------

{no} Cogs: Unloaded
------------------------------

{no} Commands: Error 
------------------------------

{no} Maintenance Mode: Failed
------------------------------

{tick} Errors: 0""")

  await bot.close()
  python = sys.executable
  os.execl(python, python, *sys.argv)




if __name__ == '__main__':
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    for filename in os.listdir('./cogs/'):
        if filename.endswith(".py") and not filename.startswith("_"):
            bot.load_extension(f"cogs.{filename[:-3]}")
    token = os.environ.get("token")
    bot.run(token)
