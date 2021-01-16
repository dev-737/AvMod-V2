import discord
from discord.ext import commands
import json
import random



ashop = [{"Name": "Boeing-737", "ID":"B737", "Price": 5000},
        {"Name": "Mikoyan MiG-29", "ID":"MiG29", "Price": 10000}]

async def open_account(user):

  users =  await get_bank_data()

  if str(user.id) in users:
    return False


  else:
    users[str(user.id)] = {}
    users[str(user.id)]["wallet"] = 0
    users[str(user.id)]["bank"] = 0

  with open ("economy/mainbank.json", "w") as f:
    json.dump(users, f, indent=4, sort_keys=True)
  return True  


async def get_bank_data():
  with open ("economy/mainbank.json", "r") as f:
    users = json.load(f)
  return users 

async def update_bank(user, change = 0, mode = "wallet"):
  users = await get_bank_data()
  users[str(user.id)][mode] += change
  with open("economy/mainbank.json", "w") as f:
    json.dump(users, f, indent=4, sort_keys=True)
  bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
  return bal



async def buy_this(user,item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in ashop:
        name = item["ID"].lower()
        if name == item_name:
            name_ = name
            price = item["Price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("economy/mainbank.json","w") as f:
        json.dump(users,f, indent=4, sort_keys=True)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]


class Economy(commands.Cog, name='💰ECONOMY'):

  def __init__(self, bot):
    self.bot = bot



  @commands.command()
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def shop(self, ctx):

    """Have a loot at the items you can buy!"""

    embed=discord.Embed(title=f"✈️{ctx.guild.name} Shop! ", color=ctx.author.color)
    for item in ashop:
      name = item["Name"]
      ID = item["ID"]
      price = item["Price"]
      embed.add_field(name=name, value=f"ID: `{ID}`\nPrice: `✈️️{price}`", inline=False)
      embed.set_footer(text="You need to atleast buy one item first, to get nitro. ")
    await ctx.send(embed=embed)


  @commands.command()
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def buy(self, ctx,item,amount = 1):

      """Buy some items from the shop!"""

      await open_account(ctx.author)

      res = await buy_this(ctx.author,item,amount)

      if not res[0]:
          if res[1]==1:
              await ctx.send("That Object isn't there!")
              return
          if res[1]==2:
              await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
              return
      await ctx.send(f"You just bought {amount} {item}")


  @commands.command(aliases=["inv"])
  @commands.cooldown(1, 3, commands.BucketType.user)
  async def Inventory(self, ctx):

      """Bought something? Have a look if you have it in your inventory!"""

      await open_account(ctx.author)
      user = ctx.author
      users = await get_bank_data()

      try:
          bag = users[str(user.id)]["bag"]
      except:
          bag = []


      em = discord.Embed(title = "👜Inventory:", color=discord.Colour.dark_theme())
      for item in bag:
          name = item["item"]
          amount = item["amount"]

          em.add_field(name = name, value = amount)    

      await ctx.send(embed = em)    

  @commands.command(aliases=["bal", "b"])
  async def balance(self, ctx, member: discord.Member=None):

      """Check out how much money you have!"""

      if member==None:
        member=ctx.author
      await open_account(member)
      users = await get_bank_data()
      wallet_amt=users[str(member.id)]["wallet"]
      bank_amt=users[str(member.id)]["bank"]
      em = discord.Embed(title = f"{member.name}'s balance.", color=discord.Colour.dark_theme())
      em.add_field(name="Wallet", value=f'`✈️{wallet_amt}`')
      em.add_field(name="Bank", value=f"`✈️{bank_amt}`")
      await ctx.send(embed=em)


  @commands.command()
  @commands.cooldown(1, 60, commands.BucketType.user)
  async def beg(self,ctx):

    """Feeling too poor, and want to beg for money?"""

    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    earnings = random.randrange(200)

    await ctx.send(f"You got `✈️{earnings}` air-coins!")

    users[str(user.id)]["wallet"] += earnings
    with open ("economy/mainbank.json", "w") as f:
      json.dump(users, f, indent=4, sort_keys=True)


  @commands.command(aliases=["with"])
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def withdraw(self,ctx, amount=None):


    """Withdraw some money from your bank!"""

    await open_account(ctx.author)

    if amount == None:
      await ctx.send("Please input the amount.")
      return
    bal = await update_bank(ctx.author)

    if amount == 'all':
      users = await get_bank_data()
      amount = int(users[str(ctx.author.id)]["bank"])

    amount = int(amount)

    if amount>bal[1]:
      await ctx.send("Bruh, don't try to fool me. You don't have that much! ;-;")
      return
    
    if amount<0:
      await ctx.send("You withdrew nothing? LMFAO")
    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1*amount, "bank")
    await ctx.send(f"You withdrew `✈️{amount}`!")



  @commands.command(aliases=["dep"])
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def deposit(self, ctx, amount=None):


    """Deposite some money from your wallet!"""


    await open_account(ctx.author)

    if amount == None:
      await ctx.send("Please input the amount.")
      return

    bal = await update_bank(ctx.author)


    if amount == 'all':
      users = await get_bank_data()
      amount = int(users[str(ctx.author.id)]["wallet"])

    amount = int(amount)

    if amount > bal[0]:

      await ctx.send("Bruh, don't try to fool me. You don't have that much! ;-;")
      return
    
    if amount<=0:
      await ctx.send("You depositted nothing? LMFAO")
      return
    await update_bank(ctx.author, -1*amount)
    await update_bank(ctx.author, amount, "bank")
    await ctx.send(f"You depositted `✈️{amount}`!")

  @commands.command()
  @commands.cooldown(1, 60, commands.BucketType.user)
  async def slots(self, ctx, amount=None):

    """Feel like gambling? Use this to bet money!"""

    await open_account(ctx.author)

    if amount == None:
      await ctx.send("Please input the amount.")
      return
    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount > bal[0]:
      await ctx.send("Bruh, don't try to fool me. You don't have that much! ;-;")
      return
    
    if amount<=0:
      await ctx.send("You depositted nothing? LMFAO")
      return  
    final = []
    for i in range(3):
      a = random.choice(["🍑", "🍊", "🍐", "🍋"])

      final.append(a)

    await ctx.send(str(final))
    if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
      am = await update_bank(ctx.author, 2*amount)
      await ctx.send(f"You Won {am}")
    else:
      am = await update_bank(ctx.author, -1*amount)
      await ctx.send(f"You Lost {am}!")



  @commands.command(aliases=["g"])
  async def give(self, ctx, member: discord.Member, amount=None):


    """Want to give someone money?"""

    await open_account(ctx.author)
    await open_account(member)

    if amount == None:
      await ctx.send("Please input the amount.")
      return
    bal = await update_bank(ctx.author)

    if amount == 'all':
      users = await get_bank_data()
      amount = int(users[str(ctx.author.id)]["wallet"])
      return
      
    amount = int(amount)
    if amount > bal[0]:
      await ctx.send("Bruh, don't try to fool me. You don't have that much! ;-;")
      return
    
    if amount<=0:
      await ctx.send("You gave them nothing? LMFAO")
      return
    

    await update_bank(ctx.author, -1*amount)
    await update_bank(member, amount, "wallet")
    await ctx.send(f"You gave {member} `✈️{amount}`!")




  @commands.command(description='Get your daily air-coins!')
  @commands.cooldown(1, 86400, commands.BucketType.user)
  async def daily(self,ctx):


    """Claim your daily rewards!"""

    await open_account(ctx.author)

    await update_bank(ctx.author, 2000)


    embed=discord.Embed(title="Here are your daily ✈️Air-coins!\n", description="`2000✈️` were placed in your wallet!\nCome back in 24h to claim your daily reward!", color=discord.Colour.blue())
    await ctx.send(embed=embed)
    

  @commands.command()
  @commands.cooldown(1, 1800, commands.BucketType.user)
  async def work(self,ctx):

    """Work and earn some money!"""


    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    earnings = random.randrange(500)
    responces=[f"You Worked For Ryanair And Earned `✈️{earnings}`!", f"You worked as a Gate Agent at the airport and earned `✈️{earnings}`!", f"You Worked As An ATC and earned `✈️{earnings}`", f"You Flew A 747! Here are `✈️{earnings}` air-coins for you!"]
    await ctx.send(f"{random.choice(responces)}")

    users[str(user.id)]["wallet"] += earnings
    with open ("economy/mainbank.json", "w") as f:
      json.dump(users, f, indent=4, sort_keys=True)


  @commands.command(hidden=True)
  @commands.is_owner()
  async def drop(self, ctx, member: discord.Member, amount=None):
    await open_account(member)
    amount = int(amount)
    if amount == None:
      await ctx.send("Please input the amount.")
      return
    await update_bank(member, amount, "wallet")
    await ctx.send(f"Congrats on winning {member}! You have gotten `✈️{amount}`!")
    await member.send(f"You received `✈️{amount}` for getting the drop! GG!")
    await ctx.message.delete()




def setup(bot):
    bot.add_cog(Economy(bot))

  