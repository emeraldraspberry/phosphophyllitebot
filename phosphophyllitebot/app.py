import discord
import logging
import io
import time
import sqlite3
import argparse
import datetime
import shlex
import json
from database import Database
from command import Command

def get_token():
    with open('config.json') as json_file:
        data = json.load(json_file)
        return data['token']

class MyClient(discord.Client):
    prompt = "."

    def __init__(self, database):
        super().__init__()
        self.database = database
        self.command = Command()
        

    async def on_ready(self):
        logging.info(f'Logged on as {self.user}!')
        activity = discord.Activity(type=discord.ActivityType.listening, name=".help")
        await client.change_presence(activity=activity)

    ###########################################################################
    #    DYNAMIC METHODS FOR DATABASE                                         #
    ###########################################################################

    async def on_member_update(self, before, after):
        self.database.update(member=after)

    async def on_member_join(self, member):
        self.database.update(member=member)

    async def on_member_remove(self, member):
        self.database.update(member=member)

    ###########################################################################

    async def on_guild_join(self, guild):
        logging.info(f'Joined {guild.name} server!')

    async def on_message(self, message):
        # Avoid recursion
        if message.author == client.user:
            return

        # On command "quote"
        if message.content.startswith(f'{self.prompt}quote'):
            await message.channel.send('No way! I want something cooler.')

        # On command "seen"
        if message.content.startswith(f'{self.prompt}seen'):
            response = self.command.on_seen(message, self.database)
            # Occurs when user input is invalid.
            if response!=None:
                await message.channel.send(response)
                await message.add_reaction(u"\U0001F48E")

        # On command "help"
        if message.content.startswith(f'{self.prompt}help'):
            await message.channel.send("Hello! I'm Phosphophyllite, a bot (gem)"
            +" that is ready to assist you with the best that I can do!\nLet "
            +"me look through the books again...\n\n```.seen [--user=EmeraldRaspberry]```Check how"
            +" much time a human has elapsed with their status "
            +"(like Online, Idle...)")
            await message.add_reaction(u"\U0001F48E")



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.basicConfig(filename="bot_log")
    client = MyClient(database=Database())
    client.run(get_token())
