import discord
import os
from typing import Optional
from imports import test
from imports import testers_only
from discord_slash import cog_ext
from discord_slash import SlashCommand
import datetime
import asyncio
from imports import convert
from discord_slash.utils import manage_commands
from discord.ext import commands
import difflib
import dbl
from disputils import BotMultipleChoice
from discord.utils import get
from dpymenus import PaginatedMenu

CODE = {'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
        'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',

        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.' 
        }







def to_morse(s):
    return ' '.join(CODE.get(i.upper()) for i in s)

def from_morse(s):
    return ''.join(CODE_REVERSED.get(i) for i in s.split())

CODE_REVERSED = {value:key for key,value in CODE.items()}
testers  = [252821261506445314, 739187622634717265, 701727675311587358]
          
"""async def custom_embedder(self, ctx, icon, color:discord.Colour, title, description):
  self.embed = discord.Embed()
  self.embed.set_author(name='test author',icon_url=icon)
  self.embed.title = title
  self.embed.description = description
  self.embed.color = 0x2F3136"""







class tests(commands.Cog):

    def __init__(self, bot):       
      if not hasattr(bot, "slash"):
              # Creates new SlashCommand instance to bot if bot doesn't have.
          bot.slash = SlashCommand(bot, override_type=True)
          token = os.environ.get("dbltoken")
          self.bot = bot
          self.token = token  # set this to your DBL token
          self.dblpy = dbl.DBLClient(self.bot, self.token)
          self.bot.slash.get_cog_commands(self)

      def cog_unload(self):
          self.bot.slash.remove_cog_commands(self)

    
    @commands.command()
    @test()
    @testers_only()
    async def check(self, ctx):
      await ctx.send("Voted!")
      return

    @commands.command()
    @testers_only()
    async def check_vote(self, ctx, member: discord.Member=None):
      if not member:
        member=ctx.author
      e=await self.dblpy.get_user_vote(member.id)
      if e==False:
        await ctx.send("Not Voted!")
      else:
        await ctx.send("Thanks for voting :D")

    @commands.command()
    @testers_only()
    async def ss(self, ctx, site):
      try:
        embed=discord.Embed(colour = discord.Colour.orange())
        embed.set_image(url=f"https://image.thum.io/get/width/1920/crop/675/maxAge/1/noanimate/{site}")
        await ctx.send(embed=embed)
      except:
        await ctx.send("Can't fetch that website!")

    @cog_ext.cog_slash(
        name="embed",
        guild_ids=[802183212846678066],
        description='Send your own discord embed!',
        options=[
            manage_commands.create_option(
                name = "icon",
                description = "The small icon on top. Use an Image ending with .png / .jpg / .gif.",
                option_type = 3,
                required = True
                ),
            manage_commands.create_option(
                name = "color",
                description = "Enter a valid color or a hex value.",
                option_type = 3,
                required = True
                ),
            manage_commands.create_option(
                name = "title",
                description = "Put in the title of the embed.",
                option_type = 3,
                required = True
                ),
            manage_commands.create_option(
                name = "description",
                description = "Put your content here. Supports formatting and markdown. To move to the next line, use \\n",
                option_type = 3,
                required = True
                ),
            manage_commands.create_option(
                name = "image",
                description = "Image ending with .png / .jpg / .gif",
                option_type = 3,
                required = False
                ),
            ]
    )
    async def custom_embedder(self, ctx, icon, color, title, description, image: Optional[str] = None):
      if ctx.author.id not in testers:
        await ctx.send(3, content="You need to be a tester in order to use this!", hidden=True)
        return
      description = description.replace('\\n', '\n')
      color = await commands.ColourConverter().convert(ctx, color)
      if not icon.startswith("https://"):
        await ctx.send(3, content="Please use a link that startswith `https://`.", hidden=True)
        return
      self.embed=discord.Embed()
      self.embed.set_author(name=title,icon_url=icon)
      self.embed.description = description
      self.embed.color = discord.Color(color.value)
      if image != None:
        self.embed.set_image(url=image)
      #self.embed.set_footer(text=f"By: {ctx.author.name}")
      self.embed.timestamp=datetime.datetime.now()

      
      await ctx.send(send_type=3, embeds=[self.embed])


    @commands.command()
    @testers_only()
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
    @testers_only()
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


    @commands.command(name='new-help', description="Shows this message!",aliases=['commands', 'comms', 'command'], hidden=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def _help(self, ctx, *, optional_command: Optional[str]=None):

      cogs=[c for c in self.bot.cogs.keys()]

      SB_COGS = ['Jishaku', 'TopGG', 'owners', 'tests', 'Errors'] #, 'tests'
      
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
              menu.show_page_numbers()
              menu.allow_multisession()
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

      

    @commands.command()
    @testers_only()
    async def help2(self, ctx, *cog):
      cog=[cog for cog in self.bot.cogs]

      for x in self.bot.cogs:
          SB_COGS = ['Jishaku', 'TopGG', 'owners', 'tests', 'Errors'] #, 'tests'
      
      for hidden_cog in SB_COGS:
          cog.remove(hidden_cog)

      if not cog:
        embed=discord.Embed(color=discord.Color.red())
        cog_desc = " "
        cog_desc += ("**{}**".format(x)+'\n') #Old cog_desc += ("**{}** - {}".format(x, self.bot.cogs[x].__doc__)+'\n')
        embed.add_field(name="COMMANDS", value=cog_desc[0:len(cog_desc)-1], inline=False)
        await ctx.send(embed=embed)

      else:
        if len(cog) > 1:
          embed=discord.Embed(title="Error", description="Too many cogs!")
          await ctx.message.author.send('', embed=embed)
          
        else:
          found = False
          for x in self.bot.cogs:
            for y in cog:
              if x == y:
                embed=discord.Embed()
                scog_info = ""
                #print (self.bot.get_cog(y).get_commands())
                for c in self.bot.get_cog(y).get_commands():
                  if not c.hidden:
                    scog_info += f"**{c.name}** - {c.help}\n"
                embed.add_field(name=f"{cog[0]} Module - {self.bot.cogs[cog[0]].__doc__}", value=scog_info)
        if not found:
          for x in self.bot.cogs:
            for c in self.bot.get_cog(x).get_commands():
              if c.name == cog[0]:
                embed=discord.Embed()
                embed.add_field(name=f"{c.name} - {c.help}", value=f'Proper Syntax:\n`{c.qualified_name} {c.signature}`') 
        await ctx.send(embed=embed)



    @commands.command()
    @testers_only()
    @testers_only()
    async def morse(self, ctx, *, msg):
      try:
        m=to_morse(msg)
      except: return await ctx.send("An error occured!")
      await ctx.send(f'`{m}`')


    @commands.command()
    @testers_only()
    async def unmorse(self, ctx, *, msg):
      m=from_morse(msg)
      await ctx.send(f'`{m}`')
    """@commands.command()
    async def tmetar(self, ctx, metar):
      with request.urlopen(f'https://avwx.rest/api/metar/{metar}') as response:
        source = response.read()
        data = json.loads(source)
        altimeter=data['sample']['altimeter']['repr']
      
      await ctx.send(altimeter)"""



def setup(bot):
    bot.add_cog(tests(bot))