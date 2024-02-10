from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord import Intents, Client, Message
from responses import get_response


# LOAD TOKEN
load_dotenv()
TOKEN: Final[(str | None)] = os.getenv('DISCORD_TOKEN')


# BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
bot: Client = Client(intents=intents)


# MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('Message was empty')
        return

    try:
        response: str = get_response(user_message)
        
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
    
    if bot .user and bot.user.mentioned_in(message) \
    or isinstance(message.channel, discord.channel.DMChannel):
        username: str = str(message.author)
        user_message: str = message.content
        channel: str = str(message.channel)

        print(f'[{channel}] {username}: {user_message}')
        await send_message(message, user_message)


# MAIN ENTRY POINT
if __name__ == '__main__':
    if not TOKEN:
        print('Token missing!')
    else:
        bot.run(token=TOKEN)