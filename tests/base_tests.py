from unittest import TestCase
from lib.selenium_plus import SeleniumPlus
from uuid import uuid4


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.selenium_plus = SeleniumPlus()
        cls.selenium_plus.get_driver()
        cls.info = cls.selenium_plus.LOGGER.info

    @classmethod
    def tearDownClass(cls) -> None:
        cls.selenium_plus.quit_driver()

    @staticmethod
    def generate_random_text():
        return str(uuid4()).replace("-", "")[:10]
