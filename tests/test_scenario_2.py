from selenium import webdriver
from pages.sbis_page import SbisPage

"""
Реализация второго сценария
pytest -s tests/test_scenario_2.py
"""

def test_scenario_2():
    driver = webdriver.Chrome()
    sbis = SbisPage(driver)

    try:
        sbis.open_url("https://sbis.ru/")
        sbis.go_to_contacts()

        initial_region = sbis.get_current_region()
        print(f"Определённый регион: {initial_region}")

        assert initial_region, "Регион не определился автоматически"

        initial_partners = sbis.get_partners_list()
        assert initial_partners, "Список партнёров отсутствует"

        sbis.change_region("Камчатский край")

        new_region = sbis.get_current_region()
        assert new_region == "Камчатский край", f"Регион не изменился, текущий: {new_region}"

        new_partners = sbis.get_partners_list()
        assert new_partners != initial_partners, "Список партнёров не изменился"

        sbis.verify_url_contains("kamchatskij-kraj")
        sbis.verify_title_contains("Камчатский край")

    finally:
        driver.quit()