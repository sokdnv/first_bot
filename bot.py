# Импорт библиотек
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message  # ловим все обновления этого типа
from aiogram.filters.command import Command  # обрабатываем команды /start, /help и другие

# Инициализация объектов
TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)  # Создаем объект бота
dp = Dispatcher()  # Создаем объект диспетчера. Все хэндлеры(обработчики) должны быть подключены к диспетчеру
# сначала я начал думать над конструкциями типо with open('logs.log, 'a') as file: у каждой записи
# но затем глянул в документацию :)
logging.basicConfig(level=logging.INFO,
                    handlers=[
                        logging.FileHandler('logs.log', mode='a')
                    ])


# Домашнее Задание
# - Включить запись log в файл
# - Бот принимает кириллицу отдаёт латиницу в соответствии с Приказом МИД по транслитерации
# - Бот работает из-под docker контейнера
def transliterate(text):
    transliteration_dict = {
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'ZH',
        'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O',
        'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'KH', 'Ц': 'TS',
        'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH', 'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'YU',
        'Я': 'YA',
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh',
        'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu',
        'я': 'ya'}
    answer = []
    for symbol in text:
        if symbol in transliteration_dict:
            answer.append(transliteration_dict.get(symbol))
        else:
            answer.append(symbol)
    return ''.join(answer)


# Обработка/Хэндлер на команду /start
@dp.message(Command(commands=['start']))
async def proccess_command_start(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = (f'Привет, {user_name}! Я текстовый бот, единственный смысл существования которого - '
            f'превращать кириллицу в латиницу')
    logging.info(f'{user_name} {user_id} запустил бота')
    await bot.send_message(chat_id=user_id, text=text)


# Обработка/Хэндлер на команду /help
@dp.message(Command(commands=['help']))
async def proccess_command_help(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = ('Повторяю, я умею только преобразовывать текст. Пиши кириллицей - получай '
            'латиницу. На этом всё.')
    logging.info(f'{user_name} {user_id} вызвал команду help')
    await bot.send_message(chat_id=user_id, text=text)


# Обработка/Хэндлер на любые сообщения
@dp.message()
async def send_transliteration(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = transliterate(message.text)
    logging.info(f'{user_name} {user_id}: {text}')
    await message.answer(text=text)


# Запуск процесса пуллинга
if __name__ == '__main__':
    dp.run_polling(bot)