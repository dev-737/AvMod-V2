import discord
import asyncio
import platform
import humanize
import datetime
from discord.ext import commands


load_time = datetime.datetime.utcnow()

class Bott(commands.Cog, name="bot"): #, name="<a:discordstaff_shine:769445529238372373> MODERATION"



  def __init__(self, bot):
    self.bot = bot
  
  @commands.command()
  async def uptime(self, ctx):

    """Know how long I have been up and moderating for you!"""

    x = load_time - datetime.datetime.utcnow()
    y = humanize.precisedelta(x, minimum_unit="seconds")
    embed=discord.Embed(title="Uptime", description=f'```Uptime: {y}```', color=discord.Colour.random())
    await ctx.send(embed=embed)      


  @commands.command(hidden=True)
  @commands.cooldown(1, 100, commands.BucketType.user)
  async def source(self, ctx):
    await ctx.send("https://github.com/dev-737/AvMod-V2")

  @commands.command(aliases=['stat', 'info'])
  @commands.cooldown(1, 5, commands.BucketType.member)
  async def stats(self, ctx):

      """Show's the bots statistics."""
      owner = await self.bot.fetch_user(701727675311587358)
      pythonVersion = platform.python_version()
      dpyVersion = discord.__version__
      serverCount = len(ctx.bot.guilds)
      memberCount=len(set(ctx.bot.get_all_members()))
      delta_uptime = datetime.datetime.utcnow() - self.bot.launch_time
      hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
      minutes, seconds = divmod(remainder, 60)
      days, hours = divmod(hours, 24)
      embed = discord.Embed(description="[Support](https://discord.gg/v2wJ6Wk6xp)  •   [Invite](https://discord.com/api/oauth2/authorize?client_id=765905026454388737&permissions=8&scope=bot)", colour=0x2F3136, timestamp=ctx.message.created_at)

      embed.add_field(name='Bot Info: ',      value=f'```css\nBot version: {ctx.bot.version}```\n```css\nPython Version: {pythonVersion}```\n```css\nDiscordpy Version: {dpyVersion}```\n```css\nCommands: {len(self.bot.commands)}```')
      embed.add_field(name='Other Info: ',   value=f'```elm\nGuildCount: {serverCount}```\n```elm\nTotal Users: {memberCount}```\n ```elm\nOwner: {owner}```\n```elm\nUptime: {days}d {hours}h {minutes}m {seconds}s   ```')
      embed.set_author(name=f"{ctx.bot.user.name} Stats", icon_url=ctx.bot.user.avatar_url)
      await ctx.message.reply(embed=embed, mention_author=False)

  @commands.command()
  async def invite(self, ctx):

    """Shows you the invite link to the bot."""

    embed=discord.Embed(description="**Administrator Invite (8)**  •    [Administrator Permissions](<https://discord.com/api/oauth2/authorize?client_id=765905026454388737&permissions=8&scope=bot>)\n**Required Permissions (1544023159)**  •   [Required Permissions](https://discord.com/oauth2/authorize?client_id=765905026454388737&scope=bot&permissions=1544023159)\n**No Permissions (0)**  •   [No Permissions](https://discord.com/oauth2/authorize?client_id=765905026454388737&scope=bot&permissions=0)\n**Slash Command**  •   [Slash Command Invite](https://discord.com/api/oauth2/authorize?client_id=765905026454388737&permissions=8&scope=applications.commands%20bot)", color=0x36393E)
    embed.set_author(name="AVMOD INVITE", icon_url=self.bot.user.avatar_url)

    await ctx.message.reply(embed=embed, mention_author=False)

  @commands.command()
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def ping(self, ctx):

    """Shows AvMod's's ping'"""
    msg = await ctx.message.reply("**Checking ping...**")
    await msg.edit(content=f'Pong! `{round(ctx.bot.latency * 1000)}ms`')


  @commands.command(aliases=["discord", "support"])
  async def supportserver(self, ctx):
    
    """Shows you AvMod support server!"""

    await ctx.send("https://discord.gg/v2wJ6Wk6xp")


  @commands.command(name="bug-report")
  async def bug_report(self, ctx , *, bug):

    """Having issues with some of my commands? Use this!"""

    await ctx.send("**Reported to the devs! Use `av!support` if you further want assistance.**")
    e = await self.bot.fetch_channel(802184823015211058)
    await e.send(f"**Bug Reported**\nBy: {ctx.author}\nBug: ```{bug}```")
    return


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

    if entry.clean_content.startswith('yes'):
        await ctx.message.delete()
        msg=await ctx.bot.get_channel(802184822185394186).send(f"{ctx.author.mention}", embed=embed)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await ctx.send("Your suggestion has been sent to <#802184822185394186>, join the support server to view it. - <https://discord.gg/v2wJ6Wk6xp>")

    elif entry.clean_content.startswith('no'):
        await ctx.send("Ok, Cancelled The Command!")
        return

def setup(bot):
    bot.add_cog(Bott(bot))