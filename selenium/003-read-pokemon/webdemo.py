#!/usr/bin/python3
##
## ref: https://www.zenrows.com/blog/firefox-headless#how-do-i-start-firefox-headless
from selenium import webdriver
from selenium.webdriver.common.by import By

url = "https://scrapeme.live/shop/"

from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument("-headless")

with webdriver.Firefox(options=options) as driver:
	driver.get(url)

	print("Page URL:", driver.current_url)
	print("Page Title:", driver.title)

	parent_elements = driver.find_elements(By.XPATH, "//a[@class='woocommerce-LoopProduct-link woocommerce-loop-product__link']")
	for parent_element in parent_elements:
		pokemon_name = parent_element.find_element(By.XPATH, ".//h2")
		pokemon_link = parent_element.get_attribute("href")
		pokemon_price = parent_element.find_element(By.XPATH, ".//span")

		temporary_pokemons_data = {
			"name": pokemon_name.text,
			"link": pokemon_link,
			"price": pokemon_price.text
		}

		print(temporary_pokemons_data)
