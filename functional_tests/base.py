from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
from .server_tools import reset_database, create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.staging_server = os.environ.get("STAGING_SERVER")
        if self.staging_server:
            self.live_server_url = "http://" + self.staging_server
            reset_database(self.staging_server)

    def tearDown(self):
        self.browser.quit()

    def wait(fn):
        def modified_fn(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    time.sleep(0.5)

        return modified_fn

    @wait
    def wait_for(self, fn):
        return fn()

    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element_by_link_text("Log out")
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element_by_name("email")
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertNotIn(email, navbar.text)

    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(
            dict(name=settings.SESSION_COOKIE_NAME, value=session_key, path="/")
        )
