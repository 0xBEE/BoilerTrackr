# BoilerTrackr - Lost and Found Discord Bot for Purdue

<img src="/images/boilertrackr-transparent.png" alt="BoilerTrackr Logo" width="256"/>

**BoilerTrackr** is a Discord bot designed to help **Purdue University** students and community members facilitate the search for lost items on campus. With a few basic commands, you can easily submit any items found on campus, or search through our database to efficiently find your belongings to claim them.

## Features

*   ```/found```: Use this command to submit a lost item to the BoilerTrackr database. Include details like the item's name, description, and the location where it was found. This information will be stored for others to search and claim if they have lost a similar item.
*   ```/lost```: Use this command to view the currently found items stored in the BoilerTrackr database. You can browse through the list to see what other people have found and claim them if it's yours.

**BoilerTrackr** is built using Python, using Discord's API, namely "aiohttp", "aiosqlite", "discord.py" and "discord.py-pagination". While data was originally planned to be stored in a SQLite-based database, we decided to store information locally using a ```.csv``` file as a proof of concept.

## Credits

As a "[Hello World 2023](https://www.hwhack2023.com/)" 24-hour hackathon project, the bot was coded and designed by Jean Gonzalez and Heran Mei.