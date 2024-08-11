import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import concurrent.futures

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def process_page(image, page_number):
    # Конвертация изображения в текст(используется только русский, 
    # но можно скомбинировать русский и английский по желанию)
    text = pytesseract.image_to_string(image, lang='rus')
    print(f'Обработана страница {page_number}')
    return page_number, text

def pdf_to_text(pdf_path, output_txt_path):
    # Конвертация PDF в список изображений с указанием пути к poppler
    images = convert_from_path(pdf_path, poppler_path=r'C:\Program Files\poppler-24.02.0\Library\bin')

    results = []
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Запуск обработки страниц параллельно(хоть какая-то оптимизация этого унылого процесса)
        futures = [executor.submit(process_page, image, i+1) for i, image in enumerate(images)]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    # Сортировка результатов по номерам страниц
    results.sort(key=lambda x: x[0])

    # Запись извлеченного текста в файл
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        for _, text in results:
            f.write(text + '\n')
        
    print(f'Текст сохранен в {output_txt_path}')

pdf_path = 'myPdf.pdf'
output_txt_path = 'readyToBeReaden.txt'

pdf_to_text(pdf_path, output_txt_path)