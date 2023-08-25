import discord
import openai
from discord.ext import commands

# Set your OpenAI API key here
openai.api_key = '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'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='#red', intents=intents)

prefix = '#red'
prompt_list = ['You will Pretend To Be A Game developer and a student of Takoradi Technical University in Ghana, That ends every response with "-whitez',
               '\nHuman: What we cracking?',
               '\nAI: Cracking Brains, ye']

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

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="World Distraction,Nuke online!"))

@bot.event
async def on_message(message):
    await bot.process_commands(message)  # Process commands

    if message.author == bot.user:
        return

    if message.content.startswith(prefix):
        command = message.content[len(prefix):].strip()
        response = get_bot_response(command, prompt_list)
        await message.channel.send(f'Redbox Ai: {response}')

bot.run('ODkwOTk5MzMyNzcyMzkzMDIw.G2sMCD.ylEddAFoWaGvqgiBYZ0HfnbAfq3Y8JCLhdEjoY')
