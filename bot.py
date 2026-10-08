# bot.py — بۆتی دیسکۆرد بە AI
import os, discord
from discord.ext import commands
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")

client = Groq(api_key=GROQ_KEY)
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

def ask_ai(history):
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system",
                   "content": "تۆ یاریدەدەرێکی زیرەکی بۆتی دیسکۆردی. بە کوردی وەڵام بدەوە، کورت و ڕوون."}] + history,
    )
    return resp.choices[0].message.content

@bot.event
async def on_ready():
    print(f"بۆت چالاکە: {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # تەنیا کاتێک وەڵام بدەوە کە ناوی بۆتەکە هاتووە یان لە کەنالێکی AI ـیە
    if bot.user in message.mentions or message.channel.name == "ai":
        async with message.channel.typing():
            history = [
                {"role": "user", "content": m.content}
                for m in reversed([x async for x in message.channel.history(limit=6)])
                if not m.author.bot
            ][::-1]
            try:
                answer = ask_ai(history)
                await message.reply(answer[:2000])  # دیسکۆرد ٢٠٠٠ نووسە سنوورە
            except Exception as e:
                await message.reply(f"هەڵەیەک ڕوویدا: {e}")

bot.run(DISCORD_TOKEN)
