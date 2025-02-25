import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher()


class Form(StatesGroup):
    waiting_for_text = State()
    waiting_for_translation = State()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Отправь мне задание и я выполню его.")

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды:\n/start\n/help\n/photo\n/text\n/translate')

@dp.message(F.photo)
async def react_photo(message: Message):
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file_path = file_info.file_path
    file_name = os.path.join('img', f'{photo.file_id}.jpg')

    await bot.download_file(file_path, file_name)
    await message.answer(f'Фото сохранено как {file_name}')

@dp.message(Command('text'))
async def request_text(message: Message, state: FSMContext):
    await message.answer(f'Пожалуйста, введите текст, который вы хотите преобразовать в голосовое сообщение')
    await state.set_state(Form.waiting_for_text)

@dp.message(Form.waiting_for_text)
async def handle_text(message: Message, state: FSMContext):
    text = message.text
    tts = gTTS(text, lang='ru')
    file_path = f'vcm/{message.message_id}.ogg'
    tts.save(file_path)

    audio = FSInputFile(file_path)
    await bot.send_audio(message.chat.id, audio)
    os.remove(file_path)

    await state.clear()

@dp.message(Command('translate'))
async def request_translation_text(message: Message, state: FSMContext):
    await message.answer(f'Пожалуйста, введите текст, который вы хотите перевести на английский язык и преобразовать в голосовое сообщение')
    await state.set_state(Form.waiting_for_translation)

@dp.message(Form.waiting_for_translation)
async def handle_translation(message: Message, state: FSMContext):
    text_to_translate = message.text
    translator = GoogleTranslator(source='auto', target='en')
    translated_text = translator.translate(text_to_translate)

    tts = gTTS(translated_text, lang='en')
    file_path = f'vcm/{message.message_id}.ogg'
    tts.save(file_path)

    audio = FSInputFile(file_path)
    await bot.send_audio(message.chat.id, audio)
    os.remove(file_path)

    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__=="__main__":
    asyncio.run(main())