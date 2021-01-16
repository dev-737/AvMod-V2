import discord
from discord.ext import commands
from discord.ext import commands

import dbl

class tests(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.dblpy = dbl.DBLClient(self.bot, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc2MTQxNDIzNDc2Nzg4NDMxOCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA2NDAxMzM5fQ.K6nFXKKJSMJ0WVORejXCfj93aMpnr6mt-MHnZ2oM1vs")

    @commands.command()
    async def check_vote(self, ctx):
      e=await self.dblpy.get_user_vote(ctx.author.id)
      if e==False:
        await ctx.send("Not Voted!")
      else:
        await ctx.send("Thanks for voting! :D")

def setup(bot):
    bot.add_cog(tests(bot))