import discord
import asyncio
from discord.ext import commands
from imports import StaticEmoji, animatedEmojis

staff = StaticEmoji.staff
thonkspin = animatedEmojis.thonkspin
animatedStaff = animatedEmojis.staff
alarm = animatedEmojis.alarm
idk = animatedEmojis.idk
animatedWrong = animatedEmojis.wrong

class moderation(commands.Cog): #, name="{animatedStaff} MODERATION
  def __init__(self, bot):
    self.bot = bot


  @commands.command()
  @commands.check_any(commands.is_owner(), commands.has_permissions(ban_members=True))
  async def ban(self, ctx, member: discord.Member, *, reason=None):

    """Bans the mentioned member."""


    if not reason: reason = "No Reason Provided."
    if not member:
      embed=discord.Embed(title=f"{thonkspin}  Syntax Error", description="Please ping or use the id of the member you want to ban.\n\nex.`.ban <@User> [reason]`/`.ban <ID> [Reason]`", color=discord.Colour.dark_theme())
      await ctx.send(embed=embed)
      return
    if member == ctx.author:
      noban=await ctx.send(":x: You Can't ban yourself!")
      await asyncio.sleep(3)
      await noban.delete()
      await ctx.message.delete()
      return
    try:
      await member.send(f"{alarm} You were banned from **{ctx.guild.name}**.\n\nReason: **{reason}**")
      await member.ban(reason=f'Moderator: {ctx.author}\nReason: {reason}')            
      embed=discord.Embed(description=f"***{staff} {member} was successfully banned!***", color=discord.Colour.dark_theme())  
      await ctx.send(embed=embed)
    except discord.errors.Forbidden:
      await ctx.send(f"{idk}  Sorry, I do not have enough permissions to ban that member.")
      return


    except:
      await member.ban(reason=f'Moderator: {ctx.author}\nReason: {reason}')            
      embed=discord.Embed(description=f"***{staff} {member} was successfully banned! I couldn't DM the user.***", color=discord.Colour.dark_theme())  
      await ctx.send(embed=embed)


  @commands.command()
  @commands.check_any(commands.is_owner(), commands.has_permissions(kick_members=True))
  async def kick(self, ctx, member: discord.Member=None, *, reason="No Reason Provided."):

    """Bans the mentioned member."""

    if not member:
      embed=discord.Embed(title=f"{thonkspin}  Syntax Error", description=f"Please ping or use the id of the member you want to kick.\n\nex.`{ctx.prefix}kick <@User> [reason]`/`{ctx.prefix}kick <ID> [Reason]`", color=discord.Colour.dark_theme())
      await ctx.send(embed=embed)
      return
    if member == ctx.author:
      nokick=await ctx.send(":x: You Can't kick yourself!")
      await asyncio.sleep(3)
      await nokick.delete()
      await ctx.message.delete()
      return
    
    try:
      await member.kick(reason=f'Moderator: {ctx.author}\nReason: {reason}')       
      await member.send(f"🔨 You were kicked from **{ctx.guild.name}**.\n\nReason: **{reason}**")     
      embed=discord.Embed(description=f"***{staff} {member} was successfully kicked!***", color=discord.Colour.dark_theme())  
      await ctx.send(embed=embed)

    except discord.errors.Forbidden:
      await ctx.send(f"{idk} Sorry, I do not have enough permissions to kick that member.")
      return

    except:
      await member.kick(reason=f'Moderator: {ctx.author}\nReason: {reason}')            
      embed=discord.Embed(description=f"***{staff} {member} was successfully kicked! I couldn't DM the user.***", color=discord.Colour.dark_theme())  
      await ctx.send(embed=embed)
      return



  @commands.command(aliases=["chup", "moot", "silence"])
  @commands.has_permissions(administrator=True)
  async def mute(self, ctx, member: discord.Member, *, reason=None):

    """Gives the user you mention the 'Muted' role."""
    if not reason: reason="No reason provided."
    role=discord.utils.get(ctx.guild.roles, name="Muted")
    if not member:
      await ctx.send('Please specify a member you would like to mute')
      return
    await member.add_roles(role, reason=reason)
    embed=discord.Embed(
    color=discord.Colour.dark_theme(), description=f"{animatedStaff}***{member} has been muted || {reason}***")
    await ctx.send(embed=embed)
    embed=discord.Embed(title="🤐 You have been muted!",
    color=discord.Colour.dark_theme(), description=f"{animatedStaff}***{member.mention} you have been muted from {ctx.guild.name}***\n\n**REASON: {reason}**")
    try:
      await member.send(embed=embed)
    except:
      pass


  @mute.error
  async def mute_error(self, ctx, error):
    if isinstance(error, commands.BadArgument):
        if len(ctx.args) == 2:
          embed=discord.Embed(title=f"{animatedWrong} SYNTAX ERROR", description=f"```py\n{error}```", color=discord.Colour.dark_theme())
          await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=f"{animatedWrong} SYNTAX ERROR", description=f"```py\n{error}```", color=discord.Colour.dark_theme())
            await ctx.send(embed=embed)


  @commands.command(aliases=["unchup", "unmoot", "unsilence"])
  @commands.has_permissions(administrator=True)
  @commands.guild_only()
  async def unmute(self, ctx, member: discord.Member=None):

    """Removes the 'Muted' role from the user you mention."""

    role=discord.utils.get(ctx.guild.roles, name="Muted")
    if not member:
        await ctx.send('Please specify a member you would like to unmute')
        return
    if role in member.roles:
      await member.remove_roles(role)
      embed=discord.Embed(
      color=discord.Colour.dark_theme(), description=f"***{animatedStaff} {member} has been unmuted***")
      await ctx.send(embed=embed)
    else:
      embed=discord.Embed(description=f"{animatedWrong}***{member} is not muted!***",color=discord.Colour.dark_theme())
      await ctx.send(embed=embed)


  @commands.command()
  @commands.check_any(commands.has_permissions(manage_messages=True), commands.is_owner())
  @commands.cooldown(1, 5, commands.BucketType.member)
  async def purge (self, ctx, amount):

    """Deletes a number of messages you say it to."""

    async with ctx.channel.typing():
      if int(amount) <= 0:
        embed = discord.Embed(
        color=discord.Colour.dark_theme()) 
        embed.add_field(name=f"{animatedWrong} ERROR", value="```Please provide a number more than 0.```") 
        await ctx.send(embed=embed)
        return

      elif int(amount) >= 101:
          await ctx.send ("You can only delete 100 messages at a time.")
      else:
          await ctx.channel.purge(limit=int(amount) + 1)
      #await self.bot.get_channel(771373935622750248).send(f'**{ctx.author}** purged **{amount}** of messages in **{ctx.guild}**')



  @commands.command(pass_context=True, aliases=["changenick", "setnick"])
  @commands.has_permissions(manage_nicknames=True)
  async def nick(self, ctx, member: discord.Member, *, nick):
    
    """Changes the NickName of the person you mention."""
    
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for **{member}**.')

  @commands.command()
  @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
  async def role(self, ctx, member: discord.Member, role: discord.Role):

    """Adds a role to the member you mention."""

    await member.add_roles(role)
    await ctx.send(f'Added {role} role to {member}.')

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def derole(self, ctx, member: discord.Member, role: discord.Role):

    """Removes a role from the member you mention."""

    await member.remove_roles(role)
    await ctx.send(f'Removed {role} role from {member}.')

  @commands.command(aliases=["ctc"])
  @commands.has_permissions(manage_channels=True)
  async def create_text_channel(self, ctx, name=None, category: discord.CategoryChannel=None):

    """Creates a text channel."""
    if not name:
      await ctx.send("***Please provide a name.***")
      return
      
    guild = ctx.guild
    await guild.create_text_channel(name=name, category=category)
    await ctx.send(f'Created text channel `{name}` in category `{category}`.')



  @commands.command(description="Announces the message you provide. `@everyone`\`@here` pings don't work.")
  @commands.has_permissions(manage_messages=True)
  async def announce(self, ctx,chan: discord.TextChannel=None, *, message=None):

    """Make an announcement through the bot."""

    try:
      if not chan:
        embed=discord.Embed(title=":x: Invalid Syntax", description="***Please mention the channel you would like to send this announcement to!***\n\n*Eg.`!announce <#channel> <announcement text>`*", color=discord.Colour.dark_theme())
        await ctx.send(embed=embed)
        return
  
      elif not message:
        embed=discord.Embed(discord.Colour.dark_theme())
        embed.add_field(name=":x: Invalid Syntax", value="```Please provide a message to be announced.```\n\nEg. `!announce <#channel> <announcement text>`", color=discord.Colour.dark_theme())
        await ctx.send(embed=embed)
        return
      else:
        await ctx.message.delete()
        embed=discord.Embed(timestamp=ctx.message.created_at, description=f"{message}", color=discord.Colour.dark_theme())
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await chan.send(embed=embed) 
        await ctx.send(f"<a:correct:765080491669061633> Announcement sent to {chan.mention}")
    except:
      await ctx.send(f"**Error!**\nChannel Not Found! Please use `{ctx.prefix}help announce` for more information.")
      return
  


  @commands.command(aliases=["direct", "dm"])
  @commands.has_permissions(manage_guild=True)
  async def dmuser(self, ctx, member: discord.Member,*, message):

    """DM's a user."""
    try:
      embed=discord.Embed(description=message, color=discord.Colour.dark_theme())
      embed.set_author(name=f'Message from {ctx.guild.name}', icon_url=ctx.guild.icon_url)
      embed.set_footer(text="Contact the staff or make a ticket if you have any questions/doubts. Thank You!", icon_url=ctx.guild.icon_url)
      await member.send(embed=embed)
      await ctx.send(f"${StaticEmoji.yeye}  I have DM'ed **{member}** for you!")
    except:
      await ctx.send("Sorry. Seems Like The User Has Their DM's Closed, or has Blocked Me.")


  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def softban(self, ctx, user: discord.Member=None, reason=None):
      """Temporarily restricts access to the server."""
      
      if not user: # checks if there is a user
          return await ctx.send("You must specify a user")
      
      try: # Tries to soft-ban user
          await ctx.guild.ban(user, f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified") 
          await ctx.guild.unban(user, "Temporarily Banned")
      except discord.Forbidden:
          return await ctx.send("Are you trying to soft-ban someone higher than the bot?")

  
  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def lock(self, ctx, channel : discord.TextChannel=None):

    """Locks a channel."""

    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('Channel locked.')



  @commands.command(aliases=["dtc", "deletechannel"] )
  @commands.has_permissions(manage_channels=True)
  async def delete_channel(self, ctx, chan: discord.TextChannel=None, *, reason=None):

    """Deletes a Text channel."""
    if reason==None:
      reason = "No Reason Provided."
    elif not chan:
      chan = ctx.channel
      
    try:
      await chan.delete(reason=reason)
    except:
      await ctx.send("Invalid Channel!")
      return
    else:
      await ctx.send(f'Deleted channel `{chan}` for reason `{reason}`')


    

  
  
  @commands.command(aliases=['changechannelname', 'ccn'])
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.has_permissions(manage_messages=True)
  async def change_channel_name(self, ctx,*, name : str=None):

    """Changes the channel name to the name you provide."""

    if not name:
      await ctx.send("***Please give a name to change this channel name to.***")
      return
    await ctx.channel.edit(name=name)
    await ctx.send(f"The channel name has been set to `{name}`")

  @commands.command()
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.has_permissions(manage_messages=True)
  async def slowmode(self, ctx, duration):

    """Changes the slowmode of the channel you are in."""

    duration = str(duration)
    if duration == "off":
      await ctx.channel.edit(slowmode_delay=0)
      await ctx.send("Slowmode has been disabled.")
      return

    duration = int(duration)
    if duration > 0:
        await ctx.channel.edit(slowmode_delay=duration)
        await ctx.send(f"Slowmode has been set to `{duration}s`")
    
    elif duration == 0:
        await ctx.channel.edit(slowmode_delay=duration)
        await ctx.send("Slowmode has been disabled.")
    


  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def unban(self, ctx, *, member):

    """Unbans the mentioned member."""

    banned_members= await ctx.guild.bans()
    member_name, member_descriminator = member.split('#')

    for ban_entry in banned_members:
      user=ban_entry.user

      if (user.name, user.discriminator) == (member_name, member_descriminator):
        await ctx.guild.unban(user)
        await ctx.send(f"Unbanned {user}")




"""  @commands.command()
  async def create_invite(self, ctx):
      Create instant invite
      link = await ctx.channel.create_invite(max_age = 300)
      await ctx.send(f"Here is an instant invite to your server: {link}")"""

"""  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def clone(self, ctx, channel):
    if channel==None:
      channel=ctx.Channel
    name=ctx.channel_name

    await channel.clone(name=name)
    await ctx.send('Cloned channel!')"""

"""  @commands.command()
  async def avtest(self, ctx, user_id: int):
    voted= await self.get_user_vote(self.bot_id, user_id)
    if voted == True:
      await ctx.send("TEST SUCCESSFUL!")
    else:
      await ctx.send("In order for you to use this command, pls vote in https://top.gg/bot/763626077292724264")"""





def setup(bot):
    bot.add_cog(moderation(bot))