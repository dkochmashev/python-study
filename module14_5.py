import asyncio
import logging
import sys
from os import getenv, environ

# Использовал API версии 3
from aiogram import Bot, Dispatcher, F, html
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.default import DefaultBotProperties

from crud_functions import Storage


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


storage = Storage()
dp = Dispatcher(storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()  # height?
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    logging.info('Получен запрос на запуск бота')
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Рассчитать"), KeyboardButton(text="Информация")],
            [KeyboardButton(text="Регистрация"), KeyboardButton(text="Купить")]
        ])
    await message.answer("\U0001F929")
    await message.answer(f'Привет, {html.bold(message.from_user.full_name)}! '
                         'Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message(F.text.startswith("Рассчитать"))
async def main_menu(message: Message, state: FSMContext):
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
         InlineKeyboardButton(text='Формулы расчета', callback_data='formulas')]
    ])
    await message.answer(text='Выберите опцию:', reply_markup=ikb)


@dp.message(F.text.startswith("Информация"))
async def show_info(message: Message, state: FSMContext):
    logging.info(f'Получено сообщение: {message.text}')
    await message.answer(
        f'Бот {html.bold('"В здоровом теле, здоровый дух"')}\n'
        f'Версия {html.bold('0.14.5alpha')}'
    )


@dp.message(F.text.startswith("Регистрация"))
async def sign_up(message: Message, state: FSMContext):
    logging.info(f'Получено сообщение: {message.text}')
    await state.set_state(RegistrationState.username)
    await message.answer("Введите имя пользователя (только латинский алфавит):")


@dp.message(StateFilter(RegistrationState.username))
async def set_username(message: Message, state: FSMContext):
    logging.info(f'Получено сообщение: {message.text}')
    username = message.text
    if storage.is_included(username):
        await message.answer("Пользователь существует, введите другое имя:")
        return
    await state.update_data(username=username)
    await state.set_state(RegistrationState.email)
    await message.answer('Введите свой email:')


@dp.message(StateFilter(RegistrationState.email))
async def set_email(message: Message, state: FSMContext):
    logging.info(f'Получено сообщение: {message.text}')
    email = message.text
    if storage.is_included(email=email):
        await message.answer("Такой email уже используется, введите другой:")
        return
    await state.update_data(email=email)
    await state.set_state(RegistrationState.age)
    await message.answer('Введите свой возраст:')


@dp.message(StateFilter(RegistrationState.age))
async def set_age(message: Message, state: FSMContext):
    logging.info(f'Получено сообщение: {message.text}')
    await state.update_data(age=int(message.text))
    data = await state.get_data()
    if storage.add_user(data["username"], data["email"], data["age"]) == -1:
        await message.answer("Ошибка регистрации")
    else:
        await message.answer("Регистрация прошла успешно")
    await state.clear()


@dp.message(F.text.startswith("Купить"))
async def get_buying_list(message: Message, state: FSMContext):
    logging.info(f'Получено сообщение: {message.text}')
    product_buttons = []
    for product in storage.get_all_products():
        await message.answer(
            f'Название: {product["title"]} | '
            f'Описание: {product["description"]} | '
            f'Цена: {product["price"]}'
        )
        await message.answer_photo(photo=product["image"])
        product_buttons.append(InlineKeyboardButton(text=f'{product["title"]}',
                                                    callback_data=f'product_buying:{product["title"]}'))

    await message.answer('Выберите продукт для покупки:',
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[product_buttons]))


@dp.callback_query(F.data.startswith('product_buying:'))
async def send_confirm_message(call: CallbackQuery):
    product_label = call.data.split(':')[1]
    logging.info(f'Получен запрос на покупку продукта "{product_label}"')
    await call.message.answer(text=f'Вы успешно приобрели продукт "{product_label}"!')
    await call.answer()


@dp.callback_query(F.data == 'formulas')
async def get_formulas(call: CallbackQuery):
    logging.info('Получен запрос на показ формул расчета')
    await call.message.answer(text='Вычисляет норму калорий по формулам:\n'
                                   '- для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5\n'
                                   '- для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161'
                              )
    await call.answer()


@dp.callback_query(F.data == 'calories')
async def set_age(call: CallbackQuery, state: FSMContext):
    logging.info('Получен запрос на расчет нормы калорий')
    await call.message.answer('Введите свой возраст:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserState.age)
    await call.answer()


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
    result_male = 10 * data["weight"] + 6.25 * data["growth"] - 5 * data["age"] + 5
    # для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.
    result_female = 10 * data["weight"] + 6.25 * data["growth"] - 5 * data["age"] - 161
    await message.answer(f'Норма калорий для мужчин: {html.bold(result_male)}\n'
                         f'Норма калорий для женщин: {html.bold(result_female)}')
    await state.clear()


@dp.message()
async def show_usage(message: Message, state: FSMContext):
    await message.answer('Напишите /start для запуска')


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
