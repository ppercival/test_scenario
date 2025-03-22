from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class TensorPage(BasePage):
    POWER_IN_PEOPLE_BLOCK = (By.XPATH, "//p[text()='Сила в людях']")
    POWER_IN_PEOPLE_LOCATOR = (By.XPATH, "//div[contains(@class, 'tensor_ru-Index__block4-content')]//p[contains(text(), 'Сила в людях')]")
    MORE_LINK = (By.LINK_TEXT, "Подробнее")
    WORKING_SECTION = (By.XPATH, "//section[contains(@class, 'work')]")
    TIMELINE_IMAGES = (By.XPATH, "//section[contains(@class, 'work')]//img")

    def check_power_in_people(self):
        """Прокручиваем страницу к блоку 'Сила в людях' и проверяем его наличие"""
        element = self.scroll_to_element(self.POWER_IN_PEOPLE_BLOCK)
        assert element.is_displayed(), "Блок 'Сила в людях' не виден"

    def go_to_about(self):
        """Переход в 'Подробнее'"""
        power_in_people_block = self.driver.find_element(*self.POWER_IN_PEOPLE_LOCATOR)
        more_link = power_in_people_block.find_element(By.XPATH, ".//following-sibling::p//a[contains(text(), 'Подробнее')]")
        more_link.click()

    def check_images_size(self):
        """Проверяем, что изображения одной высоты и ширины"""
        images = self.driver.find_elements(*self.TIMELINE_IMAGES)
        sizes = [(img.size['width'], img.size['height']) for img in images]
        return all(size == sizes[0] for size in sizes)