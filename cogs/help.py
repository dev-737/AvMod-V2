from typing import Optional
import discord
import traceback
import cogs._json
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from discord.utils import get
import asyncio
import platform
import humanize
import datetime
from dpymenus import PaginatedMenu
import math
import re
import random
import dbl
load_time = datetime.datetime.utcnow()


errors = ('ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BlockingIOError',
          'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError',
          'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError',
          'EnvironmentError', 'FileExistsError', 'FileNotFoundError','FloatingPointError', 'FutureWarning',
          'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning',
          'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError',
          'KeyboardInterrupt', 'LookupError', 'MemoryError', 'ModuleNotFoundError', 'NameError',
          'NotADirectoryError', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError',
          'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 'RecursionError',
          'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration',
          'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError',
          'TimeoutError', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError',
          'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning',
          'WindowsError', 'ZeroDivisionError')

def convert(time):
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    return "%d:%d:%d:%d" % (day, hour, minutes, seconds)

"""def gen_code():
    chars = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.punctuation)
    num = list(string.digits) + list(string.hexdigits) + list(string.octdigits)
    former = []
    for i in range(random.randint(10, 20)):
        x = ('y', 'n')
        if random.choice(x) == 'y':
            if random.choice(x) == 'y':
                former.append(random.choice(chars).lower())
            else:
                former.append(random.choice(chars).upper())
        else:
            former.append(random.choice(num))
    return ''.join(map(str, former))"""


class HELP(commands.Cog, name='<:info:769844372107427860> INFO'):

    def __init__(self, bot):
        self.bot = bot
        self.dblpy = dbl.DBLClient(self.bot, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc2MTQxNDIzNDc2Nzg4NDMxOCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA2NDAxMzM5fQ.K6nFXKKJSMJ0WVORejXCfj93aMpnr6mt-MHnZ2oM1vs")

        


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            global time, message
            time = error.retry_after
            time = convert(time)
            x = time.split(':')
            if x[1] != '0' and x[2] != '0':
                if x[1] == 1:
                    message = f'Retry this command after **{x[1]}** hour and **{x[2]}** minutes!'
                else:
                    message = f'Retry this command after **{x[1]}** hours and **{x[2]}** minutes!'
            elif x[1] == '0' and x[2] != '0' and x[3] != '0':
                message = f'Retry this command after **{x[2]}** minutes and **{x[3]}** seconds!'
            elif x[3] != '0' and x[1] == '0' and x[2] == '0':
                message = f'Retry this command after **{x[3]}** seconds!'
            await ctx.send(message)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('**You have made an error.**\n\n{}'.format(error.param))
        elif isinstance(error, commands.TooManyArguments):
            await ctx.send('You have given too many args.\nPlease use the command as directed.')
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send('I am missing permissions.')
        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            await ctx.send('The cog {} is already loaded.'.format(error.args[0]))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('You need **{}** perms to complete this actions.'.format(' '.join(error.missing_perms[0].split('_'))))
        elif isinstance(error, commands.BotMissingAnyRole):
            await ctx.send('**Woops!**\n\nLooks like i am missing the {} role.'.format(error.missing_role))
        elif isinstance(error, commands.CheckAnyFailure):
            await ctx.send('An unknown error has occured.')
        elif isinstance(error, commands.errors.NSFWChannelRequired):
            await ctx.send('You must use this command in a channel marked as **NSFW**.')
        elif isinstance(error, commands.errors.NotOwner):
            await ctx.send('**Owner Only.**')
        elif isinstance(error, commands.errors.NoPrivateMessage):
            await ctx.send("The user has blocked me or has the DM's closed.")
        elif isinstance(error, discord.ext.commands.DisabledCommand):
            await ctx.send('This command is disabled.')
        elif isinstance(error, discord.errors.Forbidden):
            await ctx.send('I do not have permissions for this command!')
        elif isinstance(error, commands.errors.MemberNotFound):
            await ctx.send('Please give a valid user!')
        else:
          error = traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__)
          channel = self.bot.get_channel(792734554947452958)
          await channel.send('**Error in the command {}**\n```\n'.format(ctx.command.name) + ''.join(map(str, error)) + '\n```')
          embed=discord.Embed(title=f"Unknown Error!", description=f"```{error}```", color=discord.Colour.random())
          await ctx.send(embed=embed)
          errortype = 'Unspecified'
          for i in range(len(error)):
              for j in errors:
                  if j in error[i]:
                      errortype = j
                      break


    @commands.command(aliases=['stat', 'info'])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def stats(self, ctx):

        """Show's the bots statistics."""

        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(ctx.bot.guilds)
        memberCount=len(set(ctx.bot.get_all_members()))
        embed = discord.Embed(colour=ctx.author.colour, timestamp=ctx.message.created_at)

        embed.add_field(name='<:AvMod2:770247678885625856> Bot Version ',      value=ctx.bot.version)
        embed.add_field(name='<:python:769448668348416010>Python Version ',   value=pythonVersion)
        embed.add_field(name='<:discord:769449385670737940>Discord.py Version ',value=dpyVersion)
        embed.add_field(name='<:server_boost:769450820076306443>Total Guilds ',      value=serverCount)
        embed.add_field(name="<:members:769449777472471060>Total Members",      value= memberCount)
        embed.add_field(name='<a:botdev_shine:769445361693491200>Developer', value='<@701727675311587358>')

        embed.add_field(name="Discord", value="[Click to join](https://discord.gg/eJrTyEX)")

        embed.add_field(name="<:invite:769450163671400459>Bot Invite", value="[Invite](https://discord.com/api/oauth2/authorize?client_id=761414234767884318&permissions=8&scope=bot)", inline=True )
        embed.set_author(name=f"{ctx.bot.user.name} Stats", icon_url=ctx.bot.user.avatar_url)
        embed.add_field(name="<:upvote:274492025678856192> Vote", value="[vote](https://top.gg/bot/761414234767884318)")
        await ctx.message.reply(embed=embed)



    """async def cmd_help(self, ctx, command):
      embed = discord.Embed(title=f"{str(command).upper()}",
                            description=f"**USAGE:\n**`{ctx.prefix}{command.qualified_name} {command.signature}`",
                            color=discord.Colour.dark_theme())
      embed.add_field(name="Aliases", value=f"`{command.aliases}`", inline=False)
      embed.add_field(name=f'Description:', value=f'{command.help}\n\n{command.usage}')
      await ctx.message.reply(embed=embed)

    @commands.command(name='help', description="Shows this message!", aliases=['commands', 'comms', 'command'])
    async def help(self, ctx, *, command: Optional[str] = None):
      
        cogs=[c for c in self.bot.cogs.keys()]

        SB_COGS = ['oldhelp']
    
        for hidden_cog in SB_COGS:
          cogs.remove(hidden_cog)

        if command == None:
            HelpList = []

            for rl_cog in cogs:
                commandList = ""
                for command in self.bot.get_cog(rl_cog).walk_commands():
                    if command.hidden:
                        continue

                    elif command.parent != None:
                        continue

                    commandList += f"`{command.name}` ➣ {command.help}\n"

                else:
                    helpEmbed = discord.Embed(description="[Support](https://discord.gg/eJrTyEX)  •   [Vote](https://top.gg/bot/761414234767884318/vote)  •   [Invite](https://discord.com/api/oauth2/authorize?client_id=761414234767884318&permissions=8&scope=bot)", color=discord.Colour.dark_theme())
                    helpEmbed.add_field(name=rl_cog, value=commandList, inline=True)
                    helpEmbed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
                    HelpList.append(helpEmbed)
            
            else:
              
              menu = (PaginatedMenu(ctx))
              menu.add_pages(HelpList)
              menu.set_timeout(30)
              menu.show_skip_buttons()
              menu.show_page_numbers()
              menu.allow_multisession()
              menu.show_command_message() 
              try: 
                await menu.open()
              except:
                await ctx.send("**AN ERROR HAS OCCORED! PLEASE REPORT IT TO THE DEVS.")
                return
            

            

        else:
            if (command := get(self.bot.commands, name=command)):
                await self.cmd_help(ctx, command)
                return

            else:
                await ctx.message.reply("Invalid Command!")
                return"""

    async def cmd_help(self, ctx, command):
      prefix = await self.bot.config.find(ctx.guild.id)
      prefix = prefix["Bot Prefix"] or "&"
      embed = discord.Embed(title=f"{str(command).upper()} Help!", description=f"`{prefix}` {syntax(command)}", color = discord.Colour.random())

      '''
      if command.parent in self.bot.get_command(command).walk_commands():
        SCmd = ""
        for subcommmand in command.parent:
          SCmd += f"`{subcommmand}` - {subcommmand.description}\n"

        embed.add_field(name='Subcommands:', value=SCmd)
      '''


      embed.add_field(name=f'Command Description:', value=command.help or command.description)

      embed.set_footer(text=f'{ctx.prefix} - Server Prefix | <> - Required | [] - Optional')
      await ctx.send(embed=embed)

    @commands.command(name='help', description="Shows this message!",aliases=['commands', 'comms', 'command'])
    async def help(self, ctx, *, optional_command: Optional[str]=None):

      cogs=[c for c in self.bot.cogs.keys()]

      SB_COGS = ['🎁 GIVEAWAY', 'Jishaku', 'TopGG', 'tests']
      
      for hidden_cog in SB_COGS:
        cogs.remove(hidden_cog)
    

      if optional_command == None:
        HelpList = []

        for rl_cog in cogs:
          commandList = ""
          for command in self.bot.get_cog(rl_cog).walk_commands():
            if command.hidden:
              continue
              
            elif command.parent != None:
              continue

            commandList += f"`{command.name}` ➣ {command.help}\n"

          else:
            helpEmbed = discord.Embed(description="[Support](https://discord.gg/eJrTyEX)  •   [Vote](https://top.gg/bot/761414234767884318/vote)  •   [Invite](https://discord.com/api/oauth2/authorize?client_id=761414234767884318&permissions=8&scope=bot)", color=0x36393E)
            helpEmbed.add_field(name=rl_cog, value=commandList, inline=True)
            helpEmbed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            HelpList.append(helpEmbed)

        else:
          try: 
              menu = (PaginatedMenu(ctx))
              menu.add_pages(HelpList)
              menu.set_timeout(30)
              menu.show_skip_buttons()
              menu.show_page_numbers()
              menu.allow_multisession()
              menu.show_command_message() 
              await menu.open()
          except:
            await ctx.send("I need `manage_message` perms for removing the reactions.")
            pass

      else:
        
        if (command := get(self.bot.commands, name=optional_command)):
          for secret_cogs in SB_COGS:
            if command in self.bot.get_cog(secret_cogs).walk_commands() or command.hidden:
              retur
            
            else:
              await self.cmd_help(ctx, command)
              return

        else:
          await ctx.send("**Invalid Command!**")
          return



    @commands.command()
    async def invite(self, ctx):

      """Shows you the invite link to the bot."""

      embed=discord.Embed(description="**Administrator Invite (8)**  •    [Administrator Permissions](<https://discord.com/api/oauth2/authorize?client_id=761414234767884318&permissions=8&scope=bot>)\n**Required Permissions (1544023159)**  •   [Required Permissions](https://discord.com/oauth2/authorize?client_id=761414234767884318&scope=bot&permissions=1544023159)\n**No Permissions (0)**  •   [No Permissions](https://discord.com/oauth2/authorize?client_id=761414234767884318&scope=bot&permissions=0)\n**Slash Command**  •   [Slash Command Invite](https://discord.com/api/oauth2/authorize?client_id=761414234767884318&permissions=8&scope=applications.commands%20bot)", color=0x36393E)
      embed.set_author(name="AVMOD INVITE", icon_url=self.bot.user.avatar_url)

      await ctx.message.reply(embed=embed)
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):

      """Shows AvMod's's ping'"""
      msg = await ctx.message.reply("**Checking ping...**")
      await msg.edit(content=f'Pong! `{round(ctx.bot.latency * 1000)}ms`')


    @commands.command(aliases=["discord", "support"])
    async def supportserver(self, ctx):
      
      """Shows you AvMod support server!"""

      await ctx.send("https://discord.gg/eJrTyEX")


    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def vote(self, ctx):

      """Vote For Meeee :smilely:!"""

      vote=discord.Embed(title="Vote Options", description="`1.` **[TOP.GG](https://top.gg/bot/761414234767884318/vote)**\n`2.` **[DISCORD.BOTLIST](https://discordbotlist.com/bots/avmod/upvote)**\n`3.` **[DISCORD.BOATS](https://discord.boats/bot/761414234767884318/vote)**", color=0x2F3136)
      await ctx.send(embed=vote)

    @commands.command(aliases=["server", "guildinfo", "si"], description="Shows Information about the server.")
    async def serverinfo(self, ctx):

      """Info On The Server."""

      roles=[role for role in ctx.guild.roles if role != ctx.guild.default_role]
      name = str(ctx.guild.name)
      description = str(ctx.guild.description)

      owner = str(ctx.guild.owner)
      id = str(ctx.guild.id)
      region = str(ctx.guild.region)
      boosts = ctx.guild.premium_subscription_count
      memberCount = str(ctx.guild.member_count)
      UserCount = len([m for m in ctx.guild.members if not m.bot])
      BotCount = len([m for m in ctx.guild.members if  m.bot])
      icon = str(ctx.guild.icon_url)

      embed = discord.Embed(
          color=discord.Color.dark_theme(), description=f"<:arrow:775686257723441162>Owner: {owner}\n <:arrow:775686257723441162>  Region: {region}\n <:arrow:775686257723441162>Verification: {ctx.guild.verification_level}\n <:arrow:775686257723441162>  ID: {id}\n"
      )
      embed.set_thumbnail(url=icon)
      #embed.add_field(name="<a:owner_crown:774605327873212426> Owner", value="737Aviator!#0737", inline=True)
      embed.set_author(name=ctx.guild.name, icon_url=icon)
      embed.add_field(name="◽Members", value=f"▫️All: {memberCount}\n ▫️Humans: {UserCount}\n▫️Bots: {BotCount}\n▫️Online Members: {sum(member.status==discord.Status.online  and not member.bot for member in ctx.guild.members)}\n▫️Offline Members: {sum(member.status==discord.Status.offline and not member.bot for member in ctx.guild.members)}")
      embed.add_field(name="◽Boosts", value=f"▫️Level: {ctx.guild.premium_tier}\n▫️Boost Count: {boosts} \n")
      embed.add_field(name=f"◽Counts:", value=f"▫️Roles: {len(roles)}\n▫️Catogory Count: {len(ctx.guild.categories)}\n▫️Channel Count: {len(ctx.guild.channels)} ")
      embed.add_field(name='◽Created At', value=ctx.guild.created_at.strftime("%a, %#d/%B/%Y, %I:%M %p UTC"))

      await ctx.send(embed=embed)



    @commands.command(aliases=["whois", "wi", "ui"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def userinfo(self, ctx, member: discord.Member=None):

      """Shows Info about a user."""

      member=ctx.author if not member else member

      roles=[role for role in member.roles if role != ctx.guild.default_role][::-1]


      embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
      embed.set_author(name=f"User Info - {member}", icon_url=member.avatar_url)
      embed.set_thumbnail(url=member.avatar_url)
      embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)

      embed.add_field(name='<:info:769844372107427860> ID', value=member.id)
      embed.add_field(name=":name_badge: NickName", value=member.display_name, inline=False)

      embed.add_field(name=f":roll_of_paper: Roles ({len(roles)})", value="".join([role.mention for role in roles]), inline=False) 
      embed.add_field(name=":roll_of_paper: Top Role", value=member.top_role.mention)

      embed.add_field(name="<:bot_tag:772392739722756097> Bot?", value=member.bot, inline=False)

      embed.add_field(name="<:ping:786216763004026881> Status", value=str(member.status), inline=False)

      embed.add_field(name=':calendar:Created At', value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)

      embed.add_field(name=":calendar:Member Joined At", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)

      await ctx.send(embed=embed)


    @commands.command()
    async def suggest(self, ctx, *, suggestion):

      """Suggest something to be added/removed from the bot."""

      def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and len(m.content) <= 100
      embed=discord.Embed(title="New Suggestion:", description=suggestion, color=ctx.author.color)
      embed.set_thumbnail(url=ctx.author.avatar_url)
      embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
      embed.set_footer(text=f"Suggestion by: {ctx.author}", icon_url=ctx.author.avatar_url)

        
      try:
        msg=await ctx.send("***ARE YOU SURE YOU WANT TO DO THIS?***\n> If you want to suggest this to the devs type `yes` if not type `no`. [`yes / no]`")
        entry = await self.bot.wait_for('message', check=check, timeout=10.0)
      except asyncio.TimeoutError:
          await ctx.message.delete()
          await msg.delete()
          m = await ctx.send(f"{ctx.author.mention} You didn't respond in time. Try again.")
          await asyncio.sleep(5)
          await m.delete() 
          return

      if entry.clean_content.startswith(f'yes'):
          await ctx.message.delete()
          await ctx.bot.get_channel(765067272041267220).send(f"{ctx.author.mention}", embed=embed)
          await ctx.send("Your suggestion has been sent to <#765067272041267220>, join the support server to view it. - <https://discord.gg/eJrTyEX>")

      elif entry.clean_content.startswith(f'no'):
          await ctx.send("Ok, Cancelled The Command!")
          return


    @commands.command(name="bug-report")
    async def bug_report(self, ctx,error_code,  *, bug):
      await ctx.send("**Reported to the devs! Use `av!support` if you further want assistance.**")
      e = await self.bot.fetch_channel(768471667927547954)
      await e.send(f"**Bug Reported!**\nBug: **{bug}**\nCode:```{error_code}```")
      return



    @commands.command()
    async def uptime(self, ctx):
      x = load_time - datetime.datetime.utcnow()
      y = humanize.precisedelta(x, minimum_unit="seconds")
      embed=discord.Embed(title="Uptime", description=f'```Uptime: {y}```', color=discord.Colour.random())
      await ctx.send(embed=embed)      


def setup(bot):
    bot.add_cog(HELP(bot))