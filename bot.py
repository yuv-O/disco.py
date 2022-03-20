
import asyncio
from itertools import cycle
from os import name
import discord
import random
from discord import message
from discord.ext import commands
import json
from discord.ext import commands, tasks
from discord.ext.commands.converter import MemberConverter               
logo = 'https://cdn.discordapp.com/icons/780278916173791232/9dbc0f39d731c76be13b4ed9fa471570.webp?size=1024'


def get_prefix(client, message):
    with open('prefixes.json','r')as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)] 

bot = commands.Bot(command_prefix= get_prefix)

@bot.event 
async def on_ready():
    print('bot is ready.')
bot.remove_command('help')      
@bot.command(name="reminder", description="reminds you something after said amount of time.", case_insensitive = True, aliases = ["remind", "remindme", "remind_me"])
@commands.bot_has_permissions(attach_files = True, embed_links = True)
async def reminder(ctx, time, *, reminder):
	await ctx.respond()
	print(time)
	print(reminder)
	user = ctx.message.author
	embed = discord.Embed(color=0x2F3136)
	embed.set_footer(text="oh yhey", icon_url=f"{logo}")
	seconds = 0
	if reminder is None:
		embed.add_field(name='Warning', value=' Run the command again but specify what do you want me to remind you about.') # Error message
	if time.lower().endswith("d"):
		seconds += int(time[:-1]) * 60 * 60 * 24
		counter = f"{seconds // 60 // 60 // 24} days"
	if time.lower().endswith("h"):
		seconds += int(time[:-1]) * 60 * 60
		counter = f"{seconds // 60 // 60} hours"
	elif time.lower().endswith("m"):
		seconds += int(time[:-1]) * 60
		counter = f"{seconds // 60} minutes"
	elif time.lower().endswith("s"):
		seconds += int(time[:-1])
		counter = f"{seconds} seconds"
	if seconds == 0:
		embed.add_field(name='Warning',
						value='Please specify a proper duration, do `!help reminder` for more information.')
	elif seconds < 300:
		embed.add_field(name='Warning',
						value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
	elif seconds > 7776000:
		embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
	else:
		beforermd = discord.Embed(title='Reminder Set', description=f'You will be reminded in {counter}', color=0x2F3136)
		beforermd.set_footer(text='Discord.py For Beginners', icon_url=logo)
		afterrmd = discord.Embed(title='Reminder', description=f'**Your reminder:** \n {reminder} \n\n *reminder set {counter} ago*', color=0x2F3136)
		afterrmd.set_footer(text='Discord.py For Beginners', icon_url=logo)
		await ctx.send(embed=beforermd)
		await asyncio.sleep(seconds)
		await ctx.send(embed=afterrmd)
		return
	await ctx.send(embed=embed)
@bot.event 
async def on_guild_join(guild): 
       with open('prefixes.json','r')as f:
        prefixes = json.load(f)
        prefixes[str(guild.id)] = '>'

       with open('prefixes.json', "w")as f:
        json.dump(prefixes, f, indent=4)

@bot.event 
async def on_guild_remove(guild):
     with open('prefixes.json','r')as f:
         prefixes = json.load(f)
     prefixes.pop(str(guild.id))     
                      

        
     with open('prefixes.json', "w")as f:
        json.dump(prefixes, f, indent=4)

@bot.command()
@commands.has_permissions(administrator=True)
async def changeprefix(ctx,prefix):
     with open('prefixes.json','r')as f:
        prefixes = json.load(f)
        await ctx.send(f'changed')

     prefixes[str(ctx.guild.id)] = prefix


     with open('prefixes.json', "w")as f:
       json.dump(prefixes, f, indent=4) 
@bot.command(name="help", description="Shows all commands")
async def help(ctx, command=None):
	if command is None:
		embed = discord.Embed(timestamp=ctx.message.created_at, title='probts Official Bot', description='You can do `prefix help <command>` to get more info about the command.', color=0x2F3136)
		embed.add_field(name=' mod commands', value='```ban, kick, modrep, modclose, tempban,clear,changeprifix, report```')
		embed.add_field(name=' User Commands', value='```ping, 8ball,```')
		embed.set_footer(text='probt discord', icon_url=logo)
		await ctx.send(embed=embed)   
Status=cycle(['prifix > ,''playing help'])
@bot.event
async def on_ready():
    change_Status.start()
    print('bot is ready.')
@tasks.loop(seconds=10)
async def change_Status():
    await bot.change_presence(activity=discord.Game(next(Status)))

@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: MemberConverter, *, reason=None):
    await ctx.guild.ban(member)
    await ctx.send(f'banned {member.mention}')
@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'kicked {member.mention}')

class Durationconverter(commands.Converter):
    async def convert(self,ctx,argument):
        ammount= argument[:-1]
        unit= argument[-1]

        if ammount.isdigit()and unit in ['s','m']:
            return (int(ammount),unit)

        raise commands.BadArgument(message='Not a valid duration')

@bot.command(name="modclose", description="Closes Modmail Conversation")
async def modclose(ctx, user: discord.Member):
	await ctx.respond()
	if ctx.author.guild_permissions.ban_members:
		if ctx.channel.category_id ==914529379617501187:
			notification = discord.Embed(title='ModMail Ended', description='This Modmail conversation has been ended, the Staff has been disconnected from the conversation.', color=0x2F3136)
			notification.set_footer(text='Discord.py For Beginners', icon_url=f'{logo}')
			await user.send(embed=notification)
			await ctx.send('<:S:790882958574616616> ModMail Ended. Deleting Channel in 5 seconds')
			await asyncio.sleep(5)
			await ctx.channel.delete(reason='ModMail Support Ended.')
		else:
			await ctx.message.delete()
			await ctx.send('<:F:780326063120318465> This channel is not a ModMail channel.', delete_after=3)
	else:
		await ctx.message.delete()
		await ctx.send('<:F:780326063120318465> You are not a Administrator, and this is not a ModMail Channel.', delete_after=5)





@bot.command()
@commands.has_permissions(administrator=True)
async def tempban(ctx, member: commands.MemberConverter, duration:Durationconverter):

    multiplier = {'s': 1 , 'm':60}
    amount, units =duration
    await ctx.guild.ban(member)
    await ctx.send (f'{member} has been banned for {amount}{units}.')
    await asyncio.sleep(amount*multiplier[units])
    await ctx.guild.unban(member)

@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator =member.split('#')


    for ban_entery in banned_users:
        user = ban_entery.user

        if(user.name, user.discriminator)==(member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned welcome back boy! {user.mention}')
            return    





   

@bot.command()
async def ping(ctx):
    await ctx.send(f'hello cutie {round(bot.latency * 1000)}ms')

@bot.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question):
    responses = ['it is certain.',
                 'it is decidedly so.',
                 'without a doubt.',
                 'yes _ definitely.',
                 'you may rely on it.',
                 'as i see it, yes.',
                 'most likely.'
                 'outlook good.',
                 'yes.',
                 'signs point to yes.',
                 'reply hazy, try again.',
                 'ask again later.',
                 'better not tell you now.',
                 'cannot predict now.',
                 'concentrate and ask again.',
                 "don't count on it.",
                 'my reply is no.',
                 'my sources say no.',
                 'outlook not so good.',
                 'very doubtful.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

        

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=40):
    await ctx.channel.purge(limit=amount)

@bot.event
async def on_member_join(member):

    print(f'{member} has joined a server.')

@bot.event
async def on_member_remove(member):
    print(f'{member} has left a server.')

@bot.command()
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error,commands.CommandNotFound):
        await ctx.send('invalid command.')
        
game = {
    "high_score": 0,
    "current_score": 0,
    "games_played": 0,
    "game": False,
    "head": [1, 1],
    "length": 0,
    "direction": 6,
    "body": [],
    "grid": [
        [4, 4, 4, 4, 4, 4, 4, 4],
        [4, 3, 3, 3, 3, 3, 3, 4],
        [4, 3, 3, 3, 3, 3, 3, 4],
        [4, 3, 3, 3, 3, 3, 3, 4],
        [4, 3, 3, 3, 3, 3, 3, 4],
        [4, 3, 3, 3, 3, 3, 3, 4],
        [4, 3, 3, 3, 3, 3, 3, 4],
        [4, 4, 4, 4, 4, 4, 4, 4]
    ],# Just for reference
    "elements": {
        0: ":green_circle:", # Snake Head
        1: ":green_square: ", # Snake Body
        2: ":white_large_square:", # Background
        3: ":bricks:", # Walls
        4: ":green_square:" # Food
    },
    "spawn_food": True,
    "food": []
}


class Snake_Bot(discord.bot):
    async def on_ready(self):
        print('Logged in as {0}'.format(self.user))
    
    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.channel.name == 'snake_game':
            if message.content.startswith('!start'):
                if game['game']:
                    return await message.channel.send('A game is already going on.')
                await message.channel.send('Starting a new game.')
                await self.start_game(message)

    async def start_game(self, message):
        game['game'] = True
        game['games_played'] += 1
        await message.channel.send(f'This will be game number {game["games_played"]}')
        await self.update_grid(message)

    async def update_grid(self, message):
        if game['length'] > 0:
            game['body'].insert(0, game['head'].copy())
            game['body'].pop(-1)

        if game['direction'] == 2:
            game['head'][0] += 1
        elif game['direction'] == 4:
            game['head'][1] -= 1
        elif game['direction'] == 6:
            game['head'][1] += 1
        elif game['direction'] == 8:
            game['head'][0] -= 1

        if game['head'] == game['food'] and not game['spawn_food']:
            game['current_score'] += 1
            game['spawn_food'] = True
            game['length'] += 1
            body_add = game['head'].copy()
            if game['length'] > 1:
                body_add = game['body'][-1].copy()
            if game['direction'] == 2:
                body_add[0] -= 1
            elif game['direction'] == 4:
                body_add[1] += 1
            elif game['direction'] == 6:
                body_add[1] -= 1
            elif game['direction'] == 8:
                body_add[0] -= 1
            game['body'].insert(0, body_add)

        while game['spawn_food']:
            game['food'] = [random.randint(1, 6), random.randint(1, 6)]
            if game['food'] not in game['body'] and game['food'] != game['head']:
                game['spawn_food'] = False

        plot = await self.plot_grid()
        message = await message.channel.send(plot)
        clockwise = '\U0001F503'
        counter_clockwise = '\U0001F504'
        await message.add_reaction(counter_clockwise)
        await message.add_reaction(clockwise)

        time.sleep(5)
        message = await message.channel.fetch_message(message.id)
        clockwise_reactions = discord.utils.get(message.reactions, emoji='🔃')
        counter_clockwise_reactions = discord.utils.get(message.reactions, emoji='🔄')
        
        if clockwise_reactions and counter_clockwise_reactions:
            if clockwise_reactions.count > counter_clockwise_reactions.count:
                if game['direction'] == 2:
                    game['direction'] = 4
                elif game['direction'] == 4:
                    game['direction'] = 8
                elif game['direction'] == 6:
                    game['direction'] = 2
                elif game['direction'] == 8:
                    game['direction'] = 6
            elif clockwise_reactions.count < counter_clockwise_reactions.count:
                if game['direction'] == 2:
                    game['direction'] = 6
                elif game['direction'] == 4:
                    game['direction'] = 8
                elif game['direction'] == 6:
                    game['direction'] = 8
                elif game['direction'] == 8:
                    game['direction'] = 4

        if not (await self.game_over_check(message)):
            await self.update_grid(message)
        
    async def plot_grid(self):
        plot = ""
        for x in range(0, 8):
            for y in range(0, 8):
                if [x, y] == game['head']:
                    plot += game['elements'][0]
                elif [x, y] in game['body']:
                    plot += game['elements'][1]
                elif [x, y] == game['food']:
                    plot += game['elements'][4]
                elif x == 0 or y == 0 or x == 7 or y == 7:
                    plot += game['elements'][3]
                else:
                    plot += game['elements'][2]
            plot += '\n'
        return plot
    
    async def game_over_check(self, message):
        if game['head'][0] == 0 or game['head'][0] == 7 or game['head'][1] == 0 or game['head'][1] == 7:
            await message.channel.send(f'Game Over!\nCurrent Score: {game["current_score"]}\nHigh Score: {game["high_score"]}')
            if game["current_score"] > game["high_score"]:
                game["high_score"] = game["current_score"]
                await message.channel.send("New High Score!!")
            game['game'] = False
            game['head'] = [1, 1]
            game['length'] = 0
            game['direction'] = 6
            game['body'] = []
            game['spawn_food'] = True
            game['food'] = []
            return True
        if game['head'] in game['body']:
            await message.channel.send(f'Game Over!\nCurrent Score: {game["current_score"]}\nHigh Score: {game["high_score"]}')
            if game["current_score"] > game["high_score"]:
                game["high_score"] = game["current_score"]
                await message.channel.send("New High Score!!")
            game['game'] = False
            game['head'] = [1, 1]
            game['length'] = 0
            game['direction'] = 6
            game['body'] = []
            game['spawn_food'] = True
            game['food'] = []
            return True
        return False

    

bot.run('OTE0NTMwMDQzNDYyNTcwMDg0.YaOYeQ.hTivCnVeJIDLMSOOFjjh4b39x7w')
