import discord
import platform
import re
import os
import urllib.request as request
import asyncio
import json
from discord import Spotify
from discord import CustomActivity
import random
import urllib.parse
from discord.ext import commands

from imports import animatedEmojis

tada = animatedEmojis.tada

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
        await ctx.send(content=message, allowed_mentions = discord.AllowedMentions(everyone = False, roles=False))

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
      """Interactively creates a poll with upto 20 questions."""

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
      embed=discord.Embed(title="Poll:", color=discord.Colour.random())
      embed.add_field(name=question, value=answer)
      actual_poll = await ctx.send(embed=embed)
      for emoji, _ in answers:
          await actual_poll.add_reaction(emoji)

  @poll.error
  async def poll_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
          return await ctx.send('Missing the question.')

  @commands.command()
  @commands.guild_only()
  async def quickpoll(self, ctx, *questions_and_choices: str):
      """Makes a poll quickly."""

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
      embed=discord.Embed(title="Poll:", color=discord.Colour.random())
      embed.add_field(name=question, value=body)
      poll = await ctx.send(embed=embed)
      for emoji, _ in choices:
          await poll.add_reaction(emoji)

  @commands.command()
  async def pypi(self, ctx, lib: str):

      """Search for a library/module on pypi.org."""
      with request.urlopen(f'https://pypi.org/pypi/{lib}/json') as response:
        
        source = response.read()
        data = json.loads(source)
        email=data['info']['author_email']
        if email == None:
          email = "None Provided."
        docs=data['info']['docs_url']
        summary=data['info']['summary']
        author=data['info']['author']
        package_url=data['info']['package_url']
        licence=data['info']['license']
        home_page=data['info']['project_urls']['Homepage']
        project_url=data['info']['project_url']
        keywords = data['info']['keywords']
        download_url = data['info']['download_url']
        if download_url == "": download_url = "None Provided."
        if keywords == "": keywords = "None Provided."
        if project_url == None: project_url = "None Provided."
        version=data['info']['version']
        if email =="": email="None Provided."
        if docs ==None: docs="None Provided."

      
        embed=discord.Embed(title=f'{lib} {version}', url=project_url, description=f"{summary}", color=discord.Colour.random())
        #embed.add_field(name="Description:", value=data['info']['description'])
        embed.add_field(name="◽ Author Details:", value=f"**▫️ Name:** {author}\n**▫️ Email:** {email}\n")
        embed.add_field(name="◽ Project Details:", value=f'**▫️ Version:** {version}\n**▫️ Licence:** {licence}\n**▫️ Homepage:** {home_page}\n**▫️ Documentation URL:** {docs}\n**▫️ Download URL:** {download_url}\n**▫️ Keywords:** {keywords}\n', inline=False)
        embed.set_thumbnail(url='https://miro.medium.com/max/660/1*2FrV8q6rPdz6w2ShV6y7bw.png')

  
      
      await ctx.send(embed=embed)



  @commands.command()
  async def spotify(self, ctx, user: discord.Member=None):
      """Shows you what your listening to, in a nice embed."""
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

  @commands.command(name="change-log", aliases=["changelog", "cl"])
  async def changel(self, ctx):
    """List Of bot updates."""
    embed=discord.Embed(title=f"{tada}V2.1.0{tada}", color=0x2F3136, description="""

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
