from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest
from .server_tools import create_session_on_server

from .management.commands.create_session import create_pre_authenticated_session

User = get_user_model()


class MyListTest(FunctionalTest):
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'edith@example.com'
        # self.browser.get(self.live_server_url)
        # self.wait_to_be_logged_out(email)

        # Edith is a logged-in user
        self.create_pre_authenticated_session(email)
        # self.browser.get(self.live_server_url)
        # self.wait_to_be_logged_in(email)
        self.browser.get(self.live_server_url)
        first_item = 'Reticulate splines'
        self.add_list_item(first_item)
        self.add_list_item('Immanentize eschaton')
        first_list_url = self.browser.current_url

        # She notices a "My lists" link, for the first time.
        self.browser.find_element_by_link_text('My lists').click()

        # She sees that her list is in there, named according to its
        # first list item
        self.wait_for(
            lambda: self.browser.find_element_by_link_text(first_item)
        )
        self.browser.find_element_by_link_text(first_item).click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # She decides to start another list, just to see
        self.browser.get(self.live_server_url)
        new_list_item = 'Click cows'
        self.add_list_item(new_list_item)
        second_list_url = self.browser.current_url

        # Under "my lists", her new list appears
        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text(new_list_item)
        )
        self.browser.find_element_by_link_text(new_list_item).click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_elements_by_link_text('My lists'), []
            )
        )
