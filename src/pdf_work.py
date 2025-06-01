# Импортируем необходимые модули из PyPDF2
from PyPDF2 import PdfReader
import re

# Указываем путь к PDF-файлу
pdf_path = r"C:\Users\Admin\Downloads\Documents\ob-7350-21.pdf"

# Открываем PDF-файл для чтения
with open(pdf_path, "rb") as file:
    # Создаем объект для чтения PDF
    reader = PdfReader(file)
    
    # Получаем количество страниц в PDF
    num_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()
    pattern = r'НИЕ : (.*?)\n'
    update = re.findall(pattern, text)[0]
    print(update)
