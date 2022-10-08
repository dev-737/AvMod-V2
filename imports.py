import json
from typing import Optional
import discord
import os

import ast

from discord.ext import commands
import dbl

testers  = [252821261506445314, 739187622634717265, 701727675311587358]


def testers_only():
  async def predicate(ctx):
    if ctx.author.id in testers:
      return True

    else:
      await ctx.send("**This command requires you to be a tester!**")
      return False
  return commands.check(predicate)
      
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

def convert_error(time):
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    return "%d:%d:%d:%d" % (day, hour, minutes, seconds)




def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)




class Test:
    def __init__(self, key, value):
        self.key = key
        self.value = value

data = [
    Test(key=key, value=value)
    for key in ['test', 'other', 'okay']
    for value in range(20)
]

class StaticEmoji:
    def __init__(self):
      pass

    tick = "<:tick:972084759176040448>"
    staff = "<:badge_staff:981766696266268732>"
    yeye = "<:coolyeye:806102750373871617>"
    join = "<:join:802376779087872000>"
    rooSob ="<:rooSob:802383709813866526>"
    note = "<:note:972735279964254268>"
    heheboii = "<:heheboii:976368709528612894>"
    arrow = "<:arrow:885763505049985024>"
    no = "<:no:972087845743394886>"
    new = "<:new:982263577295593502>"
    sad = "<:sad:982306060129955891>"


class statusEmojis:
    def __init__(self):
       pass
    dnd =  "<:status_dnd:982264235893612554>"
    idle =  "<:status_idle:982264359667499098>"
    offline =  "<:status_offline:982264390831198268>"
    online =  "<:status_online:982264461106769970>"

    anim_dnd = "<a:dnd:957197075144114257>"
    anim_online =  "<a:online:957197074540134423>"

class animatedEmojis:
    def __init__(self):
       pass

    amongus = "<a:yesyes_amongus:982297939651227678>"
    staff = "<a:discordstaff_shine:769445529238372373>"
    loadDark = "<a:loaddark:972366633257553930>"
    thonkspin = "<a:thonkspin:982265580545507338>"
    alarm = "<a:alarm:982265874251673670>"
    idk = "<a:idk:982266499991470150>"
    wrong = "<a:wrong:902923242879205478>"
    correct = "<a:correct:902923241692229663>"
    loading = "<a:loading:982267391977357362>"
    swirly_loading = "<a:swirly_load:982267641009958942>"
    thecat = "<a:thecat:982267939505975396>"
    crown = "<a:owner_crown:982268247229472778>"
    vibing = "<a:vibing:972375962903781406>"
    tada = "<a:tada:772393312652886017>"
