import time
from selenium import webdriver
from pages.sbis_page import SbisPage
from pages.tensor_page import TensorPage
from selenium.webdriver.support.ui import WebDriverWait

"""
Реализация первого сценария
pytest -s tests/test_scenario_1.py
"""

def test_scenario_1():
    driver = webdriver.Chrome()
    sbis = SbisPage(driver)
    tensor = TensorPage(driver)

    try:
        sbis.open_url("https://sbis.ru/")
        sbis.go_to_contacts()
        sbis.click_tensor_banner()

        # страница открывается в новой вкладке, переключаемся на неё
        WebDriverWait(driver, 20).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])

        tensor.check_power_in_people() # здесь assert внутри (если нет блока "Сила в людях")
        tensor.go_to_about()

        assert driver.current_url == "https://tensor.ru/about", f"Ожидался URL: https://tensor.ru/about, но найден: {driver.current_url}"
        assert tensor.check_images_size(), "Не все изображения одинакового размера"
        time.sleep(5)
    finally:
        driver.quit()