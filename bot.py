
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
		embed.add_field(name='<:D:780326506366500864> mod commands', value='```ban, kick, modrep, modclose, tempban, report```')
		embed.add_field(name='<:C:780327572847853628> User Commands', value='```ping, 8ball,```')
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
        


    

bot.run('OTE0NTMwMDQzNDYyNTcwMDg0.YaOYeQ.hTivCnVeJIDLMSOOFjjh4b39x7w')
