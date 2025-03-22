import time
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

"""
Это учебный скрипт, является реализацией ЧАСТИ третьего сценария и служит для понимания как всё работает
"""

download_directory = os.path.abspath("downloads")  # папка, куда будет скачиваться файл
os.makedirs(download_directory, exist_ok=True)
file_name = "sbisplugin-setup-web.exe"
file_path = os.path.join(download_directory, file_name)

print(f"Директория: {download_directory}")
print(f"Путь к файлу: {file_path}")

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_directory,
    "download.prompt_for_download": False,  # отключить запрос перед скачиванием
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# запуск
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    driver.get("https://sbis.ru/download?tab=plugin")

    download_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Скачать')]"))
    )
    download_link_text = download_button.text.strip()
    print(f"Текст ссылки: {download_link_text}")

    match = re.search(r'(\d+\.\d+)\s*МБ', download_link_text)
    if match:
        expected_file_size_mb = float(match.group(1))
        print(f"Ожидаемый размер файла: {expected_file_size_mb} МБ")
    else:
        expected_file_size_mb = None
        print("Не удалось извлечь размер файла.")

    print("Скачивание файла...")
    download_button.click()
    time.sleep(10)  # ждём скачивания (может не успеть скачать, но для теста норм, с моим инетом хватает)



    # Дальше идут проверки
    # Скачан ли файл и соответствует ли размер ожидаемому

    files = os.listdir(download_directory)
    if files:
        print(f"Файл успешно скачан: {files[0]}")
    else:
        print("Файл не найден в папке загрузок.")


    if os.path.exists(download_directory):
        print(f"Файл найден: {file_path}")
        actual_size = os.path.getsize(file_path)
        expected_size = 10.43 * 1024 * 1024  # перевод в байты

        if abs(actual_size - expected_size) < 1024 * 10:  # погрешность 10 кб
            print("Размер файла совпадает с ожидаемым.")
        else:
            print(f"Ожидаемый размер: {expected_size} байт, фактический: {actual_size} байт.")

        # Посмотрели и хватит
        os.remove(file_path)
        print("Файл удалён.")

    else:
        print("Файл не найден.")


finally:
    driver.quit()


