#!/bin/python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

## instance of firefox
driver = webdriver.Firefox()

## navigate to web page, and assert
driver.get("http://www.python.org")
assert "Python" in driver.title

## locate element by name
elem = driver.find_element(By.NAME, "q")

## use keys to input some search request
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)

## assert search result was not empy
assert "No results found." not in driver.page_source

## close down, alternatively use quit()
driver.close()
