import sys
sys.dont_write_bytecode = True # Prevent __pycache__

import os
import discord
from typing import Final
from llm import get_response
from dotenv import load_dotenv
from discord import Intents, Client, Message


# LOAD ENV
load_dotenv()

TOKEN: Final[(str | None)] = os.getenv('DISCORD_TOKEN')

assert TOKEN is not None


# BOT SETUP
intents: Intents = Intents.default()
intents.messages = True
bot: Client = Client(intents=intents)


# MESSAGE FUNCTIONALITY
async def send_message(message: Message, username:str, user_message: str) -> None:
    try:
        response: str = get_response(username, user_message)

        response = f'{message.author.mention} {response}' \
        if bot.user and bot.user.mentioned_in(message) \
        else response
        
        await message.channel.send(response)

    except Exception as e:
        print(e)


# HANDLING BOT STARTUP
@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is now running.')


# HANDLING BOT STARTUP
@bot.event
async def on_message(message: Message) -> None:
    if message.author == bot.user:
        return
    
    if bot.user and bot.user.mentioned_in(message) \
    or isinstance(message.channel, discord.channel.DMChannel):
        
        username: str = message.author.display_name
        user_message: str = message.content.replace(bot.user.mention, '').strip()
        channel: str = str(message.channel)

        if not user_message:
            print('Message was empty')
            return
        
        print(f'[{channel}] {username}: {user_message}')
        await send_message(message, username, user_message)


# MAIN ENTRY POINT
if __name__ == '__main__':
    bot.run(TOKEN)
