import discord
import asyncio
from discord.ext import commands
import cogs._json

        
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



class moderation(commands.Cog): #, name="<a:discordstaff_shine:769445529238372373> MODERATION"



  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=['disconnect', 'close', 'stopbot'], hidden=True)
  @commands.is_owner()
  async def logout(self, ctx):
      """
      If the user running the command owns the bot then this will disconnect the bot from discord.
      """
      await ctx.send(f"Hey {ctx.author.mention}, I am now logging out :wave:")
      await self.bot.logout()

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
      self.bot.blacklisted_users.remove(user.id)
      data = cogs._json.read_json("blacklist")
      data["blacklistedUsers"].remove(user.id)
      cogs._json.write_json(data, "blacklist")
      await ctx.send(f"Hey, I have unblacklisted {user.name} for you.")

  @commands.command(aliases=["setprefix"], usage='[name] <image URL or custom emote>')
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 5, commands.BucketType.guild)
  async def prefix(self, ctx, *, pre='av!'):
      """
      Set a custom prefix for a guild
      """

      data = cogs._json.read_json('prefixes')
      data[str(ctx.message.guild.id)] = pre
      cogs._json.write_json(data, 'prefixes')
      await ctx.send(f"The guild prefix has been set to `{pre}`. Use `{pre}set_prefix <prefix>` to change it again!")


  @commands.command(hidden=True)
  async def leave(self,ctx):
  
      if ctx.author.id == 701727675311587358:
        def check(m):
          return m.author == ctx.author and m.channel == ctx.channel and len(m.content) <= 100
        await ctx.send('Whats the guild id?')
        iid = await self.bot.wait_for('message', check=check, timeout=15.0)
        iid_content=int(iid.content)
        toleave = self.bot.get_guild (iid_content)
        print (iid.content)
        await ctx.send (f'Ok, leaving that guild now!')
        print (iid.content)
        await toleave.leave()
        print (iid.content)
      

  @commands.command()
  @commands.check_any(commands.is_owner(), commands.has_permissions(ban_members=True))
  async def ban(self, ctx, member: discord.Member=None, *, reason="No Reason Provided."):

    """Bans the mentioned member."""

    if not member:
      embed=discord.Embed(title="<a:thonkspin:785094906111983646>  Syntax Error", description="Please ping or use the id of the member you want to ban.\n\nex.`.ban <@User> [reason]`/`.ban <ID> [Reason]`", color=discord.Colour.dark_theme())
      await ctx.send(embed=embed)
      return
    if member == ctx.author:
      noban=await ctx.send(":x: You Can't ban yourself!")
      await asyncio.sleep(3)
      await noban.delete()
      await ctx.message.delete()
      return
    try:
      await member.send(f"<a:alarm:772727409764990989> You were banned from **{ctx.guild.name}**.\n\nReason: **{reason}**")
      await member.ban(reason=f'Moderator: {ctx.author}\nReason: {reason}')            
      embed=discord.Embed(description=f"***<a:discordstaff_shine:769445529238372373> {member} was successfully banned!***", color=discord.Colour.dark_theme())  
      await ctx.send(embed=embed)
    except discord.errors.Forbidden:
      await ctx.send("<:sad:796576463063089203> Sorry, I do not have enough permissions to ban that member.")
      return


    except:
      await member.ban(reason=f'Moderator: {ctx.author}\nReason: {reason}')            
      embed=discord.Embed(description=f"***<a:discordstaff_shine:769445529238372373> {member} was successfully banned! I couldn't DM the user.***", color=discord.Colour.dark_theme())  
      await ctx.send(embed=embed)


  @commands.command()
  @commands.check_any(commands.is_owner(), commands.has_permissions(kick_members=True))
  async def kick(self, ctx, member: discord.Member=None, *, reason="No Reason Provided."):

    """Bans the mentioned member."""

    if not member:
      embed=discord.Embed(title="<a:thonkspin:785094906111983646>  Syntax Error", description=f"Please ping or use the id of the member you want to kick.\n\nex.`{ctx.prefix}kick <@User> [reason]`/`{ctx.prefix}kick <ID> [Reason]`", color=discord.Colour.dark_theme())
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
      embed=discord.Embed(description=f"***<a:discordstaff_shine:769445529238372373> {member} was successfully kicked!***", color=discord.Colour.dark_theme())  
      await ctx.send(embed=embed)

    except discord.errors.Forbidden:
      await ctx.send("<:sad:796576463063089203> Sorry, I do not have enough permissions to kick that member.")
      return

    except:
      await member.kick(reason=f'Moderator: {ctx.author}\nReason: {reason}')            
      embed=discord.Embed(description=f"***<a:discordstaff_shine:769445529238372373> {member} was successfully kicked! I couldn't DM the user.***", color=discord.Colour.dark_theme())  
      await ctx.send(embed=embed)
      return



  @commands.command(aliases=["chup", "moot", "silence"])
  @commands.has_permissions(administrator=True)
  async def mute(self, ctx, member: discord.Member=None, *, reason="No reason provided."):

    """Gives the user you mention the 'Muted' role."""

    role=discord.utils.get(ctx.guild.roles, name="Muted")
    if not member:
      await ctx.send('Please specify a member you would like to mute')
      return
    await member.add_roles(role, reason=reason)
    embed=discord.Embed(
    color=discord.Colour.dark_theme(), description=f"<a:discordstaff_shine:769445529238372373>***{member} has been muted || {reason}***")
    await ctx.send(embed=embed)
    embed=discord.Embed(title="🤐 You have been muted!",
    color=discord.Colour.dark_theme(), description=f"<a:discordstaff_shine:769445529238372373>***{member.mention} you have been muted from {ctx.guild.name}***\n\n**REASON: {reason}**")
    try:
      await member.send(embed=embed)
    except:
      pass


  @mute.error
  async def mute_error(self, ctx, error):
    if isinstance(error, commands.BadArgument):
        if len(ctx.args) == 2:
          embed=discord.Embed(title="<a:wrong:765080446937202698> SYNTAX ERROR", description=f"```py\n{error}```", color=discord.Colour.dark_theme())
          await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="<a:wrong:765080446937202698> SYNTAX ERROR", description=f"```py\n{error}```", color=discord.Colour.dark_theme())
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
      color=discord.Colour.dark_theme(), description=f"***<a:discordstaff_shine:769445529238372373> {member} has been unmuted***")
      await ctx.send(embed=embed)
    else:
      embed=discord.Embed(description=f"<a:wrong:765080446937202698>***{member} is not muted!***",color=discord.Colour.dark_theme())
      await ctx.send(embed=embed)


  @commands.command()
  @commands.check_any(commands.has_permissions(manage_messages=True), commands.is_owner())
  @commands.cooldown(1, 5, commands.BucketType.member)
  async def purge (self, ctx, amount=None):

    """Deletes a number of messages you say it to."""

    async with ctx.channel.typing():
      if amount == None:
        embed=discord.Embed(color=discord.Colour.dark_theme())
        embed.add_field(name="<a:wrong:764074894392033331> ERROR", value="```Please provide the amount of messages you want to delete.```")
        await ctx.send(embed=embed)
        return
      elif int(amount) <= 0:
        embed = discord.Embed(
        color=discord.Colour.dark_theme()) 
        embed.add_field(name="<a:wrong:764074894392033331> ERROR", value="```Please provide a number more than 0.```") 
        await ctx.send(embed=embed)
        return

      elif int(amount) >= 101:
          await ctx.send ("You can only delete 100 messages at a time.")
      else:
          await ctx.channel.purge(limit=int(amount) + 1)
          a = await ctx.send(f"<a:correct:765080491669061633> I have purged {amount} message(s).")
          await asyncio.sleep(2)
          await a.delete()
      #await self.bot.get_channel(771373935622750248).send(f'**{ctx.author}** purged **{amount}** of messages in **{ctx.guild}**')



  @commands.command(pass_context=True, aliases=["changenick", "setnick"])
  @commands.has_permissions(manage_nicknames=True)
  async def nick(self, ctx, member: discord.Member, *, nick):
    
    """Changes the NickName of the person you mention."""
    
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')

  @commands.command()
  @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
  async def role(self, ctx, member: discord.Member, role: discord.Role):

    """Adds a role to the member you mention."""

    await member.add_roles(role)
    await ctx.send(f'Added {role} role to {member.mention}')

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def derole(self, ctx, member: discord.Member, role: discord.Role):

    """Removes a role from the member you mention."""

    await member.remove_roles(role)
    await ctx.send(f'Removed {role} role from {member.mention}')

  @commands.command(aliases=["ctc"])
  @commands.has_permissions(manage_channels=True)
  async def create_text_channel(self, ctx, name=None, category: discord.CategoryChannel=None):

    """Creates a text channel."""
    voted=await self.dblpy.get_user_vote(ctx.author.id)
    if voted == False:
      embed=discord.Embed(title="Voters Only Command!", description="You must vote for me on [top.gg](https://top.gg/bot/761414234767884318/vote) in order to use this command. ", color=discord.Colour.red())
      await ctx.send(embed=embed)
    if voted == True:
      if not name:
        await ctx.send("***Please provide a name.***")
        return
      guild = ctx.guild
      await guild.create_text_channel(name=name, category=category)
      await ctx.send(f'Created text channel `{name}` in category `{category}`')



  @commands.command(description="Announces the message you provide. `@everyone`\`@here` pings don't work.")
  @commands.has_permissions(manage_messages=True)
  async def announce(self, ctx,chan: discord.TextChannel=None, *, message=None):
    try:
      if not chan:
        embed=discord.Embed(title=":x: Invalid Syntax", description="***Please mention the channel you would like to send this announcement to!***\n\n*Eg.`!announce <#channel> <announcement text>`*", color=discord.Colour.dark_theme())
        await ctx.send(embed=embed)
        return
  
      elif not message:
        embed=discord.Embed(discord.Colour.dark_theme())
        embed.add_field(name=":x: Invalid Syntax", value=f"```Please provide a message to be announced.```\n\nEg. `!announce <#channel> <announcement text>`", color=discord.Colour.dark_theme())
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
      await ctx.send(f"<:cool_yeye:785100613205491752>  I have DM'ed **{member}** for you!")
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
  async def block(self, ctx, user: discord.Member=None):
      """
      Blocks a user from chatting in current channel.
      """
                              
      if not user: # checks if there is user
          return await ctx.send("You must specify a user")
                              
      await ctx.channel.set_permissions(user, send_messages=False) 
      await ctx.send(f"{user} has been blocked!")
  
  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def lock(self, ctx, channel : discord.TextChannel=None):

    """Locks a channel."""

    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('Channel locked.')

  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def unblock(self, ctx, user: discord.Member=None):

      """Unblocks a user from current channel"""
                              
      if not user: # checks if there is user
          return await ctx.send("You must specify a user")
      
      await ctx.channel.set_permissions(user, overwrite=None) # gives back send messages permissions
      await ctx.send(f"{user} has been unblocked!")

  @commands.command(aliases=["dtc", "deletechannel"] )
  @commands.has_permissions(manage_channels=True)
  async def delete_channel(self, ctx, chan: discord.TextChannel=None, *, reason=None):

    """Deletes a Text channel."""
    if reason==None:
      reason = "No Reason Provided."
    voted=await self.dblpy.get_user_vote(ctx.author.id)
    if voted == False:
      embed=discord.Embed(title="Voters Only Command!", description="You must vote for me on [top.gg](https://top.gg/bot/761414234767884318/vote) in order to use this command. ", color=discord.Colour.red())
      await ctx.send(embed=embed)
    if voted == True:
      if not chan:
        await ctx.send("**Please Provide a Channel Name!**")
        return
      await chan.delete(reason=reason)
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
  async def slowmode(self, ctx, duration: int):

    """Changes the slowmode of the channel you are in."""

    if duration > 0:
        await ctx.channel.edit(slowmode_delay=duration)
        await ctx.send(f"Slowmode has been set to `{duration}s`")
    
    elif duration == 0:
        await ctx.channel.edit(slowmode_delay=duration)
        await ctx.send(f"Slowmode has been disabled.")

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
        

  @commands.command()
  @commands.check_any(commands.has_permissions(manage_roles=True), commands.has_permissions(manage_guild=True))
  async def tempmute(self, ctx, member: discord.Member=None, timee=None,*, reason=None):
      if not member:
          await ctx.channel.send("**ERROR!** \nJoin the support server to know more.")
          return

      elif reason == None:
          reason = "No Reason Provided"
      timee = convert(timee)
      muteRole = discord.utils.get(ctx.guild.roles, name="Muted")

      if muteRole in member.roles:
        await ctx.reply("Already Muted!")
        return

      await member.add_roles(muteRole)

      tempMuteEmbed = discord.Embed(color=discord.Colour.blue(), description=f"**Reason:** {reason}")
      tempMuteEmbed.set_author(name=f"{member} Has Been Muted", icon_url=f"{member.avatar_url}")

      await ctx.channel.send(embed=tempMuteEmbed)

      tempMuteModLogEmbed = discord.Embed(color=discord.Colour.blue())
      tempMuteModLogEmbed.set_author(name=f"[MUTE] {member}", icon_url=f"{member.avatar_url}")
      tempMuteModLogEmbed.add_field(name="User", value=f"{member.mention}")
      tempMuteModLogEmbed.add_field(name="Moderator", value=f"{ctx.message.author}")
      tempMuteModLogEmbed.add_field(name="Reason", value=f"{reason}")
      tempMuteModLogEmbed.add_field(name="Duration", value=f"{str(timee)}s")
      modlog = self.bot.get_channel(784746785402650691)
      await modlog.send(embed=tempMuteModLogEmbed)

      tempMuteDM = discord.Embed(color=discord.Colour.blue(), title="Mute Notification", description=f"You Were Muted In **{ctx.guild.name}**")
      tempMuteDM.add_field(name="Reason", value=f"{reason}")
      tempMuteDM.add_field(name="Duration", value=f"{timee}")

      userToDM = self.bot.get_user(member.id)
      await userToDM.send(embed=tempMuteDM)

      await asyncio.sleep(timee)
      await member.remove_roles(muteRole)

      unMuteModLogEmbed = discord.Embed(color=discord.Colour.blue())
      unMuteModLogEmbed.set_author(name=f"[UNMUTE] {member}", icon_url=f"{member.avatar_url}")
      unMuteModLogEmbed.add_field(name="User", value=f"{member.mention}")
      modlog = self.bot.get_channel(784746785402650691)
      await modlog.send(embed=unMuteModLogEmbed)


  @commands.command()
  @commands.check_any(commands.has_permissions(manage_roles=True), commands.has_permissions(manage_guild=True))
  async def temprole(self, ctx, member: discord.Member=None, role: discord.Role=None, timee=None, *, reason=None):
    timee = convert(timee)
    if role == None:
      await ctx.reply("What role do you want to give, dummy?")
      return
      
    elif not member:
      await ctx.reply("Member needed!")
      return

    else:

      await member.add_roles(role)
      await ctx.reply("Done!")
      await member.send(f"You have gotten the {role.name} in {ctx.guild.name}!")
      await asyncio.sleep(timee)
      await member.remove_roles(role)
      await ctx.reply("Role Removed!")




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
