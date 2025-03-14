import discord
from discord.ext import commands
from config import TOKEN
from commands import setup_commands
from voice_chat_reader import VoiceChatReader  # テキスト読み上げ機能
from time_signal import TimeSignal  # 時報機能
import voice_state_announce  # 入退出読み上げ機能

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.voice_chat_reader = VoiceChatReader(self, speed=1.0)
        self.time_signal = None

    async def setup_hook(self):
        await setup_commands(self)
        print("全コマンドを追加しました")

        await self.tree.sync()
        print("スラッシュコマンドを同期しました")

        self.time_signal = TimeSignal(self)

bot = MyBot()

voice_state_announce.setup(bot)

@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user}")

@bot.event
async def on_message(message):
    await bot.voice_chat_reader.on_message(message)

bot.run(TOKEN)
