import asyncio
import edge_tts

VOICE = "th-TH-PremwadeeNeural"
OUTPUT_FILE = "output.mp3"


async def generate_audio(TEXT):
    communicate = edge_tts.Communicate(TEXT, VOICE,pitch='+35Hz')
    await communicate.save(OUTPUT_FILE)


asyncio.run(generate_audio("สวัสดีค่ะ! ยินดีต้อนรับสู่โรงพยาบาลบูรพาค่ะ มีอะไรให้ช่วยเหลือหรือบริการคุณได้บ้างคะ"))