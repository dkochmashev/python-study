import asyncio
import logging
import sys
from os import getenv, environ

# Использовал API версии 3
from aiogram import Bot, Dispatcher, F, html
from aiogram.types import Message, BotCommand
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
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


dp = Dispatcher(storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()  # height?
    weight = State()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    logging.info('Получен запрос на запуск бота')
    await message.answer("\U0001F929")
    await message.answer(f'Привет, {html.bold(message.from_user.full_name)}! '
                         'Я бот помогающий твоему здоровью.')


@dp.message(F.text.startswith("Calories"))
async def set_age(message: Message, state: FSMContext):
    logging.info(f'Получено сообщение: {message.text}')
    await message.answer('Введите свой возраст:')
    await state.set_state(UserState.age)


@dp.message(StateFilter(UserState.age))
async def set_growth(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await state.set_state(UserState.growth)
    await message.answer('Введите свой рост:')


@dp.message(StateFilter(UserState.growth))
async def set_weight(message: Message, state: FSMContext):
    await state.update_data(growth=float(message.text))
    await state.set_state(UserState.weight)
    await message.answer('Введите свой вес:')


@dp.message(StateFilter(UserState.weight))
async def send_calories(message: Message, state: FSMContext):
    await state.update_data(weight=float(message.text))
    data = await state.get_data()
    # для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;
    result = 10 * data["weight"] + 6.25 * data["growth"] - 5 * data["age"] + 5
    await message.answer(f'Норма калорий для мужчин: {html.bold(result)}')
    # для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.
    result = 10 * data["weight"] + 6.25 * data["growth"] - 5 * data["age"] - 161
    await message.answer(f'Норма калорий для женщин: {html.bold(result)}')
    await state.clear()


async def main():
    bot = Bot(token=get_bot_token(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot, allowed_updates=())


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    try:
        logging.info('Запуск')
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Принудительная остановка бота')
    except:
        logging.error('Ошибка запуска бота', exc_info=True)

    logging.info('Завершение работы')
