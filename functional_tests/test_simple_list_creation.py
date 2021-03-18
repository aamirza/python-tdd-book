import unittest

from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app.
        # She goes to check out its homepage.
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # She types "buy peacock feathers" into a text box (Edith'' hobby
        # is tying fly-fishing lures)
        self.add_list_item('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)

        self.add_list_item('Use peacock feathers to make a fly')
        inputbox = self.get_item_input_box()

        # The page updates again, and now shows both items on ehr list.

        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her - there is some
        # explanatory text to that effect.
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

    def test_multiple_users_can_start_lists_at_different_url(self):
        # Now a new user, Francis, comes along to the site.
        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc.
        # Francis visits the home page. There is no sign of Edith's
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, 'lists/.+')

        # She visits that URL - her to-do list is still there.
        self.browser.get(francis_list_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Buy milk', page_text)


if __name__ == "__main__":
    unittest.main()
