from typing import Optional
import discord
import traceback
import difflib
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice
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

from imports import StaticEmoji, statusEmojis




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


arrow = StaticEmoji.arrow
online = statusEmojis.online 
offline = statusEmojis.offline
dnd = statusEmojis.dnd
idle = statusEmojis.idle

class HELP(commands.Cog, name='Info'):

    def __init__(self, bot):
        self.bot = bot
        self.dblpy = dbl.DBLClient(self.bot, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc2MTQxNDIzNDc2Nzg4NDMxOCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA2NDAxMzM5fQ.K6nFXKKJSMJ0WVORejXCfj93aMpnr6mt-MHnZ2oM1vs")

      


    

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

    """async def cmd_help(self, ctx, command):
      embed = discord.Embed(title=f"{str(command).upper()}",
                            description=f"**USAGE:\n**`{ctx.prefix}{command.qualified_name} {command.signature}`",
                            color=discord.Colour.dark_theme())
      alias=f"`{', '.join(command.aliases)}`"
      if alias==None: alias="None"
      embed.add_field(name="Aliases", value=alias, inline=False)
      embed.add_field(name=f'Description:', value=f'{command.help}\n\n{command.usage}')
      embed.set_footer(text='<> - Required | [] - Optional')
      await ctx.message.reply(embed=embed)

    @commands.command(name='help', description="Shows this message!",aliases=['commands', 'comms', 'command'])
    async def help(self, ctx, *, optional_command: Optional[str]=None):

      cogs=[c for c in self.bot.cogs.keys()]

      SB_COGS = ['GIVEAWAY', 'Jishaku', 'TopGG', 'tests']
      
      for hidden_cog in SB_COGS:
        cogs.remove(hidden_cog)
    

      if optional_command == None:
        HelpList = []

        for cog in cogs:
          commandList = ""
          for command in self.bot.get_cog(cog).walk_commands():
            if command.hidden:
              continue
              
            elif command.parent != None:
              continue

            commandList += f"`{command.name}` ➣ {command.help}\n"

          else:
            helpEmbed = discord.Embed(title=f'Module: `{cog}`\n', description=commandList, color=0x36393E) #description="[Support](https://discord.gg/eJrTyEX)  •   [Vote](https://top.gg/bot/761414234767884318/vote)  •   [Invite](https://discord.com/api/oauth2/authorize?client_id=761414234767884318&permissions=8&scope=bot)"
            #helpEmbed.add_field(name=f'Module: {cog}\n', value=commandList, inline=True)
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
              return
            
            else:
              await self.cmd_help(ctx, command)
              return

        else:
          await ctx.send("**Invalid Command!**")
          return"""

    async def cmd_help(self, ctx, command):
      embed = discord.Embed(title=f"{str(command).upper()}",
                            description=f"**USAGE:\n**`{ctx.prefix}{command.qualified_name} {command.signature}`",
                            color=discord.Colour.dark_theme())
      embed.add_field(name="Aliases", value=f"`{command.aliases}`", inline=False)
      embed.add_field(name='Description:', value=f'{command.help}\n\n{command.usage}')
      embed.set_footer(text='<> - Required | [] - Optional')
      await ctx.message.reply(embed=embed)

    @commands.command(name='help', description="Shows this message!",aliases=['commands', 'comms', 'command'], hidden=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx, *, optional_command: Optional[str]=None):

      cogs=[c for c in self.bot.cogs.keys()]

      SB_COGS = ['Jishaku', 'owners', 'Errors'] #, 'tests'
      
      for hidden_cog in SB_COGS:
        cogs.remove(hidden_cog)
    

      if optional_command == None:
        HelpList = []

        for cog in cogs:
          commandList = ""
          for command in self.bot.get_cog(cog).walk_commands():
            if command.hidden:
              continue
              
            elif command.parent != None:
              continue

            commandList += f"`{command.name}` ➔ {command.help}\n"

          else:
            helpEmbed = discord.Embed(title=f'**Module: `{cog}`**\n', description=commandList, color=0x2F3136)
            helpEmbed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            HelpList.append(helpEmbed)

        else:
           
              menu = (PaginatedMenu(ctx))
              menu.add_pages(HelpList)
              menu.set_timeout(30)
              menu.show_skip_buttons()
              #menu.show_page_numbers()
              #menu.allow_multisession()
              menu.show_command_message() 
              await menu.open()
          #except:
            #await ctx.send("I need `manage_message` permissions for removing the reactions.")
            #pass

      else:
        
        if (command := get(self.bot.commands, name=optional_command)):
        
          for secret_cogs in SB_COGS:
            if command in self.bot.get_cog(secret_cogs).walk_commands() or command.hidden:
              return
          
            else:
                  await self.cmd_help(ctx, command)
                  return
                      
        else:	
          all_names = []
          for cmd in self.bot.commands:
            all_names.append(cmd.name)
            close_names = difflib.get_close_matches(optional_command, all_names)
          
          
          if close_names:
            multiple_choice = BotMultipleChoice(ctx, [val for val in close_names], "Did you mean?", )
            await multiple_choice.run()

            await multiple_choice.quit()
        
            optional_command=multiple_choice.choice
            if (command := get(self.bot.commands, name=optional_command)):
        
              for secret_cogs in SB_COGS:
                if command in self.bot.get_cog(secret_cogs).walk_commands() or command.hidden:
                  return
          
                else:
                      await self.cmd_help(ctx, command)
                      return


          else:
               await ctx.send("**Invalid Command!**")




    """@commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def vote(self, ctx):

      "Vote For Meeee :smilely:!""

      vote=discord.Embed(title="Vote Options", description="`1.` **[TOP.GG](https://top.gg/bot/761414234767884318/vote)**\n`2.` **[DISCORD.BOTLIST](https://discordbotlist.com/bots/avmod/upvote)**\n`3.` **[DISCORD.BOATS](https://discord.boats/bot/761414234767884318/vote)**", color=0x2F3136)
      await ctx.send(embed=vote)"""

    @commands.command(aliases=["server", "guildinfo", "si"], description="Shows Information about the server.")
    async def serverinfo(self, ctx):

      """Info On The Server."""

      roles=[role for role in ctx.guild.roles if role != ctx.guild.default_role]

      owner = str(ctx.guild.owner)
      id = str(ctx.guild.id)
      region = str(ctx.guild.region)
      boosts = ctx.guild.premium_subscription_count
      memberCount = str(ctx.guild.member_count)
      UserCount = len([m for m in ctx.guild.members if not m.bot])
      BotCount = len([m for m in ctx.guild.members if  m.bot])
      icon = str(ctx.guild.icon_url)

      embed = discord.Embed(
          color=0x2F3136, description=f"{arrow}Owner: {owner}\n {arrow}  Region: {region}\n {arrow}Verification: {ctx.guild.verification_level}\n {arrow}  ID: {id}\n"
      )
      embed.set_thumbnail(url=icon)
      #embed.add_field(name="<a:owner_crown:774605327873212426> Owner", value="dev-0737#0737", inline=True)
      embed.set_author(name=ctx.guild.name, icon_url=icon)
      embed.add_field(name="◽Members", value=f"▫️All: {memberCount}\n ▫️Humans: {UserCount}\n▫️Bots: {BotCount}\n▫️Online Members: {sum(member.status==discord.Status.online  and not member.bot for member in ctx.guild.members)}\n▫️Offline Members: {sum(member.status==discord.Status.offline and not member.bot for member in ctx.guild.members)}")
      embed.add_field(name="◽Boosts", value=f"▫️Level: {ctx.guild.premium_tier}\n▫️Boost Count: {boosts} \n")
      embed.add_field(name="◽Counts:", value=f"▫️Roles: {len(roles)}\n▫️Catogory Count: {len(ctx.guild.categories)}\n▫️Channel Count: {len(ctx.guild.channels)} ")
      embed.add_field(name='◽Created At', value=ctx.guild.created_at.strftime("%a, %#d/%B/%Y, %I:%M %p UTC"))
      embed.set_image(url=ctx.guild.banner_url)

      await ctx.send(embed=embed)



    @commands.command(aliases=["whois", "wi", "ui"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def userinfo(self, ctx, member: discord.Member=None):

      """Shows Info about a user."""

      member=ctx.author if not member else member

      roles=[role for role in member.roles if role != ctx.guild.default_role][::-1]
      pos = sum(m.joined_at < member.joined_at for m in ctx.guild.members if m.joined_at is not None)
      status = str(member.status)
      if status == 'online':
        newstatus = f"{online} Online"
      elif status == 'dnd':
        newstatus = f'{dnd} Dnd'
      elif status == 'idle':
        newstatus = f'{idle} Idle'
      elif status == 'invisible':
        newstatus = f'{offline} Invisible'
      elif status == 'offline':
        newstatus = f'{offline} Offline'
        

      if member.avatar == member.default_avatar:
        embed = discord.Embed(colour=0x2F3136, timestamp=ctx.message.created_at)
        embed.set_author(name=f"User Info - {member}", icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.default_avatar_url)
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)

        embed.add_field(name='◽ Basic Info: ', value=f'▫️ ID: {member.id}\n ▫️ Nickname: {member.display_name}\n▫️ No. Roles: {len(roles)}\n▫️ Top Role: {member.top_role.mention}\n▫️ Join Position: {pos}')
        embed.add_field(name="◽ Other Info: ", value=f'▫️ Bot: {member.bot}\n▫️ Status: {newstatus}\n▫️ Created At: {member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")}\n▫️ Joined At: {member.joined_at.strftime("%a, %d %b %Y %I:%M %p UTC")}')
        await ctx.send(embed=embed)
      elif member.avatar != member.default_avatar:
        embed = discord.Embed(colour=0x2F3136, timestamp=ctx.message.created_at)
        embed.set_author(name=f"User Info - {member}", icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)

        embed.add_field(name='◽ Basic Info: ', value=f'▫️ ID: {member.id}\n ▫️ Nickname: {member.display_name}\n▫️ No. Roles: {len(roles)}\n▫️ Top Role: {member.top_role.mention}\n▫️ Join Position: {pos}')
        embed.add_field(name="◽ Other Info: ", value=f'▫️ Bot: {member.bot}\n▫️ Status: {newstatus}\n▫️ Created At: {member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")}\n▫️ Joined At: {member.joined_at.strftime("%a, %d %b %Y %I:%M %p UTC")}')
        await ctx.send(embed=embed)


    @commands.command()
    async def perms(self, ctx, member:discord.Member=None):

      """Check perms for yourself or another user."""

      if member == None:
        perm_string = '\n'.join([str(p[0]).replace("_", " ").title() for p in ctx.author.guild_permissions if p[1]])
        await ctx.embed(title='**User Perms:**', description=f'\n {perm_string}',color=discord.Colour.red())
      else: 
        perm_string = '\n'.join([str(p[0]).replace("_", " ").title() for p in member.guild_permissions if p[1]])
        await ctx.embed(title='**User Perms:**', description=f'\n {perm_string}',color=discord.Colour.red())






def setup(bot):
    bot.add_cog(HELP(bot))