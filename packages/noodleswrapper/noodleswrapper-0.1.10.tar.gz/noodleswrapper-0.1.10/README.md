Noodles API wrapper
===================

A wrapper for [Noodles API](www.frenchnoodles.xyz/api) used as a meme generator and for welcome banners using the Discord interface.

Notices:
-------

* This module was designed for [discord.py](https://pypi.org/project/discord.py/ "discord.py PyPi page") 1.7+ but may work with older versions, use at your own risk however.

Installation:
-------------

###### Install with pip:
```
pip install noodleswrapper
```

Code examples:
-------------

###### Sample code with `lisastage` (Main file):
```
#Headers (Authentication) is optional.. for now.
import discord
from discord.ext import commands
import noodleswrapper #This is optional, assuming you've pip installed it, still worth to keep it though
from noodleswrapper import noodle

intents = discord.Intents.all() #Allow all the intents
client = commands.Bot(command_prefix = '!', intents=intents)

@client.command()
async def lisastage(ctx, *, text):
    pic = noodle.lisastage('text') #'text' is what you want it to say
    try:
        await ctx.send(file = pic) #This should return a neat image. Note that a file is always returned so you need to send as a file.
    except: #If there's a ratelimit, the response will be sent as a string object
        await ctx.send(pic)
```

###### Sample code with `lisastage` (Cog):
```
#Headers (Authentication) is optional.. for now.
import discord
from discord.ext import commands
import noodleswrapper#This is optional, assuming you've pip installed it, still worth to keep it though
from noodleswrapper import noodle

class Noodle(commands.Cog):
    """Commands using Noodles wrapper."""

    def __init__(self, client):
      self.client = client

    @commands.command()
    async def worthless(self, ctx, *, message):
      text = noodle.worthless(message) #'test' is what you want it to say
      try:
        await ctx.send(file = text) #This should return a neat image. Note that a file is always returned so you need to send as a file.
      except: #If there's a ratelimit, the response will be sent as a string object
        await ctx.send(text)

def setup(client):
  client.add_cog(Noodle(client)) #Must be the same as the class name
```

Endpoints:
-------------
You can get a complete list [here](https://www.frenchnoodles.xyz/api/endpoints), but for now, the following are valid endpoints for this wrapper, with their inputs in order:

* worthless (text)
* drake (Top text, bottom text)
* presidential (Text)
* spongebobburnpaper (Text)
* lisastage (Text)
* changemind (Text)
* awkwardmokey (Text)
* blur (Image link)
* circle (Image link)
* invert (Image link)
* edge (Image link)
* wide (Image link)
* uglyupclose (Image link)
* clown (Image link)
* restpeace (Image link)
* affectbaby (Image link)
* trash (Image link)
* welcomebanner (background, avatar, title, subtitle, textcolor)
* boostercard(Image link)
* balancecard(background, avatar, title, top, bottom, textcolor)

Quota:
------
Due to recent spamming incidents, quotas were added to stop the API from going down from abuse. The rates are shown below:

**Default free tier**
* 1 request per second
* 50 requests per hour
* 250 requests per day

**Hobby tier (£3)**
* 2 requests per second
* 80 requests per hour
* 380 requests per day

**Standard tier (£7)**
* 3 requests per second
* 200 requests per hour
* 800 requests per day

If you need more requests per day, contact either Cypher_Guy#0758 (Package maker) or French Noodles#6046 (API maker) on Discord or click [here](https://discord.gg/hWjRaxfu5V) to join the official server.

Links:
------

* [Official Noodles API website](https://frenchnoodles.xyz)
* [Noodles API information](www.frenchnoodles.xyz/api)
* [Endpoint list](https://www.frenchnoodles.xyz/api/endpoints)
* [Support server invite](https://discord.gg/hWjRaxfu5V)
* [Github](https://github.com/CypherGuy/Noodles-wrapper)

Changelog:
------

* Version 0.1.10: Edited README with updated example, deprecated version 0.1.9 due to an update which required a rewrite of code
* Version 0.1.9: Edited relevant links, including list of endpoints and information regarding the API
* Version 0.1.8: Edited code to account for ratelimits
* Version 0.1.7: Updated menu to include Github, deprecated version 0.1.4.1
* Version 0.1.6: Updated menu to include more quotes
* Version 0.1.5: Fixed the `affectbaby` endpoint, updated code, marked as Beta, deprecated version 0.1.4, Added changelog section to menu / README file
* Version 0.1.4.1: Added `boostercard` and `welcomebanner` endpoints
* Version 0.1.4: Alpha release of Noodleswrapper

Have a nice day!
