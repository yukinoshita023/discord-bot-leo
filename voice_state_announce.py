import discord
import os
import asyncio
import subprocess

VOICE_TMP_DIR = "voice_tmp"
EDGE_TTS_PATH = "edge-tts"  # edge-tts が PATH に通ってる前提

if not os.path.exists(VOICE_TMP_DIR):
    os.makedirs(VOICE_TMP_DIR)

async def play_tts(bot, vc, text, speed=1.0):
    # speed=1.0 → rate="+0%", 2.0 → rate="+100%", 0.8 → rate="-20%"
    rate_percent = int((speed - 1.0) * 100)
    rate_option = f"{rate_percent:+d}%"  # +20%, -10% みたいにする

    filename = os.path.join(VOICE_TMP_DIR, "vc_announce.mp3")

    # edge-tts 実行（音声生成）
    command = [
        EDGE_TTS_PATH,
        "--text", text,
        "--write-media", filename,
        "--voice", "ja-JP-KeitaNeural",
        "--rate", rate_option,
    ]

    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    source = discord.FFmpegPCMAudio(filename)

    async def cleanup():
        await asyncio.sleep(1)
        if os.path.exists(filename):
            os.remove(filename)

    await bot.audio_queue.enqueue(vc, source)
    asyncio.create_task(cleanup())