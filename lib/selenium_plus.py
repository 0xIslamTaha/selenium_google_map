from testconfig import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from loguru import logger
from contextlib import contextmanager
import yaml, os


class SeleniumPlus:
    # waiting time
    POLL_FREQUENCY = 0.1

    TIME_TINY = 2
    TIME_SMALL = 5
    TIME_MEDIUM = 10
    TIME_LARGE = 15
    TIME_X_LARGE = 60

    IMPLICITLY_WAIT = 60
    EXPLICITLY_WAIT = 30

    # logger instance
    LOGGER = logger

    # viewport
    width = 1280
    height = 720

    # singleton pattern
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    # initialization
    def __init__(self):
        self.url = config['site']['url']
        self.browser = config['browser']['browser'].lower()
        self.headless = config['browser']['headless'].capitalize()
        self.locators = self._load_locators(config['locators']['path'])

    def get_driver(self):
        if self.headless == 'True':
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_experimental_option("prefs", {
                "download.default_directory": os.path.expanduser("~/Downloads"),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing_for_trusted_sources_enabled": False,
                "safebrowsing.enabled": False
            })
            self.driver = webdriver.Chrome(chrome_options=options)
        else:
            if self.browser == 'chrome':
                options = Options()
                options.add_argument('--ignore-certificate-errors')
                self.driver = webdriver.Chrome(chrome_options=options)
            elif self.browser == 'firefox':
                self.driver = webdriver.Firefox()
            elif self.browser == 'ie':
                self.driver = webdriver.Ie()
            elif self.browser == 'opera':
                self.driver = webdriver.Opera()
            elif self.browser == 'safari':
                self.driver = webdriver.Safari

        self.driver.implicitly_wait(SeleniumPlus.IMPLICITLY_WAIT)
        self.driver.set_window_size(SeleniumPlus.width, SeleniumPlus.height)
        self.wait = WebDriverWait(self.driver, SeleniumPlus.EXPLICITLY_WAIT, SeleniumPlus.POLL_FREQUENCY)

    @staticmethod
    def _load_locators(locators_path):
        with open(locators_path) as file:
            return yaml.safe_load(file)

    @contextmanager
    def change_implicit_wait(self, new_value=0.001):
        self.driver.implicitly_wait(new_value)
        try:
            yield
        finally:
            self.driver.implicitly_wait(SeleniumPlus.IMPLICITLY_WAIT)

    def _parse_locator(self, locator):
        _page, _locator = locator.split(':')
        method = self.locators[_page][_locator]['by'].upper()
        value = self.locators[_page][_locator]['value']
        return method, value

    def _wait_until_element_located(self, locator):
        method, value = self._parse_locator(locator)
        with self.change_implicit_wait():
            return self.wait.until(
                EC.visibility_of_element_located((getattr(By, method), value)),
                message=f"Element with locator {locator} is not on the page or not visible."
            )

    def _wait_until_element_clickable(self, locator):
        method, value = self._parse_locator(locator)
        with self.change_implicit_wait():
            return self.wait.until(
                EC.element_to_be_clickable((getattr(By, method), value)),
                                           message=f"Element with locator {locator!r} is not clickable."
            )

    def quit_driver(self):
        self.driver.quit()

    def find_element(self, locator):
        method, value = self._parse_locator(locator)
        return self.driver.find_element(by=getattr(By, method), value=value)

    def find_elements(self, locator):
        method, value = self._parse_locator(locator)
        return self.driver.find_elements(by=getattr(By, method), value=value)

    def get_text(self, locator):
        self._wait_until_element_located(locator)
        return self.find_element(locator).text

    def set_text(self, locator, text):
        self._wait_until_element_located(locator)
        self.find_element(locator).clear()
        self.find_element(locator).send_keys(text)

    def click(self, locator):
        self._wait_until_element_clickable(locator)
        self.find_element(locator).click()

    def get_attribute(self, locator, attribute):
        self._wait_until_element_located(locator)
        return self.find_element(locator).get_attribute(attribute)

    def get_value(self, locator):
        return self.get_attribute(locator, "value")