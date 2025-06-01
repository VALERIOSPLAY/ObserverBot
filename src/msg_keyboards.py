import logging
import sqlite3
from aiogram import Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
from db_conn import execute_query


def md_answer(filepath):
    with open(filepath, 'rt', encoding='utf-8') as f:
        return f.read()


# Функции для создания inline клавиатур
def create_start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Профиль 🫂', callback_data='profile'),
        InlineKeyboardButton(text='Расписание 📆', callback_data='schedule'),
        InlineKeyboardButton(text='Поддержка 🆘', callback_data='support'),
        InlineKeyboardButton(text='FAQ 🎓', callback_data='faq', )
        , width=1
    )
    return builder.as_markup()


def create_profile_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Назад', callback_data='back_to_start'))
    return builder.as_markup()


def create_pay_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Observer на месяц - NaN₽', callback_data='pay_subscription'),
        InlineKeyboardButton(text='Назад', callback_data='back_to_start')
        , width=1
    )
    return builder.as_markup()


def pay_subscription_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Оплатить', callback_data='pay_subscription'),
        InlineKeyboardButton(text='Назад', callback_data='back_to_start')
        , width=1
    )
    return builder.as_markup()


def create_back_to_start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Назад', callback_data='back_to_start'))
    return builder.as_markup()


def create_support_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Назад', callback_data='back_to_start'))
    return builder.as_markup()


def create_schedule_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Настроить расписание', callback_data='select_faculty'),
        InlineKeyboardButton(text='Назад', callback_data='back_to_start')
        , width=1
    )
    return builder.as_markup()


def schedule_data_sender():
    pass


def select_faculty():
    execute_query("SELECT DISTINCT Faculty FROM Schedules")
    faculties = execute_query("SELECT DISTINCT Faculty FROM Schedules")
    builder = InlineKeyboardBuilder()
    for faculty in faculties:
        builder.row(InlineKeyboardButton(text=faculty[0], callback_data=f'select_course:{faculty}'))
    builder.row(InlineKeyboardButton(text='Назад', callback_data='back_to_start'))
    return builder.as_markup()


def select_course(faculty):
    courses = execute_query("SELECT DISTINCT Course FROM Schedules WHERE Faculty = ?", (faculty,))
    builder = InlineKeyboardBuilder()
    for course in courses:
        builder.row(InlineKeyboardButton(text=course[0], callback_data=f'select_group:{faculty}:{course}'))
    builder.row(InlineKeyboardButton(text='Назад', callback_data='select_faculty'))
    return builder.as_markup()


def select_group(faculty, course):
    groups = execute_query("SELECT DISTINCT group_name FROM Schedules WHERE faculty = ? AND course = ?", (faculty, course))
    builder = InlineKeyboardBuilder()
    for group in groups:
        builder.row(InlineKeyboardButton(text=group[0], callback_data=f'confirm_schedule_change:{faculty}:{course}:{group}'))
    builder.row(InlineKeyboardButton(text='Назад', callback_data=f'select_faculty'))
    return builder.as_markup()


def confirm_schedule_change(faculty, course, group):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Подтвердить', callback_data=f'set_schedule:{faculty}:{course}:{group}'))
    builder.row(InlineKeyboardButton(text='Назад', callback_data='back_to_start'))
    return builder.as_markup()


# Функция для установки расписания
def set_schedule_for_user(username, faculty, course, group):
    schedule = execute_query("SELECT Schedule_ID FROM Schedules WHERE Faculty = ? AND Course = ? AND Group_Name = ?",
                   (faculty, course, group))[0]

    if schedule:
        schedule_id = schedule[0]
        execute_query("UPDATE Students SET Schedule_ID = ?, Schedule_Last_Updated = ? WHERE Username = ?",
                      (schedule_id, datetime.now(), username))

