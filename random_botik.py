import os
import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Безопасное получение токена из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN', '8482953132:AAEk0ld9oNYGEslG7lD_zTwbLbfJddAFzpk')

if not BOT_TOKEN:
    logger.error("Не установлен BOT_TOKEN!")
    exit(1)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ========== ВСЯ ОСТАЛЬНАЯ ЧАСТЬ КОДА ОСТАЕТСЯ БЕЗ ИЗМЕНЕНИЙ ==========

# Состояния для FSM
class RandomStates(StatesGroup):
    waiting_for_min = State()
    waiting_for_max = State()
    waiting_for_exclude = State()

# Хранилище данных пользователей
user_data = {}

def get_user_data(user_id):
    """Получаем или создаем данные пользователя"""
    if user_id not in user_data:
        user_data[user_id] = {
            'min_num': 1,
            'max_num': 100,
            'excluded_numbers': set(),
            'used_numbers': set(),
            'history': []
        }
    return user_data[user_id]

# Клавиатура главного меню
def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎲 Случайное число"), KeyboardButton(text="⚙️ Настройки")],
            [KeyboardButton(text="📊 История"), KeyboardButton(text="🔄 Сбросить")]
        ],
        resize_keyboard=True
    )

# ... и весь остальной ваш код остается точно таким же ...