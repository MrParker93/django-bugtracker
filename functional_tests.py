import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
        
    def check_for_row_in_table(self, row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User has heard about a cool new online to-do app.
        # They go to check out its homepage.
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)

        self.check_for_row_in_table('1: Buy peacock feathers')

        # There is still a text box inviting them to add another item. They
        # enter "Use peacock feathers to make fly" (They are very methodical)
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Use peacock feathers to make fly')
        input_box.send_keys(Keys.ENTER)
        time.sleep(2)

        self.check_for_row_in_table('1: Buy peacock feathers')
        self.check_for_row_in_table('2: Use peacock feathers to make fly')
    
        # The page updates again, and now shows both items on their list

        # They wonder whether the to-do app will remember their list. Then they
        # see that the app has generated a unique URL for them -- there is some 
        # explanatory text to that effect.
        self.fail('Finish the test!')

        # They visit that URL - the to-do list is still there.

        # Satisfied, they go back to sleep

if __name__ == "__main__":
    unittest.main()