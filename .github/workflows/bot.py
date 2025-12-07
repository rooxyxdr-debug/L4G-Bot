import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")  # Render'da ayarlayacağın Environment Variable

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)

AUTHORIZED_ROLE = "Special"  # Yetkili rolün adı

@bot.event
async def on_ready():
    print(f"Bot aktif: {bot.user}")

@bot.command()
async def search(ctx, *, keyword: str):
    if isinstance(ctx.channel, discord.DMChannel):
        return

    if not any(role.name == AUTHORIZED_ROLE for role in ctx.author.roles):
        await ctx.send("Bu komutu kullanmaya yetkin yok!")
        return

    try:
        with open("data.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        await ctx.send("⚠️ data.txt bulunamadı!")
        return

    results = [line.strip() for line in lines if keyword.lower() in line.lower()]

    if not results:
        await ctx.send("Sonuç bulunamadı.")
        return

    txt = "\n".join(results)

    # Sonuçları kullanıc
