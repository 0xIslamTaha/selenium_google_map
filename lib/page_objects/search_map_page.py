from lib.page_objects.page import BasePage
from time import sleep

class SearchMapPage(BasePage):
    def get_search_map_page(self):
        self.selenium_plus.driver.get(self.selenium_plus.url)
        self.accept_cookies()

    def get_search_box_text(self):
        return self.selenium_plus.get_value(locator='search_map_page:search_box')

    def set_search_box_text(self, text, submit=False):
        self.selenium_plus.set_text(locator='search_map_page:search_box', text=text)
        if submit:
            self.selenium_plus.click(locator='search_map_page:search_box')

    def get_suggestions_data_list(self):
        sleep(2) # this is a hack, we shouldnt do that in real projects.
        return self.selenium_plus.get_text(locator='search_map_page:search_suggetion_list').split('\n')
