import random
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# Хранилище данных пользователей (в продакшене используй базу данных)
user_data = {}

def get_user_data(user_id):
    if user_id not in user_data:
        user_data[user_id] = {
            'min_num': 1,
            'max_num': 100,
            'excluded_numbers': set(),
            'used_numbers': set(),
            'history': []
        }
    return user_data[user_id]

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎲 Случайное число"), KeyboardButton(text="⚙️ Настройки")],
            [KeyboardButton(text="📊 История"), KeyboardButton(text="🔄 Сброс")]
        ],
        resize_keyboard=True
    )

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🎲 <b>Добро пожаловать в Рандомайзер чисел!</b>\n\n"
        "Используйте кнопки ниже для управления:",
        reply_markup=get_main_keyboard(),
        parse_mode="HTML"
    )

@router.message(F.text == "🎲 Случайное число")
async def generate_number(message: types.Message):
    user_info = get_user_data(message.from_user.id)
    
    min_num = user_info['min_num']
    max_num = user_info['max_num']
    excluded = user_info['excluded_numbers']
    used = user_info['used_numbers']
    
    # Генерация числа
    all_numbers = set(range(min_num, max_num + 1))
    available_numbers = all_numbers - excluded - used
    
    if not available_numbers:
        user_info['used_numbers'] = set()
        available_numbers = all_numbers - excluded
        await message.answer("🔄 <b>Все числа использованы! История сброшена.</b>", parse_mode="HTML")
    
    if not available_numbers:
        await message.answer("❌ <b>Нет доступных чисел!</b>", parse_mode="HTML")
        return
    
    random_number = random.choice(list(available_numbers))
    user_info['used_numbers'].add(random_number)
    user_info['history'].append(random_number)
    
    response = f"🎲 <b>Случайное число:</b> {random_number}\n\n"
    response += f"📊 <b>Диапазон:</b> {min_num}-{max_num}\n"
    
    if excluded:
        response += f"🚫 <b>Исключено:</b> {sorted(excluded)}\n"
    
    response += f"📋 <b>Осталось чисел:</b> {len(available_numbers) - 1}"
    
    await message.answer(response, parse_mode="HTML")

# ... остальные хендлеры из предыдущего кода