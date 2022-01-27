import unittest
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
        
    def test_can_start_a_list_and_retrieve_it_later(self):
        # User has heard about a cool new online to-do app.
        # They go to check out its homepage.
        self.browser.get('http://localhost:8000')

        # They notice the page title and header mention to-do lists
        self.assertIn('To-do', self.browser.title)
        self.fail('Finish the test!')

        # They are invited to enter a to-do item straight away

        # They type "Buy peacock feathers" into a text box (Their hooby is
        # tying fly-fishing lures)

        # When they hit enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list

        # There is still a text box inviting them to add another item. They
        # enter "Use peacock feathers to make fly" (They are very methodical)

        # The page updates again, and now shows both items on their list

        # They wonder whether the to-do app will remember their list. Then they
        # see that the app has generated a unique URL for them -- there is some 
        # explanatory text to that effect.

        # They visit that URL - the to-do list is still there.

        # Satisfied, they go back to sleep

if __name__ == "__main__":
    unittest.main()