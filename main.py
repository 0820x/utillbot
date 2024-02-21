# Hello, to personalize the bot add your user id to bot_access. Thanks for looking at my bot btw

import discord, colorama, asyncio, random, requests, json
from discord.ext import commands
from colorama import Fore
from discord.ext.commands.core import has_guild_permissions
from requests import get
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)
bot.remove_command('help')
bot_access = [12893021980]
@bot.event
async def on_ready():
    print(f'{Fore.GREEN}[ + ] user = {bot.user}')
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Bat Help Command", color=discord.Color.dark_grey())
    embed.add_field(name="Admin", value=".ban <@> <reason> ~ ban a user\n.kick <@> <reason> ~ kick a user\n.warn <@> <reason> ~ warn a user\n.unban <username> ~ unban a user\n.nick <@> <new nick> ~ change a user's nickname\n.purge <amount> ~ purge messages\n.lock ~ lock current channel\n.unlock ~ unlock current channel\n.setwelcchannel ~ set welcome message channel\n.setwelcmsg ~ set welcome message\n.setwelcrole ~ set welcome role", inline=False)
    embed.add_field(name="Misc", value=".ping ~ check bot's latency\n.serverinfo ~ check server's info\n.joke ~ random joke from api\n.8ball ~ random 8ball response\n.avatar <@> ~ get user's avatar\n.av <@> ~ get user's avatar\n.skullboard ~ skull reaction = skullboard channel\n.snipe ~ snipe recently deleted message\n.s ~ snipe recently deleted message\n.rr ~ send rickroll link\n.afk ~ tell everyone that youre afk\n.back ~ say youre back and how long you were gone\n.news <topic> ~ shows news about a topic\n.stock <symbol> ~ get current price of a stock\n.define <word> ~ get the definition of a word\n.userinfo <@> ~ get simple user info\n.coinflip ~ 50/50 coinflip\n.roll <sides> ~ roll a dice with the ammount of sides\n.catfact ~ random fact about cats\n.meme ~ random meme\n.cat ~ random cat pic\n.dog ~ random dog pic", inline=False)
    embed.add_field(name="Economy", value=".bal ~ check your balance\n.balance ~ check your balance\n.daily ~ 1000-1500 every day\n.work ~ 100-300 every 20 seconds\n.gamble <ammount> ~ 50/50 to double or lose\n.deposit <ammount> ~ deposit money into the bank\n.withdraw <ammount> ~ withdraw money from the bank\n.give <@> <ammount> ~ give money to a user\n.beg ~ 50-200 every minute", inline=False)
    await ctx.send(embed=embed)
@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
  if ctx.author.guild_permissions.administrator:
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned')
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
  if ctx.author.guild_permissions.administrator:
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked')
@bot.command()
async def warn(ctx, member: discord.Member, *, reason=None):
  if ctx.author.guild_permissions.administrator:
    await member.send(f'You have recieved a warning for: {reason}')
    await ctx.send(f'{member.mention} has been warned')
@bot.command()
async def unban(ctx, *, member):
  if ctx.author.guild_permissions.administrator:
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.mention} has been unbanned')
            return
@bot.command()
async def lock(ctx, channel: discord.TextChannel = None):
  if ctx.author.guild_permissions.administrator:
    channel = channel or ctx.channel
    await channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(f'{channel.mention} has been locked')
@bot.command()
async def unlock(ctx, channel: discord.TextChannel = None):
  if ctx.author.guild_permissions.administrator:
    channel = channel or ctx.channel
    await channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(f'{channel.mention} has been unlocked')
@bot.command()
async def ping(ctx):
    latency = bot.latency
    await ctx.send(f'{round(latency * 1000)}ms')
@bot.command()
async def purge(ctx, amount: int):
  if ctx.author.guild_permissions.administrator:
    amount = min(amount, 50)
    await ctx.channel.purge(limit=amount + 1)
@bot.command()
async def nick(ctx, member: discord.Member, new_nick):
  if ctx.author.guild_permissions.administrator:
    await member.edit(nick=new_nick)
    await ctx.send(f'{member.mention} : {new_nick}')
user_balances = {}
user_bank = {}
user_last_claim = {}
user_last_work = {}
user_last_beg = {}
def get_balance(user_id):
    return user_balances.get(user_id, 0)
def get_bank(user_id):
    return user_bank.get(user_id, 0)
@bot.command(aliases=["balance", "bal"])
async def _bal(ctx):
    balance = get_balance(ctx.author.id)
    bank_balance = get_bank(ctx.author.id)
    embed = discord.Embed(title="Balance Information", color=discord.Color.green())
    embed.add_field(name="💵 Wallet Balance", value=balance, inline=False)
    embed.add_field(name="💳 Bank Balance", value=bank_balance, inline=False)
    await ctx.send(embed=embed)
@bot.command()
async def deposit(ctx, amount: int):
    balance = get_balance(ctx.author.id)
    if amount <= 0 or amount > balance:
        await ctx.send("Invalid amount to deposit.")
        return
    user_balances[ctx.author.id] -= amount
    user_bank[ctx.author.id] = user_bank.get(ctx.author.id, 0) + amount
    await ctx.send(f"Deposited {amount} coins into your bank.")
@bot.command()
async def withdraw(ctx, amount: int):
    bank_balance = get_bank(ctx.author.id)
    if amount <= 0 or amount > bank_balance:
        await ctx.send("Invalid amount to withdraw.")
        return
    user_bank[ctx.author.id] -= amount
    user_balances[ctx.author.id] = user_balances.get(ctx.author.id, 0) + amount
    await ctx.send(f"Withdrew {amount} coins from your bank.")
@bot.command()
async def gamble(ctx, amount: int):
    balance = get_balance(ctx.author.id)
    if amount <= 0 or amount > balance:
        await ctx.send("Invalid amount to gamble.")
        return
    outcome = random.choice(['win', 'lose'])
    if outcome == 'win':
        user_balances[ctx.author.id] += amount
        await ctx.send(f"You won {amount} coins! Your balance: {get_balance(ctx.author.id)} coins.")
    else:
        user_balances[ctx.author.id] -= amount
        await ctx.send(f"You lost {amount} coins! Your balance: {get_balance(ctx.author.id)} coins.")
@bot.command()
async def daily(ctx):
    last_claim = user_last_claim.get(ctx.author.id)
    if last_claim and (ctx.message.created_at - last_claim).total_seconds() < 86400:
        await ctx.send("You've already claimed your daily reward today!")
        return
    reward_amount = random.randint(1000, 1500)
    user_balances[ctx.author.id] = user_balances.get(ctx.author.id, 0) + reward_amount
    user_last_claim[ctx.author.id] = ctx.message.created_at
    await ctx.send(f"You claimed your daily reward! You received {reward_amount} coins. Your balance: {get_balance(ctx.author.id)} coins.")
@bot.command()
async def work(ctx):
    last_work = user_last_work.get(ctx.author.id)
    if last_work and (ctx.message.created_at - last_work).total_seconds() < 20:
        await ctx.send("You can work again in a bit.")
        return
    earning = random.randint(100, 300)
    user_balances[ctx.author.id] = user_balances.get(ctx.author.id, 0) + earning
    user_last_work[ctx.author.id] = ctx.message.created_at
    await ctx.send(f"You worked and earned {earning} coins. Your balance: {get_balance(ctx.author.id)} coins.")
@bot.command()
async def beg(ctx):
  last_beg = user_last_beg.get(ctx.author.id)
  if last_beg and (ctx.message.created_at - last_beg).total_seconds() < 60:
      await ctx.send("You can beg again in a bit.")
      return
  earning = random.randint(50, 200)
  user_balances[ctx.author.id] = user_balances.get(ctx.author.id, 0) + earning
  user_last_beg[ctx.author.id] = ctx.message.created_at
  await ctx.send(f"You begged and received {earning} coins. Your balance: {get_balance(ctx.author.id)} coins.")
@bot.command()
async def give(ctx, recipient: discord.Member, amount: int):
  if amount <= 0:
      await ctx.send("Invalid amount to give.")
      return
  if amount > get_balance(ctx.author.id):
      await ctx.send("You don't have enough coins to give that amount.")
      return
  user_balances[ctx.author.id] -= amount
  user_balances[recipient.id] = user_balances.get(recipient.id, 0) + amount
  await ctx.send(f"You gave {recipient.name} {amount} coins. Your balance: {get_balance(ctx.author.id)} coins.")
@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=guild.name, color=discord.Color.blue())
    embed.add_field(name="Owner", value=guild.owner, inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Roles", value=len(guild.roles), inline=True)
    await ctx.send(embed=embed)
welcome_channel = None
welcome_message = None
@bot.command()
async def setwelcchannel(ctx, channel: discord.TextChannel):
  if ctx.author.guild_permissions.administrator:
    global welcome_channel
    welcome_channel = channel
    await ctx.send(f"Welcome channel set to {channel.mention}")
@bot.command()
async def setwelcmsg(ctx, *, message):
  if ctx.author.guild_permissions.administrator:
    global welcome_message
    welcome_message = message
    await ctx.send(f"Welcome message set to:\n{message} {{member}}")
@bot.command()
async def setwelcomerole(ctx, role: discord.Role):
    global welcome_role
    welcome_role = role
    await ctx.send(f"Welcome role set to {role.name}")
@bot.event
async def on_member_join(member):
    if welcome_channel and welcome_message:
        channel = member.guild.get_channel(welcome_channel.id)
        await channel.send(f"{welcome_message} {member}")
    if welcome_role:
      await member.add_roles(welcome_role)
@bot.command()
async def joke(ctx):
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    data = response.json()
    embed = discord.Embed(title=data['setup'], description=data['punchline'], color=discord.Color.random())
    await ctx.send(embed=embed)
@bot.command(aliases=["8ball"])
async def _8ball(ctx):
    responses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
    response = random.choice(responses)
    await ctx.send(response)
@bot.command(aliases=["av"])
async def avatar(ctx, member: discord.Member = None):
    if member == None:
      member = ctx.author
    embed = discord.Embed(title= member).set_image(url = member.avatar.url)
    await ctx.send(embed=embed)
@bot.command()
async def skullboard(ctx):
    if ctx.guild:
        skullboard_channel = discord.utils.get(ctx.guild.channels, name='skullboard')
        if not skullboard_channel:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            skullboard_channel = await ctx.guild.create_text_channel('skullboard', overwrites=overwrites)
            await ctx.send('Skullboard channel created!')
        await ctx.send('You can now use reactions on messages to add them to the skullboard.')
    else:
        await ctx.send('Error: This command can only be used in a server (guild).')
@bot.event
async def on_raw_reaction_add(payload):
    if str(payload.emoji) == '💀':
        guild = bot.get_guild(payload.guild_id)
        channel = guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        skullboard_channel = discord.utils.get(guild.channels, name='skullboard')
        if skullboard_channel:
            embed = discord.Embed(
                title=f"{message.author.display_name}'s message:",
                description=f" ** {message.content} ** ",
                color=0x000000
            )
            await skullboard_channel.send(embed=embed)
sniped_messages = {}
@bot.event
async def on_message_delete(message):
      sniped_messages[message.channel.id] = {
          'content': message.content,
          'author': message.author,
          'timestamp': message.created_at
      }
@bot.command(aliases=['s'])
async def snipe(ctx):
      channel_id = ctx.channel.id
      sniped_message = sniped_messages.get(channel_id)
      if sniped_message:
          embed = discord.Embed(
              description=sniped_message['content'],
              color=discord.Color.blue()
          )
          embed.set_author(name=sniped_message['author'].display_name)
          embed.set_footer(text=f"Sniped by {ctx.author.display_name}")
          await ctx.send(embed=embed)
      else:
          await ctx.send("No recently deleted messages to snipe.")
afk_timers = {}
@bot.command()
async def afk(ctx, *, message): 
    global afk_timers
    if ctx.author.id not in afk_timers:
        afk_timers[ctx.author.id] = asyncio.get_event_loop().time()
        await ctx.reply(f'{ctx.author.display_name} is now afk. Reason: `{message}`')
    else:
        await ctx.reply("You're already afk!")
@bot.command()
async def back(ctx):
    global afk_timers
    if ctx.author.id in afk_timers:
        duration = round(asyncio.get_event_loop().time() - afk_timers[ctx.author.id])
        del afk_timers[ctx.author.id]
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.reply(f"Welcome back, {ctx.author.display_name}! You were afk for {hours} hours, {minutes} minutes, and {seconds} seconds.")
    else:
        await ctx.reply("You're not afk!")
@bot.command()
async def rr(ctx):
    await ctx.reply(f"https://media.tenor.com/x8v1oNUOmg4AAAAd/rickroll-roll.gif")
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title="User Info", description=member.mention, color=discord.Color.blue())
    embed.add_field(name="Username", value=member.name, inline=True)
    embed.add_field(name="User ID", value=member.id, inline=True)
    embed.add_field(name="Status", value=member.status, inline=True)
    embed.add_field(name="Joined at", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.add_field(name="Created at", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    await ctx.send(embed=embed)
@bot.command()
async def news(ctx, topic):
    api_key = "f9728e4f705f407cb40d435c9d2b4294"
    url = f"http://newsapi.org/v2/everything?q={topic}&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    for article in articles:
        await ctx.send(f"{article['title']}: {article['url']}")
@bot.command()
async def stock(ctx, symbol):
    api_key = "7G8DpdJHw4HDgKvZRHz9oO3fTuWXuczw"
    url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    price = data[0]['price']
    await ctx.send(f"The current price of {symbol} is ${price}.")
@bot.command()
async def define(ctx, word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    data = response.json()
    definition = data[0]['meanings'][0]['definitions'][0]['definition']
    await ctx.send(f"The definition of {word} is: {definition}")
@bot.command()
async def say(ctx, *, text):
  if ctx.author.id in bot_access:
    message = ctx.message
    await message.delete()
    await ctx.send(f'{text}')
@bot.command()
async def play1(ctx, *, message):
    if ctx.author.id in bot_access:
        game = discord.Game(
            name=message
        )
        await bot.change_presence(activity=game)
        await ctx.reply(f"Playing `{message}`")
@bot.command()
async def banner(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    req = await bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
    banner_id = req.get("banner")
    if banner_id:
        banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"
        await ctx.send(f"{user.display_name}'s banner: {banner_url}")
    else:
        await ctx.send(f"{user.display_name} doesn't have a banner.")
@bot.command()
async def set_balance(ctx, member: discord.Member, amount: int):
    if ctx.author.id in bot_access:
        user_balances[member.id] = amount
        await ctx.send(f"Balance set to {amount} for {member.mention}.")
    else:
        await ctx.send("You do not have permission to use this command.")
@bot.command()
async def coinflip(ctx):
    result = random.choice(["Heads", "Tails"])
    await ctx.send(f"The coin landed on: {result}")
@bot.command()
async def roll(ctx, sides: int = 6):
    if sides < 2:
        await ctx.send("Number of sides must be at least 2.")
        return
    result = random.randint(1, sides)
    await ctx.send(f"The dice rolled: {result}")
@bot.command()
async def catfact(ctx):
    response = requests.get("https://catfact.ninja/fact")
    data = response.json()
    fact = data["fact"]
    await ctx.send(f"Did you know? {fact}")
@bot.command()
async def meme(ctx):
    response = requests.get("https://meme-api.com/gimme")
    data = response.json()
    image_url = data["url"]
    await ctx.send(image_url)
@bot.command()
async def cat(ctx):
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    data = response.json()
    image_url = data[0]["url"]
    await ctx.send(image_url)
@bot.command()
async def dog(ctx):
    response = requests.get("https://api.thedogapi.com/v1/images/search")
    data = response.json()
    image_url = data[0]["url"]
    await ctx.send(image_url)
bot.run("MTIwMjY4MTE3MjU5ODE5NDMxNg.GkMowO.8vCqbFYTp-0KVt-oGZKvGG0eLU0ztfJsjOo9x8")
