# scheduler.py
import logging
import multiprocessing
import sqlite3
import requests
import time
from aiogram import Bot
from datetime import datetime
from io import BytesIO
from db_conn import execute_query
from PyPDF2 import PdfReader
import re
import fitz
from PIL import Image
import io
import os
import asyncio
from aiogram.types import FSInputFile



# Функция для конвертации PDF в изображения (предположим, она готова)
def download_and_convert_pdf(response):
    try:
        print('Converting images')
        global output_dir
        output_dir = r"\bot_data\converted_images"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        pdf_document = fitz.open(stream=response.content, filetype="pdf")
        images = []
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)  # Загружаем страницу
            pix = page.get_pixmap()  # Получаем изображение страницы
            image = Image.open(io.BytesIO(pix.tobytes()))
            output_path = os.path.join(output_dir, f"page_{page_number + 1}.png")
            image.save(output_path, format="PNG")

        pdf_document.close()
        
        for i in os.listdir(output_dir):
            images.append(os.path.join(output_dir, i))
        return images
    except Exception as e:
        print("In download_and_convert_pdf: Can't convert pdf", e)

# Установка параметров логирования
logging.basicConfig(level=logging.INFO)



# Функция для обработки расписаний
async def process_students(bot: Bot):
    logging.info("Updating student schedules")
    # Запрашиваем все записи из таблицы Students
    students = execute_query(("SELECT Schedule_ID, Username, Schedule_Last_Updated, Chat_ID FROM Students"))

    for schedule_id, username, student_last_updated_str, chat_id in students:
        try:
            # Получаем расписание из таблицы Schedules по Schedule_ID
            schedule_url = execute_query("SELECT Schedule_URL FROM Schedules WHERE Schedule_ID = ?", (schedule_id,))[0][0]
            
            response = requests.get(schedule_url, verify=False)
            pdf_content = BytesIO(response.content)
            reader = PdfReader(pdf_content)
            update = ''
            page = reader.pages[0]
            text = page.extract_text()
            try:
                pattern = r'НИЕ : (.*?)\n'
                update = re.findall(pattern, text)[0]
            except Exception as e:
                logging.error(f'Exception in getting update date: {e}')
                update = "Нет информации о дате обновления"
                
            # Если версия расписания у пользователя устарела
            if student_last_updated_str != update:
                images = download_and_convert_pdf(response)

                # Отправляем изображения пользователю
                for image in images:
                    print(image)
                    await bot.send_photo(chat_id=chat_id, photo=FSInputFile(image))


                # Обновляем дату последнего обновления расписания для пользователя
                execute_query("UPDATE Students SET Schedule_Last_Updated = ? WHERE Username = ?", (update, username))

        except Exception as e:
            logging.error(f"Произошла ошибка: {e}")


async def process_students(bot: Bot):
    logging.info("Updating student schedules")
    # Запрашиваем все записи из таблицы Students
    students = execute_query(("SELECT Schedule_ID, Username, Schedule_Last_Updated, Chat_ID FROM Students"))

    for schedule_id, username, student_last_updated_str, chat_id in students:
        try:
            # Получаем расписание из таблицы Schedules по Schedule_ID
            schedule_url = execute_query("SELECT Schedule_URL FROM Schedules WHERE Schedule_ID = ?", (schedule_id,))[0][0]
            
            response = requests.get(schedule_url, verify=False)
            pdf_content = BytesIO(response.content)
            reader = PdfReader(pdf_content)
            update = ''
            page = reader.pages[0]
            text = page.extract_text()
            try:
                pattern = r'НИЕ : (.*?)\n'
                update = re.findall(pattern, text)[0]
            except Exception as e:
                logging.error(f'Exception in getting update date: {e}')
                update = "Нет информации о дате обновления"
                
            # Если версия расписания у пользователя устарела
            if student_last_updated_str != update:
                images = download_and_convert_pdf(response)

                # Отправляем изображения пользователю
                for image in images:
                    print(image)
                    await bot.send_photo(chat_id=chat_id, photo=FSInputFile(image))


                # Обновляем дату последнего обновления расписания для пользователя
                execute_query("UPDATE Students SET Schedule_Last_Updated = ? WHERE Username = ?", (update, username))

        except Exception as e:
            logging.error(f"Произошла ошибка: {e}")

async def process_students(bot: Bot):
    logging.info("Updating student schedules")
    # Запрашиваем все записи из таблицы Students
    students = execute_query(("SELECT Schedule_ID, Username, Schedule_Last_Updated, Chat_ID FROM Students"))

    for schedule_id, username, student_last_updated_str, chat_id in students:
        try:
            # Получаем расписание из таблицы Schedules по Schedule_ID
            schedule_url = execute_query("SELECT Schedule_URL FROM Schedules WHERE Schedule_ID = ?", (schedule_id,))[0][0]
            
            response = requests.get(schedule_url, verify=False)
            pdf_content = BytesIO(response.content)
            reader = PdfReader(pdf_content)
            update = ''
            page = reader.pages[0]
            text = page.extract_text()
            try:
                pattern = r'НИЕ : (.*?)\n'
                update = re.findall(pattern, text)[0]
            except Exception as e:
                logging.error(f'Exception in getting update date: {e}')
                update = "Нет информации о дате обновления"
                
            # Если версия расписания у пользователя устарела
            if student_last_updated_str != update:
                images = download_and_convert_pdf(response)

                # Отправляем изображения пользователю
                for image in images:
                    print(image)
                    await bot.send_photo(chat_id=chat_id, photo=FSInputFile(image))


                # Обновляем дату последнего обновления расписания для пользователя
                execute_query("UPDATE Students SET Schedule_Last_Updated = ? WHERE Username = ?", (update, username))

        except Exception as e:
            logging.error(f"Произошла ошибка: {e}")


async def lazy_process_students(bot: Bot):
    logging.info("Updating student schedules")
    # Запрашиваем все записи из таблицы Students
    students = execute_query(("SELECT Schedule_ID, Username, Schedule_Last_Updated, Chat_ID FROM Students"))

    for schedule_id, username, student_last_updated_str, chat_id in students:
        try:
            # Получаем расписание из таблицы Schedules по Schedule_ID
            schedule_url = execute_query("SELECT Schedule_URL FROM Schedules WHERE Schedule_ID = ?", (schedule_id,))[0][0]
            
            response = requests.get(schedule_url, verify=False)
            pdf_content = BytesIO(response.content)
            reader = PdfReader(pdf_content)
            update = ''
            page = reader.pages[0]
            text = page.extract_text()
            try:
                pattern = r'НИЕ : (.*?)\n'
                update = re.findall(pattern, text)[0]
            except Exception as e:
                logging.error(f'Exception in getting update date: {e}')
                update = "Нет данных о дате обновления"
                
            # Если версия расписания у пользователя устарела
            if student_last_updated_str != update:
                images = download_and_convert_pdf(response)

                # Отправляем изображения пользователю
                for image in images:
                    print(image)
                    await bot.send_photo(chat_id=chat_id, photo=FSInputFile(image))
                await bot.send_message(chat_id=chat_id, text=f"Новое расписание. Обновлено: {update}")


                # Обновляем дату последнего обновления расписания для пользователя
                execute_query("UPDATE Students SET Schedule_Last_Updated = ? WHERE Username = ?", (update, username))
                execute_query("UPDATE Students SET Schedules_Sent = Schedules_Sent + 1 WHERE Username = ?", (username,))

        except Exception as e:
            logging.error(f"Произошла ошибка: {e}")


