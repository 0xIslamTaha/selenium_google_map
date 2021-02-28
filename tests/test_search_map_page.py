from tests.base_tests import BaseTest
from lib.page_objects.search_map_page import SearchMapPage


class TestSearchMapPage(BaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_map_page = SearchMapPage()

    def setUp(self) -> None:
        print('\t')
        self.info(f'{self._testMethodName}')
        self.search_map_page.get_search_map_page()

    def test001_search_text_box_is_editable(self):
        """
        TC001: Verify that text box is editable.
            Pre-conditions:
                - Go to https://google.com/maps
                - Accept cookies
            Steps:
                1- Get data from text box, should be empty.
                2- Set keyword in text box.
                3- Verify that text box has this keyword.
        """
        self.info('Get data from text box, should be empty.')
        self.assertFalse(self.search_map_page.get_search_box_text(), "Text box should be empty.")

        random_text = self.generate_random_text()
        self.info('Set {} keyword in text box.'.format(random_text))
        self.search_map_page.set_search_box_text(text=random_text)

        self.info('Verify that text box has {} value.'.format(random_text))
        self.assertEqual(random_text, self.search_map_page.get_search_box_text(),
                         "Text box should have {} value.".format(random_text))

    def test002_auto_suggestions_list_returns_correct_results(self):
        """
        TC002: Verify that auto-suggestions list returns correct results.
            Pre-conditions:
                - Go to https://google.com/maps
                - Accept cookies
            Steps:
                1- Search for a restaurant.
                2- Verify that the suggestions list has the correct text.
        """
        self.info('Search for a restaurant.')
        self.search_map_page.set_search_box_text(text='restaurant')

        self.info('Verify that the suggestions list has the correct text.')
        suggestions_list_data = self.search_map_page.get_suggestions_data_list()
        for data in suggestions_list_data:
            self.assertIn('restaurant', data.lower())
