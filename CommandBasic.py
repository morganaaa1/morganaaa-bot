import random
import time
from datetime import datetime
from nextcord.ext import commands
import asyncio
from nextcord import File
import nextcord, youtube_dl, os
from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io

queuelist = []
filestodelete = []

intents = nextcord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)


@bot.event
async def on_ready():
  print("Bot is Ready!")


# Command that u can test ur Connection
@bot.command()
async def ping(ctx):
  start_time = time.time()
  message = await ctx.send(
    embed=nextcord.Embed(title="Pinging...", color=0xff00ff))
  elapsed_time = time.time() - start_time
  embed = nextcord.Embed(title="Pong!", color=0x00ff00)
  embed.add_field(name="Latency",
                  value=f"{elapsed_time*1000:.0f}ms",
                  inline=True)
  embed.add_field(name="API Latency",
                  value=f"{bot.latency*1000:.0f}ms",
                  inline=True)
  await message.edit(embed=embed)


# Command that u can play coin flip
@bot.command()
async def coinflip(ctx):
  num = random.randint(1, 2)

  if num == 1:
    await ctx.send("Heads")
  if num == 2:
    await ctx.send("Tails")


# Command that we can play Rock, Paper, and Scissors
@bot.command()
async def rps(ctx, hand):
  hands = ["✌️", "✋", "✊"]
  bothand = random.choice(hands)
  await ctx.send(bothand)

  if hand == bothand:
    await ctx.send("its a draw!")
  elif hand == "✌️":
    if bothand == "✊":
      await ctx.send("i won!!")
    if bothand == "✋":
      await ctx.send("you won!!")
  elif hand == "✋":
    if bothand == "✌️":
      await ctx.send("i won!!")
    if bothand == "✊":
      await ctx.send("you won!!")
  elif hand == "✊":
    if bothand == "✋":
      await ctx.send("i won!!")
    if bothand == "✌️":
      await ctx.send("you won!!")


# Command help bot
@bot.command(aliases=["about"])
async def help(ctx):
  MyEmbed = nextcord.Embed(
    title="Commands",
    description="These are the commands that you can use for this bot",
    color=nextcord.Colour.dark_purple())
  MyEmbed.set_author(
    name="Ali Nabilah Ramadhan",
    url="https://twitter.com/ampaskopi1126",
    icon_url=
    "https://scontent-cgk1-2.cdninstagram.com/v/t51.2885-19/299848341_791344618882809_3466426253983729388_n.jpg?stp=dst-jpg_s150x150&_nc_ht=scontent-cgk1-2.cdninstagram.com&_nc_cat=109&_nc_ohc=6w6fHNQ92s8AX8d3K-5&edm=ACWDqb8BAAAA&ccb=7-5&oh=00_AfC0jcQfWqInjwreD_GYEsteUARoh-s-6KAASBEs-9Ivcg&oe=6404F454&_nc_sid=1527a3"
  )
  MyEmbed.set_thumbnail(url="https://i.imgur.com/EaCCLfz.png")
  MyEmbed.add_field(name="!ping",
                    value="This Command for test ur connection",
                    inline=False)
  MyEmbed.add_field(name="!coinflip",
                    value="This Command lets u flip a coin",
                    inline=False)
  MyEmbed.add_field(
    name="!rps",
    value=
    "This Command allows u to play a game of rock pape scissors with the bot",
    inline=False)
  await ctx.send(embed=MyEmbed)


# For Admin/Owner Commands
@bot.group()
async def edit(ctx):
  pass


# Command for change name of the server
@edit.command()
async def servername(ctx, *, input):
  if ctx.author != ctx.guild.owner:
    await ctx.send("Sorry, only the server owner can use this command.")
    return
  await ctx.guild.edit(name=input)


# Command for change region of the server
@edit.command()
async def region(ctx, *, input):
  if ctx.author != ctx.guild.owner:
    await ctx.send("Sorry, only the server owner can use this command.")
    return
  await ctx.guild.edit(region=input)


# Command for add or create a new text channel
@edit.command()
async def createtextchannel(ctx, *, input):
  if ctx.author != ctx.guild.owner:
    await ctx.send("Sorry, only the server owner can use this command.")
    return
  await ctx.guild.create_text_channel(name=input)


# Command for add or create a new voice channel
@edit.command()
async def createvoicechannel(ctx, *, input):
  if ctx.author != ctx.guild.owner:
    await ctx.send("Sorry, only the server owner can use this command.")
    return
  await ctx.guild.create_voice_channel(name=input)


# Command for add or create a new role
@edit.command()
async def createrole(ctx, *, input):
  if ctx.author != ctx.guild.owner:
    await ctx.send("Sorry, only the server owner can use this command.")
    return
  await ctx.guild.create_role(name=input)


# Command for kick
@bot.command()
async def kick(ctx, member: nextcord.Member, *, reason=None):
  if ctx.author != ctx.guild.owner:
    await ctx.send("Sorry, only the server owner can use this command.")
    return
  await ctx.guild.kick(member, reason=reason)


# Command for ban
@bot.command()
async def ban(ctx, member: nextcord.Member, *, reason=None):
  if ctx.author != ctx.guild.owner:
    await ctx.send("Sorry, only the server owner can use this command.")
    return
  await ctx.guild.ban(member, reason=reason)


# Clear chat command
@bot.command()
async def purge(ctx,
                amount,
                day: int = None,
                month: int = None,
                year=datetime.now().year):
  if ctx.author != ctx.guild.owner:
    await ctx.send("Sorry, only the server owner can use this command.")
    return
  if amount == "/":
    if day == None or month == None:
      return
    else:
      await ctx.channel.purge(after=datetime(year, month, day))
  else:
    await ctx.channel.purge(limit=int(amount) + 1)


# This command mutes a specified user
@bot.command()
async def mute(ctx, user: nextcord.Member):
  if ctx.author != ctx.guild.owner:
    await ctx.send("Sorry, only the server owner can use this command.")
    return
  await user.edit(mute=True)
  embed = nextcord.Embed(title="Mute Command",
                         description=f"{user} has been muted.",
                         color=0x00ff00)
  await ctx.send(embed=embed)


# This command unmutes a specified user
@bot.command()
async def unmute(ctx, user: nextcord.Member):
  if ctx.author != ctx.guild.owner:
    await ctx.send("Sorry, only the server owner can use this command.")
    return
  await user.edit(mute=False)
  embed = nextcord.Embed(title="Unmute Command",
                         description=f"{user} has been unmuted.",
                         color=0x00ff00)
  await ctx.send(embed=embed)


# This command deafens a specified user
@bot.command()
async def deafen(ctx, user: nextcord.Member):
  if ctx.author != ctx.guild.owner:
    await ctx.send("Sorry, only the server owner can use this command.")
    return

  try:
    await user.edit(deafen=True)
    embed = nextcord.Embed(title="Deafen Command",
                           description=f"{user} has been deafened.",
                           color=0x00ff00)
    await ctx.send(embed=embed)
  except nextcord.Forbidden:
    await ctx.send("I do not have permission to deafen this user.")
  except nextcord.HTTPException:
    await ctx.send("Deafening the user failed. Please try again later.")


# This command undeafens a specified user
@bot.command()
async def undeafen(ctx, user: nextcord.Member):
  if ctx.author != ctx.guild.owner:
    await ctx.send("Sorry, only the server owner can use this command.")
    return

  try:
    await user.edit(deafen=False)
    embed = nextcord.Embed(title="Undeafen Command",
                           description=f"{user} has been undeafened.",
                           color=0x00ff00)
    await ctx.send(embed=embed)
  except nextcord.Forbidden:
    await ctx.send("I do not have permission to undeafen this user.")
  except nextcord.HTTPException:
    await ctx.send("Undeafening the user failed. Please try again later.")


# This command kicks a specified user from the voice channel they are in
@bot.command()
async def voicekick(ctx, user: nextcord.Member):
  if ctx.author != ctx.guild.owner:
    await ctx.send("Sorry, only the server owner can use this command.")
    return

  try:
    await user.edit(voice_channel=None)
    embed = nextcord.Embed(
      title="Voice Kick Command",
      description=f"{user} has been kicked from voice channel.",
      color=0x00ff00)
    await ctx.send(embed=embed)
  except nextcord.Forbidden:
    await ctx.send(
      "I do not have permission to kick this user from the voice channel.")
  except nextcord.HTTPException:
    await ctx.send(
      "Kicking the user from the voice channel failed. Please try again later."
    )


#This bot for welcoming user that join to the server
async def load_image_async(url: str) -> Image.Image:
  async with aiohttp.ClientSession() as session:
    async with session.get(url) as resp:
      buffer = io.BytesIO(await resp.read())
  return Image.open(buffer)


@bot.event
async def on_member_join(member):
  # Load the background image
  bg_image = Image.open('bg.jpg').convert('RGBA')

  # Load the member's avatar
  avatar_image = await load_image_async(str(member.avatar.url))
  avatar_image = avatar_image.resize((500, 500))  # Resize the avatar image
  avatar_image = avatar_image.convert('RGBA')

  # Create a mask for the avatar
  mask = Image.new('L', avatar_image.size, 0)
  draw = ImageDraw.Draw(mask)
  draw.ellipse((0, 0, avatar_image.size[0], avatar_image.size[1]), fill=255)

  # Apply the mask to the avatar
  avatar_image.putalpha(mask)

  # Calculate the center position for the avatar and paste it onto the background
  x = int((bg_image.width - avatar_image.width) / 2)
  y = int((bg_image.height - avatar_image.height) /
          2)  # Move the avatar image up by 100 pixels
  bg_image.alpha_composite(avatar_image, dest=(x, y))

  # Add text to the image
  draw = ImageDraw.Draw(bg_image)
  font = ImageFont.truetype('poppins/Poppins-Bold.otf', size=72)
  text = "WELCOME TO THE SERVER!"
  text_width, text_height = draw.textsize(text, font=font)
  x = int((bg_image.width - text_width) / 2)
  y = int((bg_image.height - text_height - avatar_image.height) /
          2) - 100  # Place the text above the avatar image
  draw.text((x, y), text, font=font, fill=(255, 255, 255))

  # Add name and tag to the image
  font = ImageFont.truetype('poppins/Poppins-Bold.otf', size=72)
  text = f"{member.name}#{member.discriminator}"
  text_width, text_height = draw.textsize(text, font=font)
  x = int((bg_image.width - text_width) / 2)
  y = int(
    (bg_image.height - avatar_image.height) / 2
  ) + avatar_image.height + 50  # Place the name and tag below the avatar image
  draw.text((x, y), text, font=font, fill=(255, 255, 255))

  # Save the image to a file-like object
  img_byte_arr = io.BytesIO()
  bg_image.save(img_byte_arr, format='PNG')
  img_byte_arr.seek(0)

  # Create a discord.py File object from the file-like object
  file = File(fp=img_byte_arr, filename='welcome.png')

  # Send the image in a message
  channel = bot.get_channel(
    1082120018579431535)  # Replace with the ID of your channel
  await channel.send(file=file)


bot.run("MTAyMTc0MTc1NTEwNTgyMDczMw.GqFVee.67IMNWjNmHRhxJHkrFnMaVcwP6LttUQY341Yck")
