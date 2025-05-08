import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from pydub import AudioSegment
import speech_recognition as sr

TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN)    
dp = Dispatcher()

@dp.message(Command('start'))
async def start(message: Message):
    await message.answer(
        "Привіт! Цей бот може:\n"
        "🔹 /voice_interpreter - перетворювати голосові повідомлення в текст\n"
        "🔹 /echo - повторювати ваші текстові повідомлення\n\n"
        "Оберіть потрібну функцію!"
    )

@dp.message(Command('voice_interpreter'))
async def voice_interpreter_mode(message: Message):
    await message.answer(
        "🔊 Режим голосового інтерпретатора увімкнено!\n"
        "Просто надішліть мені голосове повідомлення, і я перетворю його в текст."
    )

@dp.message(Command('echo'))
async def echo_mode(message: Message):
    await message.answer(
        "🔄 Режим ехо увімкнено!\n"
        "Тепер я буду повторювати всі ваші текстові повідомлення."
    )

@dp.message(lambda message: message.voice)
async def handle_voice(message: Message):
    file_info = await bot.get_file(message.voice.file_id)
    file_path = file_info.file_path
    downloaded_file = await bot.download_file(file_path)

    ogg_file = f"voice_{message.from_user.id}.ogg"
    wav_file = f"voice_{message.from_user.id}.wav"

    with open(ogg_file, 'wb') as f:
        f.write(downloaded_file.read())

    AudioSegment.from_file(ogg_file).export(wav_file, format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="uk-UA")
        await message.answer(f"📝 Розпізнаний текст:\n{text}")
    except sr.UnknownValueError:
        await message.answer("Не вдалося розпізнати голос.")
    except sr.RequestError as e:
        await message.answer(f"Помилка сервера: {e}")

    os.remove(ogg_file)
    os.remove(wav_file)

@dp.message(lambda message: message.text and not message.text.startswith('/'))
async def echo_message(message: Message):
    await message.answer(f"🔁 Ви сказали: {message.text}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())