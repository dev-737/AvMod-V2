import discord
import json
from aiohttp import request
import asyncio 
import pyfiglet
import os
import random
import aiohttp
from PIL import Image
from io import BytesIO
from PIL import Image, ImageFont,ImageDraw
from discord.ext import commands

class fun(commands.Cog): #, name='<:New:790914679681056768> FUN'

  def __init__(self, bot):
            self.bot = bot

  @commands.command()
  async def ascii(self, ctx, *, message):

    """Turns Your Text Into ASCII ART/TEXT BANNER!"""

    ascii_banner = pyfiglet.figlet_format(message)
    embed=discord.Embed(title="Ascii Art!", description=f"```{ascii_banner}```", color= discord.Colour.dark_theme())
    await ctx.reply(embed=embed)


  @commands.command(description="Eject a person who you think is sus! <:sus:772060172138840084>")
  async def eject(self, ctx, member: discord.Member=None):

    """Eject Your Friends, or Enimies!"""

    if member == None:
      member=ctx.author
    responces=[f'''. 　　　。　　　　•　    　ﾟ　　。 　　.

        　　　.　　　  　　.　　　　　。　　   。　.  　

        .　　      。　　　　　 ඞ   。   . 　　 • 　　　　•

        　　ﾟ　　 {member.name} was not An Impostor. 。　.

        　　'　　　 0 Impostor remains 　 　　。

        　　ﾟ　　　.　　　. 　　　　.　 .''',
        f'''. 　　　。　　　　•　    　ﾟ　　。 　　.

        　　　.　　　  　　.　　　　　。　　   。　.  　

        .　　      。　　　　　 ඞ   。   . 　　 • 　　　　•

        　　ﾟ　　 {member.name} was An Impostor. 。　.

        　　'　　　 0 Impostor remains 　 　　。

        　　ﾟ　　　.　　　. 　　　　.　 .'''
        
        ]
    msg=await ctx.send("<a:Loading:786176377757368330>  Processing...")
    await asyncio.sleep(2)
    await msg.edit(content=f'{random.choice(responces)}')

  @commands.command()
  @commands.cooldown(1, 1, commands.BucketType.user)
  async def meme(self, ctx):

    """Some Aviation Meme's to spice up your day!"""

    embed = discord.Embed(title="MEME")
    async with aiohttp.ClientSession() as cs:
      async with cs.get('https://www.reddit.com/r/aviationmemes/new/.json?sort=hot') as r:
        res = await r.json()
        embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
        await ctx.reply(embed=embed)

  @commands.command(description="A fun command that you can use the hack your friends or **Enimies**!!")
  @commands.cooldown(1, 30, commands.BucketType.user)
  async def hack(self, ctx, member: discord.Member=None):

    """hack your buddies! :yum:"""

    if not member:
      await ctx.reply('Please specify a member you would like to perform the hack on.<:hack:765540760178917417>')
      return
    msg = await ctx.send(content=f'[▘] Starting to hack {member}...')
    await asyncio.sleep(2)
    await msg.edit(content=f"[▝ ] Finding {member}'s password...")
    await asyncio.sleep(2)
    await msg.edit(content=f"[▖] {member}'s Email: `{member}.Hello@Email.com` \nPassowrd: `PAJDHSF.SHU@{member.name}`...")
    await asyncio.sleep(2)
    await msg.edit(content='[▗] Finding IP adress...')
    await asyncio.sleep(2)
    await msg.edit(content=f"[▘]{member}'s IP adress is: `65.171.199.83`")
    await asyncio.sleep(2)
    await msg.edit(content=f"[▘] Finding {member}'s latest DM.")
    await asyncio.sleep(2)
    await msg.edit(content="[▗] Latest DM: <a:Thecat:765079289590579210> Aw cats are cute...")
    await asyncio.sleep(2)
    await msg.edit(content='[▖]<a:loading:750313247110070375> almost done... ')
    await asyncio.sleep(5)
    await msg.edit(content='The hack is almost finished...')
    await asyncio.sleep(2)
    hack_responces1 = [f'<a:correct:765080491669061633> I have successfuly hacked **{member}**!',
                    '<a:wrong:765080446937202698> Hack Failed! You have been reported to discord for abusing the API and have been banned from using Discord.'] 

    await ctx.reply(f'{random.choice(hack_responces1)}')


  @commands.command(aliases=["birdfacts"])
  @commands.guild_only()
  async def bird_facts(self, ctx):

    """Random Bird Facts!"""

    with open("Links.json", 'r') as f:
      API = json.load(f)

    bird = API['birdfact']

    async with request("GET", bird, headers={}) as response:
      if response.status == 200:
        data = await response.json()

        embed = discord.Embed(title="FAX", description=f'{data["fact"]}', color=discord.Colour.red())

        embed.set_footer(text=f'Requested By: {ctx.author}', icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://news.usc.edu/files/2019/11/Taiwan-Blue-Magpie-web.jpg")

        await ctx.reply(embed=embed)

      else:
        print(response.status)

  @commands.command()
  async def cat(self, ctx):

        """Random picture of a meow"""
        
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://aws.random.cat/meow") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Meow")
                    embed.set_image(url=data['file'])
                    embed.set_footer(text="meow!")

                    await ctx.reply(embed=embed)      

  @commands.command()
  async def dog(self, ctx):

      """Random picture of a woof"""

      async with ctx.channel.typing():
          async with aiohttp.ClientSession() as cs:
              async with cs.get("https://random.dog/woof.json") as r:
                  data = await r.json()

                  embed = discord.Embed(title="Woof")
                  embed.set_image(url=data['url'])
                  embed.set_footer(text="Here is a doggo for you!")

                  await ctx.reply(embed=embed)

  @commands.command()
  async def drake(self, ctx,*, message):

    """Makes a simple drake meme."""

    text , text2 =message.split(",")
    img = Image.open('drake.png')

          
    Draw = ImageDraw.Draw(img)
    Font = ImageFont.truetype("arial.ttf",32)

    Draw.text((245,10),text,(0,0,0),font = Font)
    Draw.text((244,229),text2,(0,0,0),font = Font)

    img.save("Drakey.png")
    await ctx.reply(file = discord.File("Drakey.png"))
    os.remove("Drakey.png")

  @commands.command()
  async def hug(self, ctx, user: discord.Member):

    """Give some huggies to your friends!!"""

    gifs = ["https://cdn.weeb.sh/images/H1ui__XDW.gif", "https://cdn.weeb.sh/images/B11CDkhqM.gif", "https://cdn.weeb.sh/images/rJv2H5adf.gif", "https://cdn.weeb.sh/images/SywetdQvZ.gif", "https://cdn.weeb.sh/images/BJCCd_7Pb.gif"]
    embed = discord.Embed(title="Hug", description=f" {ctx.author.mention} hugs you {user.mention}  ...", color=discord.Color.blue())
    embed.set_image(url=f"{random.choice(gifs)}")
    await ctx.reply(embed=embed)

  @commands.command()
  async def stickroll(self, ctx):

    """Oh go on try it out :wink:"""

    await ctx.reply("https://tenor.com/view/stick-bug-rick-roll-lol-gif-18118062")


  @commands.command()
  @commands.guild_only()
  async def wasted(self, ctx, user: discord.Member=None):

    """Put a wasted overlay on your or someone else\'s avatar!"""

    if user is None:
      user = ctx.author

    with open("Links.json", 'r') as f:
      API = json.load(f)

    avatar = str(user.avatar_url).replace('.webp', '.png').replace('.gif', '.png').replace('?size=1024', '?size=512')

    UFAPI = f"{API['Wasted']}{avatar}"

    async with request("GET", UFAPI, headers={}) as response:
      if response.status == 200:

        embed = discord.Embed(title="Wasted!!", description=f'[Image Link]({UFAPI})',color=discord.Colour.red())
        embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)

        embed.set_image(url=UFAPI)

        await ctx.reply(embed=embed)



  """@commands.command()
  async def wink(self, ctx):

    ""Random Winking Gifs!"

    with open("Links.json", 'r') as f:
      WINK = json.load(f)
      WINKO = f"{WINK['link']}"
      embed=discord.Embed(title="Here Are Some Winks for you to Parctise on :wink:", color=ctx.author.color)
      embed.set_image(url=WINKO)
      await ctx.send(embed=embed)"""

  @commands.command()
  async def wanted(self, ctx, member: discord.Member=None):
    if member==None:
      member=ctx.author
    wanted= Image.open("wanted.jpg")

    asset=member.avatar_url_as(size= 128)
    data=BytesIO(await asset.read())
    pfp= Image.open(data)
    pfp= pfp.resize((161,122))

    wanted.paste(pfp, (10, 90))
    wanted.save("profile.jpg")

    await ctx.reply(file=discord.File("profile.jpg"))



def setup(bot):
    bot.add_cog(fun(bot))
