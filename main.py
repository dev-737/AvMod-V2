from flask import Flask
from threading import Thread
from datetime import datetime

app=Flask("")
app.config["DEBUG"] = True

@app.route("/")
def index():
    return "<h1>Bot is running</h1>"

Thread(target=app.run,args=("0.0.0.0",8080)).start()

import ast
import discord
import sys
import logging
from typing import Mapping
import typing
import asyncio
import random
import os
from discord_slash import SlashCommand
from discord_slash import SlashContext
from discord_slash import SlashCommandOptionType
from discord_slash.utils import manage_commands
from discord.ext import commands


import cogs._json


class MyContext(commands.Context):
    async def tick(self, value):
        # reacts to the message with an emoji
        # depending on whether value is True or False
        # if its True, it'll add a green check mark
        # otherwise, it'll add a red cross mark
        emoji = '\N{WHITE HEAVY CHECK MARK}' if value else '\N{CROSS MARK}'
        try:
            # this will react to the command author's message
            await self.message.add_reaction(emoji)
        except discord.HTTPException:
            # sometimes errors occur during this, for example
            # maybe you dont have permission to do that
            # we dont mind, so we can just ignore them
            pass

    async def embed(self, message=None):
      if message:
        embed=discord.Embed(description=message)
        return await self.send(embed=embed)
      else:
        embed=discord.Embed(color=discord.Colour.random())
        embed.set_footer(text=f"HI")
        return await self.send(embed=embed)

class MyBot(commands.Bot):
    async def get_context(self, message, *, cls=MyContext):
        # when you override this method, you pass your new Context
        # subclass to the super() method, which tells the bot to
        # use the new MyContext class
        return await super().get_context(message, cls=cls)

def get_prefix(bot, message):
    data = cogs._json.read_json('prefixes')
    if not str(message.guild.id) in data:
        return commands.when_mentioned_or('av!')(bot, message)
    return commands.when_mentioned_or(data[str(message.guild.id)])(bot, message)


    


intents = discord.Intents.all()
bot = MyBot(command_prefix=get_prefix, case_insensitive=True, owner_id=701727675311587358)
slash = SlashCommand(bot, auto_register=True)

bot.remove_command('help')

logging.basicConfig(level=logging.INFO)
bot.blacklisted_users = []
bot.version = '2.1.0'
@slash.slash(name="echo", options=[manage_commands.create_option("string", "A random string.", SlashCommandOptionType.STRING, True)])
async def _echo(ctx, string):
    embed=discord.Embed(description=string, color=discord.Colour.random())
    await ctx.send(embeds=[embed])


@bot.event
async def on_guild_join(guild):
  goal_channel = bot.get_channel(799622782362714142)
  invite=await guild.text_channels[0].create_invite(reason="Privacy Policy.")
  em=discord.Embed(title=f"<:join:790914850863317003> Join" , description=f"Thank you for adding AvMod, **{guild.name}**! <a:fox_cheer:769411352073863199>", color=discord.Colour.random())
  em.set_footer(text=f'GUILD ID: {guild.id}')
  em.set_author(name=guild.name, icon_url=guild.icon_url, url=invite)
  await goal_channel.send(embed=em)

@bot.event
async def on_guild_remove(guild):
  goal_channel = bot.get_channel(799622782362714142)
  em=discord.Embed(title=f"<a:pepecryfall:768353435106934794> Leave" , description=f"I was kicked from **{guild.name}**! How rude of them. <:sad:796576463063089203>", color=discord.Colour.random())
  em.set_footer(text=f'GUILD ID: {guild.id}')
  em.set_author(name=guild.name, icon_url=guild.icon_url)
  await goal_channel.send(embed=em)
  


@bot.event
async def on_command_error(ctx, error):
    ignored = (commands.CommandNotFound)
    if isinstance(error, ignored):
        return
    if isinstance(error, commands.CommandOnCooldown):
        message = ctx.message
        await message.add_reaction("⏰")

    elif isinstance(error, commands.MissingPermissions):
        await ctx.message.add_reaction("❌")
        raise error



@bot.command()
async def guess(ctx, number: int):
    """ Guess a random number from 1 to 6. """
    # explained in a previous example, this gives you
    # a random number from 1-6
    value = random.randint(1, 6)
    # with your new helper function, you can add a
    # green check mark if the guess was correct,
    # or a red cross mark if it wasnt
    await ctx.tick(number == value)

@bot.event
async def on_ready():
    print(f"READY!!!!!\n\n~~Logged in As {bot.user}~~")
    await bot.change_presence(status=discord.Status.dnd,
                              activity=discord.Activity(type=discord.ActivityType.listening, name=f"av!help"))


@bot.event
async def on_message(message):
    # Ignore messages sent by yourself
    if message.author.id == bot.user.id:
        return

    # A way to blacklist users from the bot by not processing commands if the author is in the blacklisted_users list
    if message.author.id in bot.blacklisted_users:
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





@bot.command()
@commands.is_owner()
async def unload(ctx, cog):
    if cog.endswith(".py") and not cog.startswith("_"):
        await ctx.send(f"Unloading `{cog}`...")
        bot.unload_extension(f'cogs.{cog[:-3]}')
        await ctx.send(f'the `{cog}` cog has now been unloaded!')

    elif not cog.endswith(".py") and not cog.startswith("_"):
        await ctx.send(f"Unload `{cog}`...")
        bot.unload_extension(f'cogs.{cog}')
        await ctx.send(f'the `{cog}` cog has now been unloaded!')

    else:
        await ctx.send('Excetuion Failed. Reason: Unknown Cog')

    print(
        f"{ctx.author.id} attempted to unload an extension named {cog}.\n----------------------------------")


@bot.command()
@commands.is_owner()
async def load(ctx, cog):
    if cog.endswith(".py") and not cog.startswith("_"):
        await ctx.send(f"Loading `{cog}`...")
        bot.load_extension(f'cogs.{cog[:-3]}')
        await ctx.send(f'the `{cog}` cog has now been loaded!')

    elif not cog.endswith(".py") and not cog.startswith("_"):
        await ctx.send(f"Loading `{cog}`...")
        bot.load_extension(f'cogs.{cog}')
        await ctx.send(f'the `{cog}` cog has now been loaded!')

    else:
        await ctx.send('Excetuion Failed. Reason: Unknown Cog')

    print(
        f"{ctx.author.id} attempted to load an extension named {cog}.\n----------------------------------")



@bot.command(aliases=['rl'])
@commands.is_owner()
async def reload(ctx, cog):
    if cog == 'all':
        for filename in os.listdir('./cogs/'):
            if filename.endswith(".py") and not filename.startswith("_"):
                bot.unload_extension(f'cogs.{filename[:-3]}')
                bot.load_extension(f'cogs.{filename[:-3]}')
        else:
            msg = await ctx.send("<a:Loading:786176377757368330> Getting cogs...")
            await msg.edit(content="📤Unloading all cogs...")
            await msg.edit(content="📥Loading all cogs...")
            await msg.edit(content="🔁Realoaded all cogs.")
            await ctx.message.add_reaction("✅")
            await asyncio.sleep(3)
            await msg.delete()

    elif cog.endswith(".py") and not cog.startswith("_"):
        bot.unload_extension(f'cogs.{cog[:-3]}')
        bot.load_extension(f'cogs.{cog[:-3]}')
        msg = await ctx.send(f"📤Unloading `{cog}`...")
        await msg.edit(content=f"📥Loading `{cog}`...")
        await msg.edit(content=f'🔁`{cog}` cog has now been reloaded!')
        await ctx.message.add_reaction("✅")
        await asyncio.sleep(3)
        await msg.delete()

    elif not cog.endswith(".py") and not cog.startswith("_"):
        bot.unload_extension(f'cogs.{cog}')
        bot.load_extension(f'cogs.{cog}')
        msg = await ctx.send(f"📤Unloading `{cog}`...")
        await msg.edit(content=f"📥Loading `{cog}`...")
        await msg.edit(content=f'🔁`{cog}` cog has now been reloaded!')
        await ctx.message.add_reaction("✅")
        await asyncio.sleep(3)
        await msg.delete()

    else:
        await ctx.send('Excetuion Failed. Reason: Unknown Cog')

        print(f"{ctx.author.id} attempted to reload an extension named {cog}.\n----------------------------------")


def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


@bot.command(name="eval")
@commands.is_owner()
async def eval_fn(ctx, *, cmd):
    fn_name = "_eval_expr"

    cmd = cmd.strip("` ")
    cmd = cmd.strip("`\npy ")

    # add a layer of indentation
    cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

    # wrap in async def body
    body = f"async def {fn_name}():\n{cmd}"

    parsed = ast.parse(body)
    body = parsed.body[0].body

    insert_returns(body)

    env = {
        'bot': ctx.bot,
        'discord': discord,
        'commands': commands,
        'ctx': ctx,
        '__import__': __import__
    }
    exec(compile(parsed, filename="<ast>", mode="exec"), env)

    result = (await eval(f"{fn_name}()", env))
    if result != None:
      await ctx.send(result)
      await ctx.message.add_reaction("✅")
    else:
      await ctx.message.add_reaction("✅")
      return

bot.load_extension("jishaku")
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
#os.environ["JISHAKU_HIDE"] = "True"



@bot.event
async def on_message_edit(before, after):
    try:
      await bot.process_commands(after) # Bot will attempt to process the new edited command
    except:
        return


@bot.command(hidden=True)
@commands.is_owner()
async def restart(ctx):
  await ctx.reply("Restarting...")
  python = sys.executable
  os.execl(python, python, *sys.argv)
  await ctx.send("Restarted!")




if __name__ == '__main__':
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    for filename in os.listdir('./cogs/'):
        if filename.endswith(".py") and not filename.startswith("_"):
            bot.load_extension(f"cogs.{filename[:-3]}")
    token = os.environ.get("token")
    bot.run(token)
