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
from imports import StaticEmoji, convert_error

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

class Errors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            global time, message
            time = error.retry_after
            time = convert_error(time)
            x = time.split(':')
            if x[1] != '0' and x[2] != '0':
                if x[1] == 1:
                    message = f'Use this command after **{x[1]}** hour and **{x[2]}** minutes!'                    
                else:
                    message = f'Retry this command after **{x[1]}** hours and **{x[2]}** minutes!'
            elif x[1] == '0' and x[2] != '0' and x[3] != '0':
                message = f'Retry this command after **{x[2]}** minutes and **{x[3]}** seconds!'
            elif x[3] != '0' and x[1] == '0' and x[2] == '0':
                message = f'Retry this command after **{x[3]}** seconds!'
            await ctx.send(message)
            await ctx.message.add_reaction("⏰")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'**{error}**\n\n')
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
            await ctx.send(error)
        elif isinstance(error, commands.errors.NSFWChannelRequired):
            await ctx.send('You must use this command in a channel marked as **NSFW**.')
        elif isinstance(error, commands.errors.NotOwner):
            await ctx.send('**Owner Only.**')
        elif isinstance(error, commands.errors.NoPrivateMessage):
            await ctx.send("The user has blocked me or has the DM's closed.")
        elif isinstance(error, discord.ext.commands.DisabledCommand):
            await ctx.send('This command is disabled.')
        elif isinstance(error, discord.Forbidden):
            await ctx.send('I do not have permissions for this command!')
        elif isinstance(error, commands.CommandInvokeError):
          await ctx.send(f'```{error}```To learn more, join the support server.')
        elif isinstance(error, commands.errors.MemberNotFound):
            await ctx.send('Please give a valid user!')
        else:
          error = traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__)
          channel = self.bot.get_channel(802184833072758784)
          await channel.send('**Error in the command {}**\n```\n'.format(ctx.command.name) + ''.join(map(str, error)) + '\n```')
          errortype = 'Unspecified'
          for i in range(len(error)):
              for j in errors:
                  if j in error[i]:
                      errortype = j
                      break



    @commands.Cog.listener()
    async def on_guild_join(self, guild):
      goal_channel = self.bot.get_channel(802184831047958590)
      #invite=await guild.text_channels[0].create_invite(reason="Privacy Policy.")
      em=discord.Embed(title=f"{StaticEmoji.join} Join" , description=f"Thank you for adding AvMod, **{guild.name}**!", color=discord.Colour.random())
      em.set_footer(text=f'GUILD ID: {guild.id}')
      em.set_author(name=guild.name, icon_url=guild.icon_url)
      await goal_channel.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
      goal_channel = self.bot.get_channel(802184832137953300)
      em=discord.Embed(title=f"{StaticEmoji.rooSob}> Leave" , description=f"I was kicked from **{guild.name}**! How rude of them. <:sad:796576463063089203>", color=discord.Colour.random())
      em.set_footer(text=f'GUILD ID: {guild.id}')
      em.set_author(name=guild.name, icon_url=guild.icon_url)
      await goal_channel.send(embed=em)




def setup(bot):
    bot.add_cog(Errors(bot))