import discord
import json
from aiohttp import request
import asyncio 
import urllib.request as request
import qrcode
import humor_langs 
import pyfiglet
import os
import random
import aiohttp
from io import BytesIO
from PIL import Image, ImageFont,ImageDraw
from discord.ext import commands
import ipaddress 

from imports import StaticEmoji, animatedEmojis

from faker import Faker
from passwordgenerator import pwgenerator



def get_random_ip():
    """Generate a random IP Address
    Returns:
        string: IP Address
    """
    randomIPAddress = str(ipaddress.IPv4Address(random.randint(0, 2 ** 32)))
    isPrivateIp = ipaddress.ip_address(randomIPAddress).is_private
    if isPrivateIp:
        return get_random_ip()
    return randomIPAddress

fake = Faker()
  

pwo = pwgenerator.generate()



heheboii = StaticEmoji.heheboii
animatedWrong = animatedEmojis.wrong
animatedCorrect = animatedEmojis.correct
loading = animatedEmojis.loading
theCat = animatedEmojis.thecat

class fun(commands.Cog): #, name='<:New:790914679681056768> FUN'

  def __init__(self, bot):
            self.bot = bot

  @commands.command()
  async def ascii(self, ctx, *, message):

    """Turns Your Text Into ASCII ART/TEXT BANNER!"""

    ascii_banner = pyfiglet.figlet_format(message)
    
    await ctx.reply(f"```{ascii_banner}```")


  @commands.command()
  @commands.cooldown(1, 30, commands.BucketType.user)
  async def qrcode(self, ctx, *, text):

      """Generate QR codes right from the bot!"""

      qr = qrcode.QRCode(version=1,
                          error_correction=qrcode.constants.ERROR_CORRECT_L, 
                          box_size=20,
                          border=1)

      qr.add_data(text)
      qr.make(fit=True)

      img = qr.make_image(fill_color="black", back_color="white")
      img.save("qr.png")
      file = discord.File("qr.png")
  
      embed = discord.Embed(color=discord.Colour.random())
      embed.set_image(url="attachment://qr.png")
      embed.set_author(name="QR Code Generator", icon_url=ctx.bot.user.avatar_url)
      embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
  
      await ctx.send(embed=embed, file=file)



  @commands.command()
  async def clap(self, ctx, *, message):

    """Make 👏Your 👏 Message 👏 Look 👏 Like 👏 This!👏"""
    if ' ' in message:
      msg=" 👏 ".join([*message.split(" ")])
      await ctx.send(msg)
      return
    await ctx.send(f'👏{message}')



  @commands.command(description=f"Eject a person who you think is sus! {animatedEmojis.amongus}")
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
    msg=await ctx.send("<a:swirl:802382870073049089>  Processing...")
    await asyncio.sleep(2)
    await msg.edit(content=f'{random.choice(responces)}')

  @commands.command()
  @commands.cooldown(2, 1, commands.BucketType.user)
  async def meme(self, ctx):

    """Some Aviation Meme's to spice up your day!"""

    embed = discord.Embed(title="AvMemes", color=discord.Colour.random())
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    async with aiohttp.ClientSession() as cs:
      async with cs.get('https://www.reddit.com/r/aviationmemes/new/.json?sort=hot') as r:
        res = await r.json()
        embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
    
        await ctx.reply(embed=embed, mention_author=False)

  @commands.command(description="A fun command that you can use the hack your friends or **Enimies**!!")
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def hack(self, ctx, member: discord.Member=None):

    """hack your buddies! :yum:"""

    if not member:
      await ctx.reply(f'Please specify a member you would like to perform the hack on. {heheboii}')
      return
    msg = await ctx.send(content=f'[▘] Starting to hack {member}...')
    await asyncio.sleep(2)
    await msg.edit(content=f"[▝ ] Finding {member}'s password...")
    print(member.display_name)
    await msg.edit(content=f"[▖] {member}'s Email: `{fake.email()}` \nPassowrd: `{pwo.generate()}`...")
    await asyncio.sleep(2)
    await msg.edit(content='[▗] Finding IP adress...')
    await asyncio.sleep(2)
    await msg.edit(content=f"[▘]{member}'s IP adress is: `{get_random_ip()}`")
    await asyncio.sleep(2)
    await msg.edit(content=f"[▘] Finding {member}'s latest DM.")
    await asyncio.sleep(2)
    await msg.edit(content=f"[▗] Latest DM: {theCat} Aw cats are cute...")
    await asyncio.sleep(2)
    await msg.edit(content=f'[▖]{loading} almost done... ')
    await asyncio.sleep(3)
    await msg.edit(content='Almost finished... this is taking sometime...')
    await asyncio.sleep(2)
    hack_responces1 = [f'{animatedCorrect} I have successfuly hacked **{member}**!',
                    f'{animatedWrong} Hack Failed! You have been reported to discord for abusing the API and have been banned from using Discord. ||JOKE||'] 

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
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    await ctx.reply(embed=embed, mention_author=False)      

  @commands.command()
  async def dog(self, ctx):

      """Random picture of a woof"""

      async with ctx.channel.typing():
          async with aiohttp.ClientSession() as cs:
              async with cs.get("https://random.dog/woof.json") as r:
                  data = await r.json()

                  embed = discord.Embed(title="Woof", color=ctx.author.color)
                  embed.set_image(url=data['url'])
                  embed.set_footer(text="Here is a doggo for you!")
                  embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                  await ctx.reply(embed=embed, mention_author=False)

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

    await ctx.reply("https://tenor.com/view/stick-bug-rick-roll-lol-gif-18118062", mention_author=False)


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
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=embed, mention_author=False)


  @commands.command()
  @commands.guild_only()
  async def glass(self, ctx, user: discord.Member = None):
  
  

    """Put a glass overlay on your or someone else\'s avatar!"""

    if user is None:
      user = ctx.author

    with open("Links.json", 'r') as f:
      API = json.load(f)

    avatar = str(user.avatar_url).replace('.webp', '.png').replace('.gif', '.png').replace('?size=1024', '?size=512')

    UFAPI = f"{API['glass']}{avatar}"

    async with request("GET", UFAPI, headers={}) as response:
      if response.status == 200:

        embed = discord.Embed(title="Glass :ghost:", description=f'[Image Link]({UFAPI})',color=discord.Colour.red())
        embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)

        embed.set_image(url=UFAPI)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=embed, mention_author=False)



  @commands.command(aliases=['greyscale'])
  @commands.guild_only()
  async def grayscale(self, ctx, user: discord.Member = None):
  
  

    """Convert your avatar into grayscale!"""

    if user is None:
      user = ctx.author
    avatar = str(user.avatar_url).replace('.webp', '.png').replace('.gif', '.png').replace('?size=1024', '?size=512')
      #API = f.read()

      #print(API)

    embed = discord.Embed(title="Grayscale 🧓", description=f'[Image Link](https://some-random-api.ml/canvas/greyscale/?avatar={avatar}&key=dVYrXeXFuXwdkREnT9zB7efDV)',color=discord.Colour.random())
    embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)

    embed.set_image(url=f"https://some-random-api.ml/canvas/greyscale/?avatar={avatar}&key=dVYrXeXFuXwdkREnT9zB7efDV")
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

    await ctx.reply(embed=embed, mention_author=False)



  @commands.command(aliases=['gay'])
  @commands.guild_only()
  async def rainbow(self, ctx, user: discord.Member = None):
  
  

    """Put a rainbow overlay on your or someone else\'s avatar!"""

    if user is None:
      user = ctx.author
    avatar = str(user.avatar_url).replace('.webp', '.png').replace('.gif', '.png').replace('?size=1024', '?size=512')
      #API = f.read()

      #print(API)

    embed = discord.Embed(title="🌈 Rainbow", description=f'[Image Link](https://some-random-api.ml/canvas/gay/?avatar={avatar}&key=dVYrXeXFuXwdkREnT9zB7efDV)',color=discord.Colour.random())
    embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)

    embed.set_image(url=f"https://some-random-api.ml/canvas/gay/?avatar={avatar}&key=dVYrXeXFuXwdkREnT9zB7efDV")
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

    await ctx.reply(embed=embed, mention_author=False)


  @commands.command(aliases=['inverted'])
  @commands.guild_only()
  async def invert(self, ctx, user: discord.Member = None):
  
  

    """Inverted colors, on your or someone elses avatar."""

    if user is None:
      user = ctx.author
    avatar = str(user.avatar_url).replace('.webp', '.png').replace('.gif', '.png').replace('?size=1024', '?size=512')
      #API = f.read()

      #print(API)

    embed = discord.Embed(title="Inverted", description=f'[Image Link](https://some-random-api.ml/canvas/invert?avatar={avatar}&key=dVYrXeXFuXwdkREnT9zB7efDV)',color=discord.Colour.random())
    embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)

    embed.set_image(url=f"https://some-random-api.ml/canvas/invert/?avatar={avatar}&key=dVYrXeXFuXwdkREnT9zB7efDV")
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

    await ctx.reply(embed=embed, mention_author=False)


  

  @commands.command(aliases=['bright', 'brightness'])
  @commands.guild_only()
  async def brighten(self, ctx, user: discord.Member = None):
  
  

    """TORTURE YOURSELF WITH LIGHT THEME (But brighter)."""

    if user is None:
      user = ctx.author
    avatar = str(user.avatar_url).replace('.webp', '.png').replace('.gif', '.png').replace('?size=1024', '?size=512')
      #API = f.read()

      #print(API)

    embed = discord.Embed(title="BRIGHT", description=f'[Image Link](https://some-random-api.ml/canvas/brightness/?avatar={avatar}&key=dVYrXeXFuXwdkREnT9zB7efDV)',color=discord.Colour.random())
    embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)

    embed.set_image(url=f"https://some-random-api.ml/canvas/brightness/?avatar={avatar}&key=dVYrXeXFuXwdkREnT9zB7efDV")
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

    await ctx.reply(embed=embed, mention_author=False)


  """@commands.command()
  @commands.guild_only()
  async def comment(self, ctx, message: str):
    ""if " " in message:g
      message = message.split("%20")""
    embed=discord.Embed()
    embed.set_image(url=f'https://some-random-api.ml/canvas/youtube-comment/?avatar={ctx.author.avatar_url}&comment={message}&username={ctx.author.name}')
    await ctx.send(embed=embed)"""

  @commands.command(name='text-to-owo', aliases=['owo', 'tto', 'owo_text', 'uwu'])
  async def text_to_owo(self, ctx, *, message):
    """Convert your text to sound owo."""
    e=humor_langs.owofy(message, _print=False)
    await ctx.send(e)


  """@commands.command()
  async def clap(self, ctx, )"""
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

    """Make a wanted poster of you or your friends."""

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


  @commands.command(aliases=['@someone'])
  async def someone(self, ctx):
    mem=[member for member in ctx.guild.members]

    rando=random.choice(mem)
    await ctx.send(f"""@someone ||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| {ctx.author.mention} {rando.mention}""")
    return

def setup(bot):
    bot.add_cog(fun(bot))
