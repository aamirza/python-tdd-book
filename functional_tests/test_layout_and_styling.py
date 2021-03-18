import unittest

from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Edith goes to the homepage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centred
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)

        # She starts a new list and sees the input is nicely centred there too.
        self.add_list_item('texting')
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)


if __name__ == "__main__":
    unittest.main()
