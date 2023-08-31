import discord
from discord.ext import commands
import openai
import requests

# Set your OpenAI API key here
openai.api_key = ''

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='#red', intents=intents)

prefix = '#red'
prompt_list = [
    'You will Pretend To Be A Game developer and a student of Takoradi Technical University in Ghana, That ends every response with "-whitez',
    '\nHuman: What we cracking?',
    '\nAI: Cracking Brains, ye'
]

# Moderation commands
# (Keep your existing moderation commands as they are)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned. Reason: {reason}')

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked. Reason: {reason}')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason="No reason provided"):
    # You can implement your own way to track warnings
    # For example, you might log warnings to a database
    await ctx.send(f'{member.mention} has been warned. Reason: {reason}')

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason="No reason provided"):
    # You can implement your own way to mute users
    # For example, you might add a "Muted" role
    # and remove their ability to send messages
    await ctx.send(f'{member.mention} has been muted. Reason: {reason}')

# Voice channel commands

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client:
        await voice_client.disconnect()

@bot.command()
async def play(ctx, *, query):
    voice_client = ctx.guild.voice_client
    if not voice_client:
        await ctx.send("I'm not connected to a voice channel. Use `join` command first.")
        return

    # Fetch radio station data from the API
    response = requests.get("http://api.radio-browser.info/json/stations")
    stations = response.json()

    # Find a station matching the query
    selected_station = None
    for station in stations:
        if query.lower() in station['name'].lower():
            selected_station = station
            break

    if not selected_station:
        await ctx.send(f"No radio station found for query '{query}'.")
        return

    stream_url = selected_station['url']
    voice_client.stop()
    voice_client.play(discord.FFmpegPCMAudio(stream_url))

# Events
# (Keep your existing event handlers as they are)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="World Distraction, Nuke online!"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith(prefix):
        command = message.content[len(prefix):].strip()
        response = get_bot_response(command, prompt_list)
        await message.channel.send(f'Redbox Ai: {response}')
    
    await bot.process_commands(message)

# OpenAI interaction
# (Keep your existing OpenAI-related functions as they are)

def get_api_response(prompt: str) -> str | None:
    text = None

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[' Human:', ' AI']
        )

        choices = response.choices[0]
        text = choices.text

    except Exception as e:
        print('ERROR:', e)

    return text

def create_prompt(message: str, pl: list[str]) -> str:
    p_message = f'\nHuman: {message}'
    pl.append(p_message)
    prompt = ''.join(pl)
    return prompt

def get_bot_response(message: str, pl: list[str]) -> str:
    prompt = create_prompt(message, pl)
    bot_response = get_api_response(prompt)

    if bot_response is not None and bot_response.strip():
        pl.append(bot_response)
        pos = bot_response.find('\nAI: ')
        bot_response = bot_response[pos + 5:]
    else:
        bot_response = 'Something Went Wrong...'

    return bot_response

# Run the bot
bot.run('')
