import discord
import attachment_processor
import time
import temp

token = None
prefix = None

with open('config.txt') as f:
    lines = f.readlines()
    if len(lines) < 2:
        print("Missing token or prefix!")
        exit(1)
    token = lines[0]
    prefix = str.lower(lines[1])

intents = discord.Intents.default()

intents.guilds = True
intents.guild_messages = True
intents.guild_reactions = True
intents.members = True
intents.messages = True


client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Discord version: {discord.__version__} Logged as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #print(message.attachments[0].url)
    if message.content.startswith(prefix):
        command = str.lower(message.content[len(prefix):].split(" ")[0])
        
        if command == "tiktok.remove":
            if len(message.attachments) > 0:
                for attachment in message.attachments:
                    try:
                        msg = await message.channel.send("Processing your attachment. This might take some time!")
                        startTime = time.time()
                        [output, video_name] = await attachment_processor.process_attachment(attachment, ["mp4"])
                        executionTime = (time.time() - startTime)
                        info = f"Execution time: {str(round(executionTime))}s"
                        await message.channel.send(info, file=discord.File(output))
                        await msg.delete()
                        temp.remove_temp(video_name)
                    except Exception as error:
                        print(error)
                        await message.channel.send(str(error) + " <" + attachment.url + ">")

            else: 
                await message.channel.send("Please provide video with your message")
        else: 
            await message.channel.send("Unknown command")



client.run(token)