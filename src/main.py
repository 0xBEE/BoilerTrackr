import os
from datetime import datetime

import Paginator
import csv

import traceback
import discord

from discord.ext import commands
from discord import Interaction


class Found(discord.ui.Modal, title='Found Item'):
    # what we want.
    itemName = discord.ui.TextInput(
        label='What item did you find?',
        placeholder='Item Name',
    )

    timeFound = discord.ui.TextInput(
        label='When did you find the item?',
        placeholder='Item Time',
    )

    placeFound = discord.ui.TextInput(
        label='Where was the item found?',
        placeholder='Item Location',
    )

    # This is a longer, paragraph style input, where user can submit feedback
    # Unlike the name, it is not required. If filled out, however, it will
    # only accept a maximum of 300 characters, as denoted by the
    # `max_length=300` kwarg.
    addInfo = discord.ui.TextInput(
        label='Include any additional information (optional)',
        style=discord.TextStyle.long,
        placeholder='Type additional information here...',
        required=False,
        max_length=300,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message('Thanks! Submit an image of the item to the channel within 60 seconds.',
                                                ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents,
                   case_insensitive=False)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print('Logged in as {0.user}'.format(bot))

    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('Finding your items...'))


@bot.command()
async def sync(ctx):
    print("sync command")
    if ctx.author.id == 749412320261701713:
        await bot.tree.sync()
        await ctx.send('Command tree synced.')
    else:
        await ctx.send('You must be the owner to use this command!')


@bot.tree.command(name="found", description="Report a lost item that you found.", )
async def found(interaction: Interaction):
    found_modal = Found()
    await interaction.response.send_modal(found_modal)

    def check(m):
        return m.channel == interaction.channel and m.author.id == interaction.user.id

    try:
        message = await bot.wait_for('message', check=check, timeout=60.0)
        if len(message.attachments) > 0:
            image_url = message.attachments[0].url
            field_names = ['what', 'where', 'when',
                           'imageLink', 'extraInfo', 'reporter', 'timePosted']

            dict = {'what': found_modal.itemName, 'where': found_modal.placeFound, 'when': found_modal.timeFound,
                    'imageLink': image_url, 'extraInfo': found_modal.addInfo,
                    'reporter': interaction.user.id, 'timePosted': datetime.now()}

            with open('res/lost_items.csv', 'a') as f_object:
                dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)
                dictwriter_object.writerow(dict)
                f_object.close()
            await interaction.followup.send("Submission complete.")
        else:
            await interaction.followup.send("No image attached.")

    except TimeoutError:
        await interaction.followup.send("You didn't send an image link in time.", ephemeral=True)


@bot.tree.command(name="lost", description="View a list of lost items.")
async def lost(interaction: Interaction):
    embeds = []

    with open('res/lost_items.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            user = bot.get_user(int(row["reporter"]))
            embed = discord.Embed(color=0x00c7fc,
                                  timestamp=datetime.strptime(row["timePosted"], '%Y-%m-%d %H:%M:%S.%f'))
            embed.set_footer(text=f"Reported by: {user.name}", icon_url=user.avatar.url)
            # TODO: implement check on whether image link is valid
            if row["imageLink"] != "":
                embed.set_thumbnail(url=row["imageLink"])
            embed.add_field(name="What", value=row["what"], inline=True)
            embed.add_field(name="Where", value=row["where"], inline=True)
            embed.add_field(name="When", value=row["when"], inline=True)
            if row["extraInfo"] != "":
                embed.add_field(name="Additional Info", value=row["extraInfo"], inline=False)

            embeds.append(embed)

    if not embeds:
        await interaction.response.send_message("No lost items right now.")
    else:
        await Paginator.Simple().start(interaction, pages=embeds)


try:
    bot.run(os.getenv("TOKEN"))
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
    else:
        raise e
