import os
from pages.sbis_page import SbisPage

"""
Реализация третьего сценария
pytest -s tests/test_scenario_3.py
"""

def test_scenario_3(driver):  # фикстура передается как параметр
    sbis = SbisPage(driver)

    try:
        sbis.open_url("https://sbis.ru/")

        sbis.download_plugin()  # Нажали на "Скачать локальные версии"
        expected_file_size = sbis.get_expected_file_size() * 1024 * 1024 # в байты
        sbis.click_link_by_text("Скачать")

        assert sbis.wait_for_download("downloads", "sbisplugin-setup-web.exe"), "Файл не загружен"

        file_path = os.path.join("downloads", "sbisplugin-setup-web.exe")
        if os.path.exists(file_path):
            actual_size = os.path.getsize(file_path)
            print(f"Фактический размер файла: {actual_size} байт")
            print(f"Ожидаемый размер файла: {expected_file_size} байт")

            assert abs(actual_size - expected_file_size) < 1024 * 10, f"Размеры файлов не совпадают. Ожидаемый: {expected_file_size}, фактический: {actual_size}"

            os.remove(file_path)
            print("Файл удалён.")
        else:
            print("Файл не найден в папке загрузок.")
            assert False, "Файл не найден в папке загрузок."

    finally:
        driver.quit()
