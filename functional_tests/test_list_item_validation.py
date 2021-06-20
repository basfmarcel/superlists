from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from .lists_page import ListPage
from time import sleep


class ItemValidationTest(FunctionalTest):
    def get_error_element(self):
        return self.browser.find_element_by_css_selector(".has-error")

    def test_cannot_add_empty_list_items(self):
        listpage = ListPage(self)
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        listpage.get_item_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request and does not load the list page
        self.wait_for(
            lambda: self.browser.find_elements_by_css_selector("#id_text:invalid")
        )

        # She starts typing some text for the new item and the error disappears
        listpage.get_item_input_box().send_keys("Buy milk")
        self.wait_for(
            lambda: self.browser.find_elements_by_css_selector("#id_text:valid")
        )

        # And she can submit it successfully
        listpage.get_item_input_box().send_keys(Keys.ENTER)
        listpage.wait_for_row_in_list_table("Buy milk", 1)

        # Perversely, she now decides to submit a second blank list item
        listpage.get_item_input_box().send_keys(Keys.ENTER)

        # Again the browser will not comply
        self.wait_for(
            lambda: self.browser.find_elements_by_css_selector("#id_text:invalid")
        )

        # And she can correct it by filling some text in
        listpage.get_item_input_box().send_keys("Make tea")
        self.wait_for(
            lambda: self.browser.find_elements_by_css_selector("#id_text:valid")
        )
        listpage.get_item_input_box().send_keys(Keys.ENTER)
        listpage.wait_for_row_in_list_table("Buy milk", 1)
        listpage.wait_for_row_in_list_table("Make tea", 2)

    def test_cannot_add_duplicate_items(self):
        listpage = ListPage(self)
        # Edith goes to the home page and starts a new list
        self.browser.get(self.live_server_url)
        listpage.add_list_item("Buy wellies")

        # She accidentially tries to input a duplicate item
        listpage.get_item_input_box().send_keys("Buy wellies")
        listpage.get_item_input_box().send_keys(Keys.ENTER)

        # She sees a helpful error message
        self.wait_for(
            lambda: self.assertEqual(
                self.get_error_element().text,
                "You've already got this in your list",
            )
        )

    def test_error_messages_are_cleared_on_input(self):
        listpage = ListPage(self)
        # Edith starts a list and causes a validation error
        self.browser.get(self.live_server_url)
        listpage.add_list_item("Banter to thick")
        listpage.get_item_input_box().send_keys("Banter to thick")
        listpage.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(self.get_error_element().is_displayed()))

        # She starts typing in the input box to clear the error
        listpage.get_item_input_box().send_keys("a")

        # She is pleased to see that the error message disappears
        self.wait_for(lambda: self.assertFalse(self.get_error_element().is_displayed()))
