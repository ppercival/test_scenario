from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class BasePage:
    """
    Реализация базового класса страницы
    """

    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url):
        """
        Метод открывает url
        """
        self.driver.get(url)

    def click_element(self, locator):
        """
        Метод чтобы кликать на ссылки
        """
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(locator)
        ).click()

    def find_element(self, locator):
        """
        Метод для поиска элемента
        """
        return WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(locator)
        )

    def scroll_to_element(self, locator):
        """
        Метод прокручивает страницу до элемента
        """
        element = self.find_element(locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

        WebDriverWait(self.driver, 20).until((EC.visibility_of(element)))
        return element
