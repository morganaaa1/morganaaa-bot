import nextcord
from nextcord.ext import commands
from nextcord import File
from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io

intents = nextcord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def load_image_async(url: str) -> Image.Image:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            buffer = io.BytesIO(await resp.read())
    return Image.open(buffer)

@bot.event
async def on_member_join(member):
    # Load the background image
    bg_image = Image.open('bg.png').convert('RGBA')

    # Load the member's avatar
    avatar_image = await load_image_async(str(member.avatar.url))
    avatar_image = avatar_image.resize((500, 500)) # Resize the avatar image
    avatar_image = avatar_image.convert('RGBA')

    # Create a mask for the avatar
    mask = Image.new('L', avatar_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, avatar_image.size[0], avatar_image.size[1]), fill=255)

    # Apply the mask to the avatar
    avatar_image.putalpha(mask)

    # Calculate the center position for the avatar and paste it onto the background
    x = int((bg_image.width - avatar_image.width) / 2)
    y = int((bg_image.height - avatar_image.height) / 2) # Move the avatar image up by 100 pixels
    bg_image.alpha_composite(avatar_image, dest=(x, y))

    # Add text to the image
    draw = ImageDraw.Draw(bg_image)
    font = ImageFont.truetype('poppins/Poppins-Black.otf', size=72)
    text = "WELCOME TO THE SERVER!"
    text_width, text_height = draw.textsize(text, font=font)
    x = int((bg_image.width - text_width) / 2)
    y = int((bg_image.height - text_height - avatar_image.height) / 2) - 100  # Place the text above the avatar image
    draw.text((x, y), text, font=font, fill=(255, 255, 255))

    # Add name and tag to the image
    font = ImageFont.truetype('poppins/Poppins-Black.otf', size=72)
    text = f"{member.name}#{member.discriminator}"
    text_width, text_height = draw.textsize(text, font=font)
    x = int((bg_image.width - text_width) / 2)
    y = int((bg_image.height - avatar_image.height) / 2) + avatar_image.height + 50  # Place the name and tag below the avatar image
    draw.text((x, y), text, font=font, fill=(255, 255, 255))

    # Save the image to a file-like object
    img_byte_arr = io.BytesIO()
    bg_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    # Create a discord.py File object from the file-like object
    file = File(fp=img_byte_arr, filename='welcome.png')

    # Send the image in a message
    channel = bot.get_channel(1082120018579431535) # Replace with the ID of your channel
    await channel.send(file=file)

bot.run("MTAyMTc0MTc1NTEwNTgyMDczMw.GikSyk.PqO0KxPSPMR7WLJIzc31pofw9ixijWEgxlw32c")
