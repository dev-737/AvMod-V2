import discord
import cogs._json
from discord import CustomActivity
import ast
import json
import asyncio
import os
from imports import StaticEmoji, animatedEmojis, insert_returns, statusEmojis
from discord import Spotify
from discord.ext import commands
import sys

import json



tick = StaticEmoji.tick
note = StaticEmoji.note
no = StaticEmoji.no
offline = statusEmojis.offline

tick = StaticEmoji.tick
animatedOnline = statusEmojis.online
loadDark = animatedEmojis.loadDark
vibing = animatedEmojis.vibing

class owners(commands.Cog): #, name="<a:discordstaff_shine:769445529238372373> MODERATION"



  def __init__(self, bot):
    self.bot = bot

  
  @commands.command(hidden=True)
  @commands.is_owner()
  async def servers(self, ctx):
      msg = "\n".join(f"{x}" for x in self.bot.guilds)
      em=discord.Embed(color=0x2F3136, description=f"```{msg}```")
      em.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
      await ctx.reply(embed=em)

  @commands.command(hidden=True)
  @commands.is_owner()
  async def nuke(self, ctx, channel_name: discord.TextChannel=None):
    if channel_name==None:
      channel_name=ctx.channel.name
      existing_channel = discord.utils.get(ctx.guild.channels, name=channel_name)
      if existing_channel is not None:
          new_channel = await existing_channel.clone(reason="Has been nuked")
          await existing_channel.delete()
          await new_channel.send("https://i.pinimg.com/originals/47/12/89/471289cde2490c80f60d5e85bcdfb6da.gif")
          await new_channel.send('**NUKED BY:**✈AvMod✈#3378')
      else:
          await ctx.send(f'No channel named **{channel_name}** was found')


  @commands.command(aliases=['disconnect', 'close', 'stopbot'], hidden=True)
  @commands.is_owner()
  async def logout(self, ctx):
      """
      If the user running the command owns the bot then this will disconnect the bot from discord.
      """
      chan = await self.bot.fetch_channel(972083876811931669)
      msg = await chan.fetch_message(972084220304457768)
      await msg.edit(content=f"""
**{offline} Offline**
------------------------------

{no} Cogs: Un-Loaded
------------------------------

{no} Commands: Failed 
------------------------------

{no}  Maintenance Mode: undefined
------------------------------

{no} Errors: null""")
      await ctx.send(f"Hey {ctx.author.mention}, I am now logging out :wave:")
      await self.bot.close()

  
  @commands.command(hidden=True)
  @commands.is_owner()
  async def blacklist(self, ctx, user: discord.Member):
      """
      Blacklist someone from the bot
      """
      if ctx.message.author.id == user.id:
          await ctx.send("Hey, you cannot blacklist yourself!")
          return

      self.bot.blacklisted_users.append(user.id)
      data = cogs._json.read_json("blacklist")
      data["blacklistedUsers"].append(user.id)
      cogs._json.write_json(data, "blacklist")
      await ctx.send(f"Hey, I have blacklisted {user.name} for you.")

  @commands.command(hidden=True)
  @commands.is_owner()
  async def unblacklist(self, ctx, user: discord.Member):
      """
      Unblacklist someone from the bot
      """
      data = cogs._json.read_json("blacklist")
      data["blacklistedUsers"].remove(user.id)
      cogs._json.write_json(data, "blacklist")
      await ctx.send(f"Hey, I have unblacklisted {user.name} for you.")



  @commands.command(hidden=True)
  @commands.is_owner()
  async def kicc(self, ctx, member:discord.Member):
    if member.guild_permissions.administrator:
      await ctx.send("NO!")
      return
    else:
      await ctx.send("yes! Kicced!")

  @commands.command(hidden=True)
  @commands.is_owner()
  async def mem(self, ctx):
    alll  = []
    for memb in ctx.guild.members:
      alll.update(memb.name)
    if len(alll) == ctx.guild.member_count:
      await ctx.send(f'```{alll}```')
  

  @commands.command(hidden=True)
  @commands.is_owner()
  async def whatdoing(self, ctx, user: discord.Member=None):
    user = user or ctx.author
    for activity in user.activities:
      if isinstance(activity, CustomActivity) and isinstance(activity, Spotify):
            embed=discord.Embed(color=discord.Colour.dark_theme())
            embed.add_field(name="CustomActivity", value=f"Name: {activity.name}\nEmoji: {activity.emoji}")
            embed.set_author(name=user.name, icon_url=user.avatar_url)
            embed.add_field(name=activity.name, value=f"Listening to **{activity.title}** by **{activity.artist}**.", inline=False)
            embed.set_image(url=activity.album_cover_url)
            await ctx.send(embed=embed)    


  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def unblock(self, ctx, user: discord.Member=None):

      """Unblocks a user from current channel"""
                              
      if not user: # checks if there is user
          return await ctx.send("You must specify a user")
      
      await ctx.channel.set_permissions(user, overwrite=None) # gives back send messages permissions
      await ctx.send(f"{user} has been unblocked!")


  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def block(self, ctx, user: discord.Member=None):
      """
      Blocks a user from chatting in current channel.
      """
                              
      if not user: # checks if there is user
          return await ctx.send("You must specify a user")
                              
      await ctx.channel.set_permissions(user, send_messages=False) 
      await ctx.send(f"{user} has been blocked!")


  @commands.command(hidden=True)
  @commands.is_owner()
  async def leave(self,ctx):
  
      if ctx.author.id == 701727675311587358:
        def check(m):
          return m.author == ctx.author and m.channel == ctx.channel and len(m.content) <= 100
        await ctx.send('Whats the guild id?')
        iid = await self.bot.wait_for('message', check=check, timeout=15.0)
        iid_content=int(iid.content)
        toleave = self.bot.get_guild(iid_content)
        print (iid.content)
        await ctx.send ('Ok, leaving that guild now!')
        print (iid.content)
        await toleave.leave()
        print (iid.content)


  @commands.command(hidden=True)
  @commands.guild_only()
  async def verify(self, ctx):
    if ctx.guild.id == 764862376930836502:
      if ctx.channel.id == 790203118159265792:
        role=discord.utils.get(ctx.guild.roles, name="humans")
        await ctx.author.add_roles(role, reason="Verification")
        await ctx.message.delete()
    
    else:
      await ctx.send(f"This Command Can Only Be used In My Support Server! `{ctx.prefix}support`")
      return




  @commands.command()
  @commands.is_owner()
  async def unload(self, ctx, cog):
      if cog.endswith(".py") and not cog.startswith("_"):
          m=await ctx.send(f"{loadDark} Unloading `{cog}`...")
          self.bot.unload_extension(f'cogs.{cog}')
          await asyncio.sleep(2)
          await m.edit(content=f'{tick}Unloaded `{cog}`!')
          chan = await self.bot.fetch_channel(972083876811931669)
          msg = await chan.fetch_message(972084220304457768)
          await msg.edit(content=f"""
  **{animatedOnline} Online**
  ------------------------------

  {note} Cogs: 1 or more unloaded
  ------------------------------

  {tick}> Commands: Fully Functional 
  ------------------------------

  {tick}>  Maintenance Mode: False
  ------------------------------

  {tick}> Errors: 0""")

      elif not cog.endswith(".py") and not cog.startswith("_"):
          m=await ctx.send(f"{loadDark} Unloading `{cog}`...")
          self.bot.unload_extension(f'cogs.{cog}')
          await asyncio.sleep(2)
          await m.edit(content=f'{tick} Unloaded `{cog}`!')
          chan = await self.bot.fetch_channel(972083876811931669)
          msg = await chan.fetch_message(972084220304457768)
          await msg.edit(content=f"""
  **{animatedOnline} Online**
  ------------------------------

  {note} Cogs: 1 or more unloaded
  ------------------------------

  {tick}> Commands: Fully Functional 
  ------------------------------

  {tick}>  Maintenance Mode: False
  ------------------------------

  {tick}> Errors: 0""")


      else:
          await ctx.send('Excetuion Failed. Reason: Unknown Cog')

          print(
          f"{ctx.author.id} attempted to unload an extension named {cog}.\n----------------------------------")


  @commands.command()
  @commands.is_owner()
  async def load(self, ctx, cog):
      if cog.endswith(".py") and not cog.startswith("_"):
          m=await ctx.send(f"{loadDark} Loading `{cog}`...")
          self.bot.load_extension(f'cogs.{cog}')
          await asyncio.sleep(2)
          await m.edit(content=f'{tick} Loaded `{cog}`!')
          chan = await self.bot.fetch_channel(802184818237374492)
          msg = await chan.fetch_message(806438951942488095)
          await msg.edit(content=f"""
  **<{animatedOnline} Online**
  ------------------------------

  {tick}> Cogs: Loaded
  ------------------------------

  {tick}> Commands: Fully Functional 
  ------------------------------

  {tick}>  Maintenance Mode: False
  ------------------------------

  {tick}> Errors: 0""")

      elif not cog.endswith(".py") and not cog.startswith("_"):
          m=await ctx.send(f"{loadDark} Loading `{cog}`...")
          self.bot.load_extension(f'cogs.{cog}')
          await asyncio.sleep(2)
          await m.edit(content=f'{tick} Loaded `{cog}`!')
          chan = await self.bot.fetch_channel(972083876811931669)
          msg = await chan.fetch_message(972084220304457768)
          await msg.edit(content=f"""
  **{animatedOnline} Online**
  ------------------------------

  {tick}> Cogs: Loaded
  ------------------------------

  {tick}> Commands: Fully Functional 
  ------------------------------

  {tick}>  Maintenance Mode: False
  ------------------------------

  {tick}> Errors: 0""")

      else:
          await ctx.send('Excetuion Failed. Reason: Unknown Cog')

      print(
          f"{ctx.author.id} attempted to load an extension named {cog}.\n----------------------------------")


  """for filename in os.listdir('./cogs/'):
    if filename.endswith('.py') and not filename.startswith("_"):
      bot.load_extension(f'cogs.{filename[:-3]}')"""


  @commands.command(aliases=['rl'])
  @commands.is_owner()
  async def reload(self, ctx, cog):
      if cog == 'all':
          for filename in os.listdir('./cogs/'):
              if filename.endswith(".py") and not filename.startswith("_"):
                 
                  msg = await ctx.send(f"{loadDark} Getting cogs...")
                  await asyncio.sleep(2)
                  await msg.edit(content="📤Unloading all cogs...")
                  self.bot.unload_extension(f'cogs.{filename[:-3]}')
                  await msg.edit(content="📥Loading all cogs...")
                  self.bot.load_extension(f'cogs.{filename[:-3]}')
                  await msg.edit(content="🔁Realoaded all cogs.")
                  await msg.edit(content=f"{vibing} Reload successful!")
                  await ctx.message.add_reaction("{tick}>")
                  await asyncio.sleep(10)
                  await ctx.message.delete()
                  await msg.delete()
                  return
              

      elif cog.endswith(".py") and not cog.startswith("_"):
          self.bot.unload_extension(f'cogs.{cog[:-3]}')
          self.bot.load_extension(f'cogs.{cog[:-3]}')
          msg = await ctx.send(f"📤Unloading `{cog}`...")
          await msg.edit(content=f"📥Loading `{cog}`...")
          await msg.edit(content=f'🔁Reloaded `{cog}`.')
          await ctx.message.add_reaction("{tick}>")
          await asyncio.sleep(3)
          await msg.delete()

      elif not cog.endswith(".py") and not cog.startswith("_"):
          self.bot.unload_extension(f'cogs.{cog}')
          self.bot.load_extension(f'cogs.{cog}')
          msg = await ctx.send(f"📤Unloading `{cog}`...")
          await msg.edit(content=f"📥Loading `{cog}`...")
          await msg.edit(content=f'🔁`{cog}` cog has now been reloaded!')
          await ctx.message.add_reaction(tick)
          await asyncio.sleep(3)
          await msg.delete()

      else:
          await ctx.send('Excetuion Failed. Reason: Unknown Cog')

          print(f"{ctx.author.id} attempted to reload an extension named {cog}.\n----------------------------------")



  @commands.command(name="eval", hidden=True)
  @commands.is_owner()
  async def eval_fn(self, ctx, *, cmd):
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
        embed=discord.Embed(description=f"```{result}```")

        await ctx.send(embed=embed)
        await ctx.message.add_reaction("✅")

      elif result == None:
        await ctx.message.add_reaction("✅")
        return


  @commands.command()
  async def disable_slash(self, ctx):
    with open('bot_config/disslash.json' , 'w') as f:
        json.dump(ctx.guild.id, f, indent = 4 )
    await ctx.send("All `slash-commands` have been disabled.")

def setup(bot):
    bot.add_cog(owners(bot))