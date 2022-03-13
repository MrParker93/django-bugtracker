import time
import unittest

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException


MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
        
    def wait_for_row_in_table(self, row_text):
        start_time = time.time()
        keep_going = True
        while keep_going:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                keep_going = False
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User has heard about a cool new online to-do app.
        # They go to check out its homepage.
        self.browser.get(self.live_server_url)

        # They notice the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # They are invited to enter a to-do item straight away
        input_box = self.browser.find_element(By.ID,'id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # They type "Buy peacock feathers" into a text box (Their hooby is
        # tying fly-fishing lures)
        input_box.send_keys('Buy peacock feathers')

        # When they hit enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: Buy peacock feathers')

        # There is still a text box inviting them to add another item. They
        # enter "Use peacock feathers to make fly" (They are very methodical)
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        
        input_box.send_keys('Use peacock feathers to make fly')
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_table('2: Use peacock feathers to make fly')   
        self.wait_for_row_in_table('1: Buy peacock feathers')
    
        # The page updates again, and now shows both items on their list

        # They wonder whether the to-do app will remember their list. Then they
        # see that the app has generated a unique URL for them -- there is some 
        # explanatory text to that effect.
        # self.fail('Finish the test!')

        # They visit that URL - the to-do list is still there.

        # Satisfied, they go back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):

        # A second user starts a new to-do list
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Buy peacock feathers')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: Buy peacock feathers')

        # They notice their list has a unique URL
        user_list_url = self.browser.current_url
        self.assertRegex(user_list_url, '/lists/.+')

        # Another new user comes along

        ##  We use a new browser session to ensure that no information from
        ## the previous user is coming through cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # The current user visits the homepage. There is no sign of the
        # previous user's lists
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # The current user starts a new to-do list by enter a new item
        # They are less interesting than the previous user..
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Buy milk')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: Buy milk')

        # The current user gets their own unique URL
        user_two_list_url = self.browser.current_url
        self.assertRegex(user_two_list_url, '/lists/.+')
        self.assertNotEqual(user_two_list_url, user_list_url)

        # Again, there is no trace of the previous users list
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisified, both users go to sleep