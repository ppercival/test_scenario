import os
import re
import time

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SbisPage(BasePage):

    # для первого сценария
    CONTACTS_LINK = (By.LINK_TEXT, "Контакты")
    TENSOR_BANNER = (By.XPATH, "//a[@href='https://tensor.ru/']")

    # для второго сценария
    CURRENT_REGION = (By.CSS_SELECTOR, ".sbis_ru-Region-Chooser__text")
    PARTNERS_LIST = (By.CSS_SELECTOR, ".sbisru-Contacts-List__col")
    REGION_POPUP = (By.CSS_SELECTOR, ".sbis_ru-Region-Panel")
    # REGION_ITEM = lambda self, region_name: (By.XPATH, f"//span[text()='{region_name}']")

    def REGION_ITEM(self, region_name):
        return By.XPATH, f"//li[contains(@class, 'sbis_ru-Region-Panel__item')]//span[@title='{region_name}']"

    # для третьего сценария
    LOCAL_VERSIONS_LINK = (By.XPATH, "//a[contains(text(), 'Скачать локальные версии')]")
    PLUGIN_DOWNLOAD_LINK = (By.LINK_TEXT, "Скачать локальные версии")
    DOWNLOAD_FOLDER = os.path.expanduser("~/downloads")

    """
    Далее методы для выполнения сценариев
    """

    # для первого сценария
    def go_to_contacts(self):
        self.click_element(self.CONTACTS_LINK)

    def click_tensor_banner(self):
        self.click_element(self.TENSOR_BANNER)


    # для второго сценария
    def get_current_region(self):
        return self.find_element(self.CURRENT_REGION).text

    def get_partners_list(self):
        elements = self.driver.find_elements(*self.PARTNERS_LIST)
        return [el.text for el in elements]

    # def change_region(self, region_name):
    #     self.click_element(self.CURRENT_REGION)
    #     WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.REGION_POPUP))
    #     self.click_element(self.REGION_ITEM(region_name))

    def change_region(self, region_name):
        self.click_element(self.CURRENT_REGION)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.REGION_POPUP))
        self.click_element(self.REGION_ITEM(region_name))
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element(self.CURRENT_REGION, region_name)
        )

    def verify_url_contains(self, region_name):
        WebDriverWait(self.driver, 10).until(
            lambda d: region_name.lower().replace(" ", "-") in d.current_url
        )

    def verify_title_contains(self, region_name):
        WebDriverWait(self.driver, 10).until(
            lambda d: region_name in d.title
        )


    # для третьего сценария
    def go_to_local_versions(self):
        self.click_element(self.LOCAL_VERSIONS_LINK)

    def download_plugin(self):
        self.scroll_to_element(self.PLUGIN_DOWNLOAD_LINK)
        self.click_element(self.PLUGIN_DOWNLOAD_LINK)
        plugin_link = self.find_element(self.PLUGIN_DOWNLOAD_LINK).get_attribute("href")
        self.driver.get(plugin_link)

    def get_expected_file_size(self):
        download_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Скачать')]"))
        )
        download_link_text = download_button.text.strip()
        print(f"Текст ссылки: {download_link_text}")

        match = re.search(r'(\d+\.\d+)\s*МБ', download_link_text)
        if match:
            expected_file_size_mb = float(match.group(1))
            print(f"Ожидаемый размер файла: {expected_file_size_mb} МБ")
            return expected_file_size_mb
        else:
            print("Не удалось извлечь размер файла.")
            return None

    def click_link_by_text(self, link_text):
        link_locator = (By.XPATH, f"//a[contains(normalize-space(text()), '{link_text}')]")
        self.click_element(link_locator)


    @staticmethod
    def wait_for_download(download_dir, file_name, timeout=30):
        file_path = os.path.join(download_dir, file_name)
        temp_file_path = file_path + ".crdownload"

        start_time = time.time()
        while time.time() - start_time < timeout:
            if os.path.exists(file_path) and not os.path.exists(temp_file_path):
                print("Файл загружен")
                return True
            time.sleep(1)

        print("Файл не был загружен")
        return False
