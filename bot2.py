# This example requires the 'message_content' intent.

import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

TOKEN = "MTE1Mjc4NTUyOTAzNzkzNDY2Mg.GK5yJS.pgXdZ9l0jSBCgwMoI4gxX-Aq_CavRe2wD67jsM"
from discord.utils import get

status_channel = client.get_channel(1170531221776904212)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        channel = client.get_channel(1170531221776904212)  # Replace channel_id with the ID of the desired channel
        await channel.send("Booting up..")

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if message.author == client.user:
            return
        if message.content.startswith("cancri"):
            await message.channel.send("kys")
            return

        desired_user_id = 511296836078796820
        desired_user = get(client.get_all_members(), id=desired_user_id)

        if message.content.startswith("c!shutup"):
            if message.author == desired_user:

                await message.channel.send("Shutting Down...")
                await client.close()
        if message.content.startswith("c!u"):
            if message.author == desired_user:
                await message.channel.send("Updating scripts...")
                await client.logout()
                await client.run(TOKEN)
        if message.content.startswith("c!ping"):
            await message.channel.send("<@511296836078796820>")

    

client = MyClient(intents=intents)
client.run(TOKEN)
