import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import PriceSender
import asyncio

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
hooklink = os.getenv("WEBHOOK_URL")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

secret_role = "test"


@bot.event
async def on_ready():
    print(f"{bot.user.name} has initialised.")
    for guild in bot.guilds:
        # Send to the first text channel the bot can send messages in
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send("Bot is online")
                break


@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx):
    await ctx.message.delete()
    print(f"Clearing messages in {ctx.channel}")
    deleted = await ctx.channel.purge(limit=10000000000)
    print(f"Deleted {len(deleted)} messages.")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} dont fucking say that https://tenor.com/view/caption-caption-meme-meme-random-meme-jerma-gif-3664785851174142772"
        )

    await bot.process_commands(message)


@bot.command()
async def WCheck(ctx):
    print(f"{bot.user.name} has begun the WCheck")
    await ctx.send("Larry is checking woolworths energy drink prices")
    # run wooliesCheck in a async co-coroutine
    asyncio.create_task(asyncio.to_thread(PriceSender.wooliesCheck, hooklink))


@bot.command()
async def hello(ctx):
    await ctx.send(f"your penar will soon be mine {ctx.author.mention}")
    await ctx.author.send(f"Welcome to the server {ctx.author.name}")


@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(
            f"{ctx.author.mention} is now a giggaa nigga with the {secret_role} tag"
        )
    else:
        await ctx.send("Role doesn't exist")


@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(
            f"{ctx.author.mention} is now no longer a giggaa nigga and has had the {secret_role} tag stripped of him"
        )
    else:
        await ctx.send("Role doesn't exist")


@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("Welcome big man")


@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You cant do that little man")
    print(error)


@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said: {msg}")


@bot.command()
async def exdm(ctx, member: discord.Member, *, msg):
    try:
        await member.send(msg)
        await ctx.author.send(f"Sent your message of: '{msg}' to {member.mention}")
    except Exception:
        await ctx.author.send(f"I cannot send a message to {member.mention}")
    await ctx.message.delete()


@bot.command()
async def embedtest(ctx, msg):
    embed = discord.Embed(
        url=str(msg),
        title=f"Embed of {msg}",
        description=msg,
        color=discord.Color.blue(),
    )
    embed.set_image(url="https://thispersondoesnotexist.com/")
    embed.set_thumbnail(url="https://thispersondoesnotexist.com/")

    await ctx.send(embed=embed)
    print(embed)


bot.run(token, log_handler=handler, log_level=logging.DEBUG)
