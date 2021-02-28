from lib.selenium_plus import SeleniumPlus


class BasePage:
    def __init__(self):
        self.selenium_plus = SeleniumPlus()

    def accept_cookies(self):
        with self.selenium_plus.change_implicit_wait(1):
            if self.selenium_plus.find_elements('cookies:frame'):
                self.selenium_plus.driver.switch_to.frame(0)
                self.selenium_plus.click('cookies:accept_btn')
                self.selenium_plus.driver.switch_to_default_content()
