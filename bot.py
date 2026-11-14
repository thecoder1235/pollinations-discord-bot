import os
import discord
from discord.ext import commands
from discord import app_commands
from config import TOKEN
from main import ImgAPI
from styles import STYLES

IMAGE_PATH = "generated_image.jpg"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Giriş yapıldı: {bot.user}')


async def style_autocomplete(interaction: discord.Interaction, current: str):
    return [
        app_commands.Choice(name=key, value=key)
        for key in STYLES
        if current.lower() in key.lower()
    ][:25]


@bot.hybrid_command(name="start", description="Botun açıklamasını gösterir.")
async def start(ctx):
    description = (
        "Bu bot sayesinde stiller seçerek AI ile oluşturulmuş resimler oluşturabilirsin!\n"
        "Mevcut stiller:\n"
    )
    for style in STYLES:
        description += f"- {style}\n"
    description += "\nBir resim oluşturmak için aşağıdaki komutu kullanabilirsiniz:\n"
    description += "`!create_img <stil> <prompt>` veya `/create_img`\n"
    description += "Örnek: `!create_img anime Bir kedi uzayda`"
    await ctx.send(description)


@bot.hybrid_command(name="create_img", description="Seçtiğin stilde AI resmi oluşturur.")
@app_commands.describe(style="Resim stili", prompt="Resmin açıklaması")
@app_commands.autocomplete(style=style_autocomplete)
async def create_img(ctx, style: str, *, prompt: str):
    if style not in STYLES:
        await ctx.send("Girdiğiniz stil geçersiz, lütfen geçerli bir stil seçin:\n" + ", ".join(STYLES.keys()))
        return

    full_prompt = f"{prompt}, {STYLES[style]}"
    print("Gönderilen prompt:", full_prompt)

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="🎵 şarkı söylüyor"))
    sing_msg = await ctx.send("🎤 La la la~ resmini çiziyorum... 🎶🎵")

    try:
        api = ImgAPI()
        api.download_image(full_prompt)
        await ctx.send(file=discord.File(IMAGE_PATH))
    finally:
        try:
            await sing_msg.delete()
        except discord.HTTPException:
            pass
        await bot.change_presence(activity=None)
        if os.path.exists(IMAGE_PATH):
            os.remove(IMAGE_PATH)


bot.run(TOKEN)