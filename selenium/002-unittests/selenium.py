#!/usr/bin/python3

import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

## setup python unittest fixture
class PythonOrgSearchFixture(unittest.TestCase):

    ## the fixture needs a setUp() and a tearDown()
    def setUp(self):
        self.driver = webdriver.Firefox()

    def testSearchInPythonOrg(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element(By.NAME, "q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        self.assertNotIn("No results found.", driver.page_source)

    ## the fixture needs a setUp() and a tearDown()
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
