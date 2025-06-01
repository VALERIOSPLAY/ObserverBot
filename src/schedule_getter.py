import requests
import fitz  # PyMuPDF
from PIL import Image
import io
import os

def download_and_convert_pdf(url, output_dir):

    response = requests.get(url, verify=False)
    if response.status_code != 200:
        raise Exception(f"Failed to download PDF: {response.status_code}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_document = fitz.open(stream=response.content, filetype="pdf")

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)  # Загружаем страницу
        pix = page.get_pixmap()  # Получаем изображение страницы
        image = Image.open(io.BytesIO(pix.tobytes()))
        output_path = os.path.join(output_dir, f"page_{page_number + 1}.png")
        image.save(output_path, format="PNG")

    pdf_document.close()

# Пример использования функции
download_and_convert_pdf("https://opi-emit.ru/api/schedule/ob-7350-23", "schedules")