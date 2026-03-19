import asyncio
import os
import re
from typing import Any

import httpx
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton


# =========================
# НАСТРОЙКИ
# =========================
def получить_токен() -> str:
    if os.path.exists('.env'):
        with open('.env', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.startswith('BOT_TOKEN='):
                    return line.split('=', 1)[1].strip()
    raise ValueError('В файле .env не найден BOT_TOKEN')


BOT_TOKEN = получить_токен()
API_BASE_URL = 'http://127.0.0.1:8000'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# =========================
# КНОПКИ MVP
# =========================
клавиатура = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🔎 Найти кандидатов')],
        [KeyboardButton(text='ℹ️ Помощь')],
    ],
    resize_keyboard=True,
    input_field_placeholder='Напиши вакансию, например: Нужен продавец в Орле 2/2 зарплата 45000'
)


# =========================
# ПАРСИНГ ВАКАНСИИ
# =========================
def извлечь_город(текст: str) -> str:
    текст_н = текст.lower()

    if 'орёл' in текст_н or 'орел' in текст_н:
        return 'Орёл'
    if 'москва' in текст_н:
        return 'Москва'
    if 'казань' in текст_н:
        return 'Казань'
    if 'спб' in текст_н or 'санкт-петербург' in текст_н:
        return 'Санкт-Петербург'

    return 'Орёл'


def извлечь_профессию(текст: str) -> tuple[str, str]:
    текст_н = текст.lower()

    if 'продав' in текст_н:
        return 'Продавец', 'sales'
    if 'кассир' in текст_н:
        return 'Кассир', 'sales'
    if 'менеджер' in текст_н:
        return 'Менеджер', 'management'
    if 'оператор' in текст_н:
        return 'Оператор', 'operations'

    return 'Сотрудник', 'other'


def извлечь_зарплату(текст: str) -> tuple[int, int]:
    совпадение = re.search(r'(\d{4,6})', текст.replace(' ', ''))
    if совпадение:
        сумма = int(совпадение.group(1))
        return сумма, сумма + 10000
    return 40000, 50000


def извлечь_график(текст: str) -> str:
    текст_н = текст.lower()
    шаблон = re.search(r'\d\/\d', текст_н)
    if шаблон:
        return шаблон.group(0)
    if 'полный день' in текст_н:
        return '5/2'
    return '2/2'


def извлечь_опыт(текст: str) -> int:
    совпадение = re.search(r'опыт\s*(\d+)', текст.lower())
    if совпадение:
        return int(совпадение.group(1))
    return 1


def разобрать_вакансию_из_текста(текст: str) -> dict[str, Any]:
    профессия, категория = извлечь_профессию(текст)
    город = извлечь_город(текст)
    зарплата_min, зарплата_max = извлечь_зарплату(текст)
    график = извлечь_график(текст)
    опыт = извлечь_опыт(текст)

    return {
        'employer_id': 1,
        'title': профессия,
        'category': категория,
        'city': город,
        'experience_min': опыт,
        'schedule': график,
        'salary_min': зарплата_min,
        'salary_max': зарплата_max,
        'employment_type': 'full_time',
        'description': текст,
    }


# =========================
# API
# =========================
async def создать_вакансию(данные: dict[str, Any]) -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=20.0) as client:
        ответ = await client.post(f'{API_BASE_URL}/vacancies/', json=данные)
        ответ.raise_for_status()
        return ответ.json()


async def получить_подбор(vacancy_id: int) -> list[dict[str, Any]]:
    async with httpx.AsyncClient(timeout=20.0) as client:
        ответ = await client.get(f'{API_BASE_URL}/match/{vacancy_id}')
        ответ.raise_for_status()
        return ответ.json()


async def получить_кандидатов() -> list[dict[str, Any]]:
    async with httpx.AsyncClient(timeout=20.0) as client:
        ответ = await client.get(f'{API_BASE_URL}/candidates/')
        ответ.raise_for_status()
        return ответ.json()


# =========================
# ФОРМАТ ОТВЕТА
# =========================
def сформировать_ответ(совпадения: list[dict[str, Any]], кандидаты: list[dict[str, Any]]) -> str:
    if not совпадения:
        return 'Кандидаты не найдены.'

    карта_кандидатов = {кандидат['id']: кандидат for кандидат in кандидаты}
    строки = ['Найдены кандидаты:']

    for номер, совпадение in enumerate(совпадения[:5], start=1):
        кандидат = карта_кандидатов.get(совпадение['candidate_id'], {})

        имя = кандидат.get('full_name', 'Без имени')
        телефон = кандидат.get('phone', 'Нет телефона')
        профессия = кандидат.get('profession', 'Не указана')
        опыт = кандидат.get('experience_years', '-')
        город = кандидат.get('city', 'Не указан')
        score = совпадение.get('score', 0)

        строки.append(
            f'\n{номер}. {имя}\n'
            f'Профессия: {профессия}\n'
            f'Город: {город}\n'
            f'Опыт: {опыт} лет\n'
            f'Телефон: {телефон}\n'
            f'Совпадение: {score}%'
        )

    return '\n'.join(строки)


# =========================
# КОМАНДЫ
# =========================
@dp.message(CommandStart())
async def команда_старт(message: Message):
    await message.answer(
        'HR-бот запущен.\n\n'
        'Напиши вакансию текстом.\n\n'
        'Пример:\n'
        'Нужен продавец в Орле 2/2 зарплата 45000',
        reply_markup=клавиатура
    )


# =========================
# ОСНОВНАЯ ЛОГИКА MVP
# =========================
@dp.message()
async def обработать_сообщение(message: Message):
    текст = (message.text or '').strip()
    текст_н = текст.lower()

    if not текст:
        await message.answer('Напиши вакансию текстом.', reply_markup=клавиатура)
        return

    if текст_н in ('ℹ️ помощь', 'помощь'):
        await message.answer(
            'Напиши вакансию в свободной форме.\n\n'
            'Пример:\n'
            'Нужен продавец в Орле 2/2 зарплата 45000',
            reply_markup=клавиатура
        )
        return

    if текст_н == '🔎 найти кандидатов':
        текст = 'Нужен продавец в Орле 2/2 зарплата 45000'
        текст_н = текст.lower()

    if 'нужен' not in текст_н and 'требуется' not in текст_н and 'вакансия' not in текст_н:
        await message.answer(
            'Напиши вакансию так:\n\n'
            'Нужен продавец в Орле 2/2 зарплата 45000',
            reply_markup=клавиатура
        )
        return

    await message.answer('Понял вакансию. Создаю...')

    данные_вакансии = разобрать_вакансию_из_текста(текст)
    вакансия = await создать_вакансию(данные_вакансии)

    await message.answer(
        'Вакансия создана:\n'
        f"Профессия: {данные_вакансии['title']}\n"
        f"Город: {данные_вакансии['city']}\n"
        f"График: {данные_вакансии['schedule']}\n"
        f"Зарплата: {данные_вакансии['salary_min']} - {данные_вакансии['salary_max']}"
    )

    await message.answer('Ищу подходящих кандидатов...')

    совпадения = await получить_подбор(вакансия['id'])
    кандидаты = await получить_кандидатов()
    ответ = сформировать_ответ(совпадения, кандидаты)

    await message.answer(ответ, reply_markup=клавиатура)


# =========================
# ЗАПУСК
# =========================
async def main():
    print('Бот запущен')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
