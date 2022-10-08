import requests
from bs4 import BeautifulSoup
import aiohttp
from Flighter import Flighter
import discord
import asyncio
from discord.ext import commands

from imports import animatedEmojis

loadDark = animatedEmojis.loadDark

class aviation(commands.Cog): #, name='✈️ AVIATION'

  def __init__(self, client):
      """Init"""
      self.client = client

   
  @commands.command()
  async def metar(self, ctx, APT):

      """Returns METAR for airport passed as arguement"""

      # print(f"METAR {APT.upper()}")
      embed = discord.Embed(
         title=f"{APT.upper()} METAR", 
         colour=discord.Colour.red(),
         description=await aviation.async_metar(APT)
      )
      embed.set_author(name="Weather", icon_url="https://cdn.discordapp.com/avatars/761414234767884318/a824512ca5391941b1de5b4e1a6e5302.png?size=2048")
      await ctx.send(embed=embed)

  @commands.command()
  async def taf(self, ctx, APT):
     
      """Returns TAF for airport passed as arguement"""

      # print(f"TAF {APT.upper()}")
      embed = discord.Embed(
         title=f"{APT.upper()} TAF", 
         colour=discord.Colour.red(),
         description=await aviation.async_taf(APT)
      )
      embed.set_author(name="AVWeather", icon_url="https://cdn.discordapp.com/avatars/761414234767884318/a824512ca5391941b1de5b4e1a6e5302.png?size=2048")
      await ctx.send(embed=embed)

  @commands.command(aliases=["wx"])
  async def report(self, ctx, APT):
      """Returns airport METAR/TAF passed as arguement"""
      # print(f"Report {APT.upper()}")
      embed = discord.Embed(
         title=f"{APT.upper()} Weather Report", 
         colour=discord.Colour.red()
      )
      embed.set_author(name="AVWeather", icon_url="https://cdn.discordapp.com/avatars/761414234767884318/a824512ca5391941b1de5b4e1a6e5302.png?size=2048")
      embed.add_field(name="METAR", value=await aviation.async_metar(APT), inline=False)
      embed.add_field(name="TAF", value=await aviation.async_taf(APT), inline=False)
      await ctx.send(embed=embed)


  @commands.command()
  async def flighttime(self, ctx, plane, speed: int, icao1, icao2):
    
    """Calculate the flight-time from one airport to another."""

    x = Flighter()
    x.plane = plane # Defualt=None
    x.speed = speed   # Default=0
    x.icao1 = icao1 # Default=None
    x.icao2 = icao2 # Default=None
    try:
      result=x.checkFlight()
    except:
      await ctx.send("Invalid ICAO code.")
      return

    if len(icao1) < 4:
      await ctx.send("ICAO's can only be 4 characters in size.") 
      return
    elif len(icao2) < 4:
      await ctx.send("ICAO's can only be 4 characters in size. Don't try to fool me.") 
      return
    msg = await ctx.send(f"<{loadDark} Calculating...")
    await asyncio.sleep(3)
    embed=discord.Embed(color=discord.Colour.random())
    embed.add_field(name="📥 Input:", value=f' ```- Route: {result["Flight"]}\n- Plane: {result["Plane"]}\n- Speed: {result["Approx. Speed"]}kts```')
    embed.add_field(name="📤 Output: ", value=f"```- Flight Time: {result['Approx. Time']}```", inline=False)
    embed.set_footer(text=f'Requested By: {ctx.author}', icon_url=ctx.author.avatar_url)
    embed.set_author(name="✈️ Flight Time Calculator", icon_url=ctx.bot.user.avatar_url)
    await msg.edit(content=None, embed=embed)


  @commands.command()
  async def airportinfo(self, ctx, icao):

    """Get info about an airport!"""

    x = Flighter()
    try:
      info=x.airportInfo(icao)
    except:
      await ctx.send("**Invalid Airport!**")
      return
    if info['IATA'] != None:
      embed=discord.Embed(color=discord.Colour.random())
      embed.add_field(name="**Name:** ", value=f"```css\n{info['Name']}```\n**Country/State:** ```css\n{info['Country/State']}  ```\n**City:** ```css\n{info['City']}```\n**ICAO:** ```css\n{info['ICAO']}```\n**IATA:** ```css\n{info['IATA']}```\n**Elivation:** ```css\n{info['Elevation']}```\n**Latitude:** ```css\n{info['Latitude']}```\n**Longitude:** ```css\n{info['Longitude']}```\n**Timezone:** ```css\n{info['Timezone']}```")
      embed.set_author(name=f'{icao} Info', icon_url=ctx.bot.user.avatar_url)
      embed.set_footer(text=f'Requested By: {ctx.author}', icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
    else:
      embed=discord.Embed(color=discord.Colour.random())
      embed.add_field(name="**Name:** ", value=f"```css\n{info['Name']}```\n**Country/State:** ```css\n{info['Country/State']}```\n**City:** ```css\n{info['City']}```\n**ICAO:** ```css\n{info['ICAO']}```\n```**Elivation:** ```css\n{info['Elevation']}```\n**Latitude:** ```css\n{info['Latitude']}```\n**Longitude:** ```css\n{info['Longitude']}```\n**Timezone:** ```css\n{info['Timezone']}```")
      embed.set_author(name=f'{icao} Info', icon_url=ctx.bot.user.avatar_url)
      embed.set_footer(text=f'Requested By: {ctx.author}', icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)


   # ------ Static methods not bound to discord ------
  @staticmethod
  def sync_metar(APT="EIDW"):
      """
      Returns (sync) requested airport METAR
      Default airport set to Dublin (EIDW)
      """

      uri = f"https://aviationweather.gov/metar/data?ids={APT}"
      web = requests.get(uri)
      if web.ok:
         soup = BeautifulSoup(web.text, "html.parser")
         try:
            return soup.code.text
         except AttributeError:
            return "Invalid airport"
      else:
         return f"Web error occured. code: {web.status_code}"

  @staticmethod
  def sync_taf(APT="EIDW"):
      """
      Returns (sync) requested airport TAF
      Default airport set to Dublin (EIDW)
      """

      uri = f"https://aviationweather.gov/taf/data?ids={APT}"
      web = requests.get(uri)
      if web.ok:
         soup = BeautifulSoup(web.text, "html.parser")
         try:
            return soup.code.text
         except AttributeError:
            return "Invalid airport"
      else:
         return f"Web error occured. code: {web.status_code}"

  @staticmethod
  async def async_metar(APT="EIDW"):
      """
      Returns (sync) requested airport METAR
      Default airport set to Dublin (EIDW)
      """

      uri = f"https://aviationweather.gov/metar/data?ids={APT}"
      timeout = aiohttp.ClientTimeout(total=10)
      async with aiohttp.ClientSession(timeout=timeout) as sesh:
         async with sesh.get(uri) as web_resp:
            if web_resp.status == 200:
               web = await web_resp.text()
               soup = BeautifulSoup(web, "html.parser")
               try:
                  return soup.code.text
               except AttributeError:
                  return "Invalid airport"
            else:
               return "Warning, Error occured. code: {web_resp.status}"
      return "Warning, request timeout"

  @staticmethod
  async def async_taf(APT="EIDW"):
      """
      Returns (async) requested airport TAF
      Default airport set to Dublin (EIDW)
      """
      
      uri = f"https://aviationweather.gov/taf/data?ids={APT}"
      timeout = aiohttp.ClientTimeout(total=10)
      async with aiohttp.ClientSession(timeout=timeout) as sesh:
         async with sesh.get(uri) as web_resp:
            if web_resp.status == 200:
               web = await web_resp.text()
               soup = BeautifulSoup(web, "html.parser")
               try:
                  return soup.code.text
               except AttributeError:
                  return "Invalid airport"
            else:
               return "Warning, Error occured. code: {web_resp.status}"
      return "Warning, request timeout"

def setup(client):
   client.add_cog(aviation(client))


def main():
   print(" --- Airport METAR / TAF testing --- ")

   # print(Weather.sync_metar("EGLL"))
   # print(Weather.sync_taf("KLAX"))
   # print(Weather.sync_metar())


async def amain():
   print(" --- Airport METAR / TAF testing --- ")

   print(await aviation.async_metar())
   # print(await Weather.async_taf("KLAX"))


if __name__ == "__main__":
   # main()
   asyncio.run(amain())