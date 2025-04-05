# main.py — Telegram бот для обліку змін
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime

API_TOKEN = '6588073582:AAE1HeohTQM-ran14BzGZWlSOe662duklvw'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

conn = sqlite3.connect('workers.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id INTEGER,
    name TEXT,
    role TEXT CHECK(role IN ('worker', 'foreman', 'driver', 'manager')),
    hourly_rate REAL,
    driving_rate REAL DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS shifts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date TEXT,
    start_time TEXT,
    end_time TEXT,
    driving_hours REAL DEFAULT 0,
    bonus_hour INTEGER DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

conn.commit()

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(KeyboardButton('➕ Додати зміну'), KeyboardButton('📊 Звіт'))

class ShiftForm(StatesGroup):
    choosing_user = State()
    choosing_date = State()
    entering_start = State()
    entering_end = State()
    entering_driving = State()
    confirm_bonus = State()
    confirm_save = State()

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("Вітаю! Оберіть дію:", reply_markup=main_kb)

# Додаткові функції ... (скорочено для читабельності, можна буде додати повністю)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
