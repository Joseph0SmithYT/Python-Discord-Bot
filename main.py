#! /bin/env python3
import logging
import sys
from colorsys import hsv_to_rgb, rgb_to_hsv
import discord
from discord import app_commands
from dotenv import load_dotenv
import os
import datetime
import json

from jsondatabase import JSONDatabase
load_dotenv('C:/Users/craft/source/repos/Quortle/.env')
TOKEN = os.getenv('COUNTBANNED')  
# print(TOKEN)

intents = discord.Intents.default()
client = discord.Client(intents=intents)    
tree = app_commands.CommandTree(client)
servers = [
    discord.Object(id=1152789940040642560),
    discord.Object(id=998062686610931755)
]

"""
handle_or_tag()

Returns the handle or tag of a user, depending on if they have a discriminator or not
"""
def handle_or_tag(person: discord.User):
    if person.discriminator == "0":
        return f"@{person.name}"
    else:
        return f"{person.name}#{person.discriminator}"

"""
make_quote_embed

Generates an embed for a quote, with a random color
"""
def make_quote_embed(quote: str = None, person: discord.User = None, title: str = None):
    if quote is None:
        quote = ""
    else:
        quote = f"\"{quote}\""
    random_color = discord.Color.random().to_rgb()
    random_color = rgb_to_hsv(random_color[0], random_color[1], random_color[2])
    random_color = hsv_to_rgb(random_color[0], random_color[1], 1)
    random_color = discord.Color.from_rgb(int(random_color[0] * 255), int(random_color[1] * 255), int(random_color[2] * 255))
    embed = discord.Embed(
        title=title,
        description=quote,
        color=random_color
    )
    embed.set_author(name="Quortle", icon_url=client.user.display_avatar.url)
    embed.set_thumbnail(url=person.display_avatar.url)
    embed.set_footer(text=f"Added on {datetime.datetime.today().strftime('%d/%m/%Y')} at {datetime.datetime.now().strftime('%H:%M')}")
    return embed

"""
! add_quote <person> <quote>

Adds a quote to the database
"""
@tree.command(
    name="add_quote",
    description="Adds a quote",
    guilds=servers
)
async def add_quote(interaction, person: discord.User, quote: str):
    db = JSONDatabase("quotes.json")
    rightnowTime = datetime.datetime.now().strftime("%H:%M")
    db.add_quote(person.id, quote, rightnowTime, datetime.date.today().strftime("%d/%m/%Y"))
    quote = db.get_quotes(person.id)[-1]
    embed = make_quote_embed(quote=quote['quote'], person=person, title=f"Added quote for {handle_or_tag(person)}")
    await interaction.response.send_message(embed=embed)

"""
! get_quotes <person>

Gets the quotes from the database and lists it
"""
@tree.command(
    name="get_quotes",
    description="Gets quotes",
    guilds=servers
)
async def get_quotes(interaction, person: discord.User):
    db = JSONDatabase("quotes.json")
    quotes = db.get_quotes(person.id)
    embed = make_quote_embed(title=f"Quotes for {handle_or_tag(person)}", person=person)
    embed.set_footer(text=f"As of {datetime.datetime.today().strftime('%d/%m/%Y')} at {datetime.datetime.now().strftime('%H:%M')}")
    if quotes == None or len(quotes) == 0:
        embed.add_field(name="No quotes found", value="Add one with /add_quote", inline=False)
    else:
        for quote in quotes:
            embed.add_field(name=f"\"{quote['quote']}\"", value=f"Added on {quote['date']} at {quote['time']}" ,inline=False)
    await interaction.response.send_message(embed=embed)

"""
! remove_quote <person> <quote>

Removes the quote from the database
"""
@tree.command(
    name="remove_quote",
    description="Removes a quote",
    guilds=servers
)
async def remove_quote(interaction, person: discord.User, quote: str):
    db = JSONDatabase("quotes.json")
    db.remove_quote(person.id, quote)
    embed = make_quote_embed(quote=quote, person=person, title=f"Removed quote for {handle_or_tag(person)}")
    await interaction.response.send_message(embed=embed, ephemeral=True)

"""
clear [person]

Clears a person's quote from the database, if no person is specified, clears all quotes
"""
@tree.command(
    name="clear",
    description="Clears",
    guilds=servers
)
async def clear_quotes(interaction, person: discord.User = None):
    if interaction.user.id == 511296836078796820:
        db = JSONDatabase("quotes.json")
        if person:
            for quote in db.get_quotes(person.id):
                print(quote)
                db.remove_quote(person.id, quote['quote'])
            await interaction.response.send_message(f"Cleared quotes for {person.name}#{person.discriminator}.")
        else:
            db.clear()
            await interaction.response.send_message("Cleared quotes.")

"""
! Admin Required!!
/ quit

Quits the bot
"""
@tree.command(
    name="quit",
    description="Quits",
    guilds=servers
)
async def quit_bot(interaction):
    if interaction.user.id == 511296836078796820:
        embed = make_quote_embed(quote="Goodbye!", person=interaction.user, title="Quitting")
        await interaction.response.send_message(embed=embed)
        await client.close()
    else:
        await interaction.response.send_message("You don't have permission to do that! :(")
        
@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as @{handle_or_tag(client.user)}")

"""
start_bot()

Starts the bot
"""
def start_bot():
    print("Starting...")
    client.run(TOKEN)

if __name__ == "__main__":
    start_bot()