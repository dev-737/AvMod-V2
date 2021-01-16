import discord
import platform
import re
import os
import asyncio
from discord import Spotify
from discord import CustomActivity
import random
import urllib.parse
import aiohttp
from PIL import Image, ImageFont,ImageDraw
import datetime
from discord.ext import commands

def convert(time):
    pos = ["s","m","h","d","w"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24, "w" : 3600*24*7}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2


    return val * time_dict[unit]

def to_emoji(c):
    base = 0x1f1e6
    return chr(base + c) 

"""snipe_message_content = None
snipe_message_author = None
snipe_message_id = None
snipe_message_channel = None"""

class utility(commands.Cog): #, name="🛠️ UTILITY"
  """
  This example uses tasks provided by discord.ext to create a task that posts guild count to top.gg every 30 minutes.
  """

  def __init__(self, bot):
      self.bot = bot


  @commands.command(aliases=["say", "repeat"])
  @commands.check_any(commands.has_permissions(manage_messages=True), commands.is_owner())
  async def echo(self, ctx, *, message=None):
        """
        A simple command that repeats the users input back to them.
        """
        message = message or "Please provide the message to be repeated."
        await ctx.message.delete()
        await ctx.send(message)

  @commands.command(aliases=["av", "pfp"])
  async def avatar(self, ctx,*, member: discord.Member=None):

    """A command used to show your avatar!"""
    if member == None:
      embed=discord.Embed(color=discord.Colour.blurple())
      embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
      embed.set_image(url=f"{ctx.author.avatar_url}")
      await ctx.reply(embed=embed)

    else:
      embed=discord.Embed(color=discord.Colour.blurple())
      embed.set_author(name=member, icon_url=member.avatar_url)
      embed.set_image(url=f"{member.avatar_url}")
      await ctx.reply(embed=embed)
  """ 
 @commands.command(aliases=["server", "guildinfo", "si"])
  async def serverinfo(self, ctx):
    
    Shows Information about the server.

    roles=[role for role in ctx.guild.roles if role != ctx.guild.default_role]
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=name + " Server Information",
        description=description,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name=f":roll_of_paper: Roles:", value=f'**{len(roles)}**', inline=False)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name=':calendar:Created At', value=ctx.guild.created_at.strftime("%a, %#d/%B/%Y, %I:%M %p UTC"), inline=True )
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)"""



  @commands.command()
  @commands.cooldown(1, 15, commands.BucketType.user)
  async def emojify(self, ctx, *, text: str):
        '''
        Converts the alphabet and spaces into emojis.
        '''
        emojified = ''
        formatted = re.sub(r'[^A-Za-z ]+', "", text).lower()
        if text == '':
            await ctx.send('Please say what text you want to be converted.')
        else:
            for i in formatted:
                if i == ' ':
                    emojified += '     '
                else:
                    emojified += ':regional_indicator_{}: '.format(i)
            if len(emojified) + 2 >= 2000:
                await ctx.send('Your message in emojis exceeds 2000 characters!')
            if len(emojified) <= 25:
                await ctx.send('Please only provide text.')
            else:
                await ctx.send('_ _'+emojified+'')

  @commands.command(helpinfo='Searches the web (or images if typed first)', aliases=['search'])
  async def google(self, ctx, *, searchquery: str):
    '''
    Googles searchquery, or images if you specified that
    '''
    searchquerylower = searchquery.lower()
    if searchquerylower.startswith('images '):
        await ctx.send('<https://www.google.com/search?tbm=isch&q={}>'
                       .format(urllib.parse.quote_plus(searchquery[7:])))
    else:
        await ctx.send('<https://www.google.com/search?q={}>'
                       .format(urllib.parse.quote_plus(searchquery)))
  
  @commands.command()
  async def wiki(self, ctx, *, message: str):

    """Search WikiPedia For Something."""

    await ctx.send('<https://en.m.wikipedia.org/wiki/{}>'
                       .format(urllib.parse.quote_plus(message)))
  


  @commands.command(description="Reverces the text you provide!!")
  async def reverse(self, ctx, *, msg):

    """Reverse Text!"""

    t_rev = msg[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
    await ctx.send(f"🔁 {t_rev}")

  @commands.command(aliases=["mc"], description="Shows the server member count.")
  async def membercount(self, ctx):

    """Know More About Your Server's Member Count!"""

    embed = discord.Embed(colour=discord.Colour.blue(),timestamp=ctx.message.created_at, title="Members:")
    embed.add_field(name="💬All:", value=ctx.guild.member_count, inline=False)
    embed.add_field(name="👨‍🚀Humans:", value=len([m for m in ctx.guild.members if not m.bot]), inline=False)
    embed.add_field(name="🤖Bots:", value=len([m for m in ctx.guild.members if m.bot]), inline=False)
    
    await ctx.send(embed=embed)


  @commands.command()
  @commands.guild_only()
  async def poll(self, ctx, *, question):
      """Interactively creates a poll with the following question.
      To vote, use reactions!
      """

      # a list of messages to delete when we're all done
      messages = [ctx.message]
      answers = []

      def check(m):
          return m.author == ctx.author and m.channel == ctx.channel and len(m.content) <= 100

      for i in range(20):
          messages.append(await ctx.send(f'What would you like the questsion to be? **{ctx.prefix}cancel** to publish poll.'))

          try:
              entry = await self.bot.wait_for('message', check=check, timeout=60.0)
          except asyncio.TimeoutError:
              break

          messages.append(entry)

          if entry.clean_content.startswith(f'{ctx.prefix}cancel'):
              break

          answers.append((to_emoji(i), entry.clean_content))

      try:
          await ctx.channel.delete_messages(messages)
      except:
          pass # oh well

      answer = '\n'.join(f'{keycap}: {content}' for keycap, content in answers)
      actual_poll = await ctx.send(f'{ctx.author} asks: {question}\n\n{answer}')
      for emoji, _ in answers:
          await actual_poll.add_reaction(emoji)

  @poll.error
  async def poll_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
          return await ctx.send('Missing the question.')

  @commands.command()
  @commands.guild_only()
  async def quickpoll(self, ctx, *questions_and_choices: str):
      """Makes a poll quickly.
      The first argument is the question and the rest are the choices.
      """

      if len(questions_and_choices) < 3:
          return await ctx.send('Need at least 1 question with 2 choices.')
      elif len(questions_and_choices) > 21:
          return await ctx.send('You can only have up to 20 choices.')

      perms = ctx.channel.permissions_for(ctx.me)
      if not (perms.read_message_history or perms.add_reactions):
          return await ctx.send('Need Read Message History and Add Reactions permissions.')

      question = questions_and_choices[0]
      choices = [(to_emoji(e), v) for e, v in enumerate(questions_and_choices[1:])]

      try:
          await ctx.message.delete()
      except:
          pass

      body = "\n".join(f"{key}: {c}" for key, c in choices)
      poll = await ctx.send(f'{ctx.author} asks: {question}\n\n{body}')
      for emoji, _ in choices:
          await poll.add_reaction(emoji)


  @commands.command(description=f'Start a giveaway!', aliases=['gcreate', 'giveawaycreate'])
  @commands.guild_only()
  @commands.check_any(commands.is_owner(), commands.has_permissions(manage_guild=True))
  async def giveaway_create(self, ctx):

    """Start a giveaway!"""

    await ctx.send("**Let's start with this giveaway!** Answer these questions within 30 seconds!")

    questions = ["1. **Which channel should this giveaway be hosted in?**", 
                "2. What should be the duration of the giveaway? (s|m|h|d|w) \nexample: `5d`",
                "3. What is the prize when someone wins the giveaway?"]

    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel 

    for i in questions:
        await ctx.send(i)

        try:
            msg = await self.bot.wait_for('message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('You didn\'t answer in time, please be quicker next time!')
            return
        else:
            answers.append(msg.content)
    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
        return

    channel = self.bot.get_channel(c_id)

    time = convert(answers[1])

    if time == -1:
        await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d|w) next time!")
        return
    elif time == -2:
        await ctx.send(f"The time must be an integer. Please enter an integer next time")
        return            

    prize = answers[2]
    await ctx.send(f"The __Giveaway will be in {channel.mention}__ and will last **{answers[1]}!** \n\nprize: **{prize}!**")


    embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = 0xB19CD9)

    embed.set_author(name = f"Giveaway Created by {ctx.author}!", icon_url=ctx.author.avatar_url)

    embed.set_footer(text = f"React with 🎉 to enter! | Ends {answers[1]} from now!")

    my_msg = await channel.send(embed = embed)


    await my_msg.add_reaction("🎉")


    await asyncio.sleep(time)


    new_msg = await channel.fetch_message(my_msg.id)


    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(self.bot.user))

    try:
      winner = random.choice(users)
    except IndexError:
      await ctx.send("Oh well... No one even entered. 😦")

    await ctx.author.send(f"The giveaway that you started {answers[1]} ago from {ctx.guild.name} has ended.\n\nWinner: {winner} | ID: `{winner.id}` ")
    await channel.send(f"Congratulations! {winner.mention} has won **{prize}**!")

  @commands.command()
  @commands.guild_only()
  @commands.check_any(commands.is_owner(), commands.has_permissions(manage_guild=True))
  async def reroll(self, ctx,  id_of_giveaway : int):

    """Reroll A Giveaway!"""

    await ctx.message.delete()

    try:
      new_msg = await ctx.channel.fetch_message(id_of_giveaway)
    except:
      await ctx.send("**ERROR!**\nInvalid message id")
      return
      
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(self.bot.user))

    winner = random.choice(users)

    await ctx.channel.send(f"The new winner is {winner.mention}!")



  @commands.command()
  async def spotify(self, ctx, user: discord.Member=None):
      user = user or ctx.author
      for activity in user.activities:
          if isinstance(activity, Spotify):
            embed=discord.Embed(color=discord.Colour.green())
            embed.add_field(name=activity.title, value=f"Listening to **{activity.title}** by **{activity.artist}**.")
            embed.set_image(url=activity.album_cover_url)
            embed.set_author(name=user.name, icon_url=user.avatar_url)
            await ctx.send(embed=embed)
            break
      else:
        await ctx.send(":x: Not Listening to Spotify!")

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

  @commands.command(name="change-log", aliases=["changelog", "cl"])
  async def changel(self, ctx):
    embed=discord.Embed(title="<a:tada:769463305424338944>V2.1.0<a:tada:769463305424338944>", color=0x2F3136, description="""

<:wait:790914749785309204> **CHANGE-LOG:**
**```diff
+ Changed The help command slightly.
+ New echo slash command.
+ Uptime Command
+ Improved Block/Lock/Unlock
+ New Temprole, Tempmute command.
+ Enhanced error handlers 
+ New Enbed Colours.
+ New Suggest Command.
+ Added Slash Command Invite.```**
<:info:769844372107427860> **UPDATE NOTICE:**
In order to add the slash command in your server, you must invite the bot with the slash command link (`av!invite`). And remember, it bypasses all perms. So do be careful while using it.
If you find a bug, you can use `av!report <What the error is about> [raw error]`. There are quite a few bugs in the`tempmute` and `temprole` command, as the time reset's when I restart AvMod. The economy system will be down until further notice. 

Thanks, 
AvMod Devs.""")
    await ctx.send(embed=embed)


  """@commands.Cog.listener()
  async def on_message_delete(self, message):

      global snipe_message_content
      global snipe_message_author
      global snipe_message_id
      global snipe_message_channel

      snipe_message_content = message.content
      snipe_message_author = message.author
      snipe_message_id = message.id
      snipe_message_channel = message.channel
      await asyncio.sleep(60)

      if message.id == snipe_message_id:
          snipe_message_author = None
          snipe_message_content = None
          snipe_message_id = None
          snipe_message_channel = None
      await self.bot.process_commands(message)

  @commands.command()
  @commands.guild_only()
  @commands.cooldown(1, 10, commands.BucketType.member)
  async def snipe(self, message):

      ""Displays the previously deleted message."

      if message.channel == snipe_message_channel:
          embed = discord.Embed(color=0x323232, description=f"{snipe_message_content}")
          embed.set_footer(text=f"Asked by {message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
          embed.set_author(name=snipe_message_author, icon_url=snipe_message_author.avatar_url)
          await message.channel.send(embed=embed)
          return
      else: 
        await message.channel.send("Theres nothing to snipe.")
"""
def setup(bot):
    bot.add_cog(utility(bot))
