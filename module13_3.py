import asyncio
import logging
import sys
from os import getenv, environ

# Использовал API версии 3.13.0
from aiogram import Bot, Dispatcher, html
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties


def get_bot_token():
    ''' Получения token для аутентификации бота.\n
        Token можно указать:\n
        - в переменной окружения BOT_TOKEN
        - в файле, чье имя укзать в переменной окружения BOT_TOKEN_FILE
        - в файле bot_token.txt
    :return: token для аутентификации\n
        или выбрасывает исклчючение RuntimeError
    '''
    if 'BOT_TOKEN' in environ:
        logging.info('Обнаружена переменная окружения BOT_TOKEN')
        return getenv('BOT_TOKEN')

    BOT_TOKEN_FILE = getenv('BOT_TOKEN_FILE') or 'bot_token.txt'

    with open(BOT_TOKEN_FILE, 'r', encoding='utf-8') as bot_token_file:
        logging.info(f'Чтение token из файла {BOT_TOKEN_FILE}')
        return bot_token_file.read().strip('\r\n')

    raise RuntimeError('Отсутствует token для аутентификации бота')


dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    logging.info('Получен запрос на запуск бота')
    await message.answer("\U0001F929")
    await message.answer(f'Привет, {html.bold(message.from_user.full_name)}! '
                         'Я бот помогающий твоему здоровью.')


@dp.message()
async def any_message(message: Message):
    logging.info(f'Получено сообщение: {message.text}')
    await message.answer('Введите команду /start, чтобы начать общение.')


async def main():
    bot = Bot(token=get_bot_token(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        logging.info('Запуск')
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Принудительная остановка бота')
    except:
        logging.error('Ошибка запуска бота', exc_info=True)

    logging.info('Завершение работы')
