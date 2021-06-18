from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest
from time import sleep

User = get_user_model()


class MyListsTest(FunctionalTest):
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # A is a logged-in user
        self.create_pre_authenticated_session("a@b.com")

        # She goes to the home page and starts a list
        self.browser.get(self.live_server_url)
        self.add_list_item("Reticulate splines")
        # self.add_list_item("Immanentize eschaton")
        # Bei Hinzufügen des zweiten Elements kommt es zu einem unerwarteten Fehler.
        # Das zweite Element wird an erster Stelle eingefügt, erhält "1: ..."
        # Das eigentlich erste Element wird an zweite Stelle geschoben
        # und erhält "2: ..."
        first_list_url = self.browser.current_url

        # She notices a "My Lists" link, for the first time.
        self.browser.find_element_by_link_text("My Lists").click()

        # She sees that her list is in there, named according to its first line item
        self.wait_for(
            lambda: self.browser.find_element_by_link_text("Reticulate splines")
        )
        self.browser.find_element_by_link_text("Reticulate splines").click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # She decides to start another list, just to see.
        self.browser.get(self.live_server_url)
        self.add_list_item("Click cows")
        second_list_url = self.browser.current_url

        # Under "My Lists", her new list appears
        self.browser.find_element_by_link_text("My Lists").click()
        self.wait_for(lambda: self.browser.find_element_by_link_text("Click cows"))
        self.browser.find_element_by_link_text("Click cows").click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # She logs out. The "My Lists" option disappears
        self.browser.find_element_by_link_text("Log out").click()
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_elements_by_link_text("My Lists"), []
            )
        )
