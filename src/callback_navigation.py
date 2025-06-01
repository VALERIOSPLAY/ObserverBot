from aiogram import Router
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher, types, F
from msg_keyboards import *
from datetime import datetime, timedelta
from db_conn import conn, cursor
from db_conn import execute_query
import threading
from schedule_updater import process_students
from pathlib import Path
import json



router_navigation = Router()
cl_bot = None


def add_user_to_db(username, chat_id):
    users = execute_query("SELECT * FROM Students WHERE Username = ?", (username,))
    if len(users) > 0:
        user = users[0]
    else:
        user = None

    
    if user is None:
        subscription_end = datetime.now() + timedelta(days=30)
        execute_query("INSERT INTO Students (Username, Subscription_End, Signup_Date, Chat_Status, Chat_ID) VALUES (?, ?, ?, ?, ?)",
                       (username, subscription_end, datetime.now(), 'active', chat_id))

@router_navigation.callback_query()
async def callback_query_handler(callback_query: types.CallbackQuery):
    print(f"Worker thread: {threading.current_thread().name}")
    command_name = callback_query.data
    username = callback_query.from_user.username
    if command_name == 'profile':
        student = execute_query("SELECT Subscription_End, Schedules_Sent FROM Students WHERE Username = ?", (username,))[0]
        subscription_end = student[0]
        schedules_sent = student[1]

        await callback_query.message.edit_text(
            text=f"Ваш никнейм: [@{username}]\nПодписка: Вечна!\nПолучено расписаний: {schedules_sent}",
            reply_markup=create_profile_keyboard(),
            parse_mode='Markdown'
        )
    elif command_name == 'schedule':
        try:
            schedule = execute_query(
                "SELECT s.Faculty, s.Course, s.Group_Name, s.Schedule_Last_Updated FROM Students st JOIN Schedules s ON st.Schedule_ID = s.Schedule_ID WHERE st.Username = ?",
                (username,))[0]
            faculty = schedule[0]
            course = schedule[1]
            group = schedule[2]
            schedule_last_updated = schedule[3]
        except Exception as e:
            faculty = ''
            course = ''
            group = ''
            schedule_last_updated = ''

        await callback_query.message.edit_text(
            text=f"*Ваше текущее расписание:\n{faculty}, {course} Курс, {group}*\n\n*Последнее обновление: {schedule_last_updated}*",
            reply_markup=create_schedule_keyboard(),
            parse_mode='Markdown'
        )

    elif command_name == 'subscription':
        subscription_end = execute_query("SELECT Subscription_End FROM Students WHERE Username = ?", (username,))[0][0]
        await callback_query.message.edit_text(
            text=f"*Ваша подписка: {subscription_end}*\n Нажми на тариф, чтобы продлить доступ к боту 📆",
            reply_markup=create_pay_keyboard(),
            parse_mode='Markdown'
        )
    elif command_name == 'support':
        await callback_query.message.edit_text(
            text='Контакт поддержки: @THE_VALERIOS\n\n Проверьте FAQ, прежде чем писать! Всем поможем',
            reply_markup=create_support_keyboard(),
            parse_mode='Markdown'
        )
    elif command_name == 'faq':
        await callback_query.message.edit_text(
            text=md_answer('faq.md'),
            reply_markup=create_back_to_start_keyboard(),
            parse_mode='Markdown'
        )
    elif command_name == 'back_to_start':
        with open('src/allowed_users.json', 'r', encoding='utf-8') as f:
            allowed_users = json.load(f)
        if username in allowed_users['users']:
            await callback_query.message.edit_text(
                text=md_answer('start.md'),
                reply_markup=create_start_keyboard(),
                parse_mode='Markdown'
            )
        else:
            await callback_query.message.answer("Вы не имеете доступа к этому боту.")

    elif command_name == 'pay_subscription':
        await callback_query.message.edit_text(
            text="*Стоимость подписки: NaN₽*\nДоступ будет продлен до NaN 🫡\n\nНажмите на кнопку, чтобы оплатить",
            reply_markup=pay_subscription_keyboard(),
            parse_mode='Markdown'
        )
    elif command_name == 'select_faculty':
        await callback_query.message.edit_text(
            text="*Выберите факультет:*",
            reply_markup=select_faculty(),
            parse_mode='Markdown'
        )


    elif command_name.startswith('select_course:'):
        faculty = command_name.split(':')[1][2:-3] # убираем кавычки

        await callback_query.message.edit_text(
            text="*Текущий факультет:* " + faculty + "\n\n*Выберите курс*:",
            reply_markup=select_course(faculty),
            parse_mode='Markdown'
        )

    elif command_name.startswith('select_group:'):
        print(command_name)
        faculty = command_name.split(':')[1]
        course = command_name.split(':')[2][2:-3]
        await callback_query.message.edit_text(
            text="*Текущий факультет:* " + faculty + "\n*Текущий курс:* " + course + "\n\n*Выберите группу:*",
            reply_markup=select_group(faculty, course),
            parse_mode='Markdown'
        )
    elif command_name.startswith('confirm_schedule_change:'):
        faculty = command_name.split(':')[1]
        course = command_name.split(':')[2]
        group = command_name.split(':')[3][2:-3]
        await callback_query.message.edit_text(
            text=f"Проверим расписание, все верно? \n\n*Факультет:* {faculty}\n*Курс:* {course}\n*Группа:* {group}",
            reply_markup=confirm_schedule_change(faculty, course, group),
            parse_mode='Markdown'
        )

    elif command_name.startswith('set_schedule:'):
        faculty = command_name.split(':')[1]
        course = command_name.split(':')[2]
        group = command_name.split(':')[3]

        set_schedule_for_user(username, faculty, course, group)

        await callback_query.message.edit_text(
            text=f"Расписание успешно обновлено!\nСейчас пришлю его... \n\n*Факультет:* {faculty}\n*Курс:* {course}\n*Группа:* {group}",
            parse_mode='Markdown'
        )
        print(f'Before, Type {type(cl_bot)}')
        await process_students(cl_bot)
        await callback_query.message.answer("Ваше расписание обновлено.")
        


@router_navigation.message(CommandStart())
async def start(message: types.Message):
    username = message.from_user.username
    with open('src/allowed_users.json', 'r', encoding='utf-8') as f:
        allowed_users = json.load(f)
    if username in allowed_users['users']:
        add_user_to_db(username, message.chat.id)
        await message.answer(
            text=md_answer('start.md'),
            reply_markup=create_start_keyboard(),
            parse_mode='Markdown'
        )
    else:
        await message.answer("Вы не имеете доступа к этому боту.")


@router_navigation.message(F.text)
async def handle_all_messages(message: types.Message):
    if message.text.startswith("SEND_ALL"):
        users = execute_query("SELECT Username, Chat_ID FROM Students WHERE Chat_Status = 'active'")
        for i in users:
            cl_bot.send_message(i[1], message.text[8:])
    else:
        await message.answer("Неизвестная команда. Используйте /start для начала.")