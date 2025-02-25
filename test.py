import main
import time
import random
import string
from gtts import gTTS
from deep_translator import GoogleTranslator

def generate_random_text(length):
    return ''.join(random.choices(string.ascii_letters + "", k=length))

def measure_execution_time(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return end_time - start_time, result

def test_tts():
    text_sizes = [10, 50, 100, 500, 1000]
    for size in text_sizes:
        text = generate_random_text(size)
        exec_time, _ = measure_execution_time(gTTS, text, lang='ru')
        print(f"TTS ({size} символов): {exec_time:.5f} секунд")

def test_translation():
    text_sizes = [10, 50, 100, 500, 1000]
    translator = GoogleTranslator(sourse='auto', target='en')

    for size in text_sizes:
        text = generate_random_text(size)
        exec_time, translated_text = measure_execution_time(translator.translate, text)
        print(f"Перевод ({size} символов): {exec_time:.5f} секунд")


print('Тестируем TTS...')
test_tts()

print('\n Тестируем перевод...')
test_translation()