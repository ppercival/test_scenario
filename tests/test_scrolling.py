import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

"""
Это учебный скрипт чтобы научиться скроллить страницу до нужного элемента
pytest -s tests/test_scrolling.py
"""

def test_scroll_to_element():
    driver = webdriver.Chrome()
    driver.get("https://tensor.ru/")
    time.sleep(2)

    try:
        element = driver.find_element(By.XPATH, "//p[text()='Сила в людях']")

        actions = ActionChains(driver)
        actions.move_to_element(element).perform()

        print("Элемент найден!")

        time.sleep(3) # просто чтобы посмотреть подольше

    except NoSuchElementException:
        print("Элемент не найден!")

    finally:
        driver.quit()

