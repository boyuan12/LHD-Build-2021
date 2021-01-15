import discord


# start a new discord client
client = discord.Client()

@client.event
async def on_message(message):
    await message.channel.send('Hey Ryan, did you add my points that I suppose to get?')

