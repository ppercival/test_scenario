from selenium import webdriver

"""
Это учебный скрипт чтобы открывать браузер
"""

def test_open_google():
    driver = webdriver.Chrome()
    driver.get("https://www.google.com")
    assert "Google" in driver.title
    driver.quit()