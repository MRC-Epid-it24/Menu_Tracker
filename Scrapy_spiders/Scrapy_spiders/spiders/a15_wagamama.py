from datetime import date
from time import sleep

import scrapy
from browserPath import web_browser_path
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class A15WagamamaSpider(scrapy.Spider):
    name = '15_Wagamama'
    allowed_domains = ['www.wagamama.com']
    start_urls = ['https://www.wagamama.com/menu?category=sides-sharing']

    def __init__(self):
        self.driver = webdriver.Chrome(web_browser_path)
        self.data = []

    def parse(self, response):
        self.driver.get(response.url)

        # try:
        #     WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))).click()
        # except TimeoutException:
        #     self.log("The cookie button was not clickable within 10 seconds or not present.")
    
        category_buttons = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//button[contains(@class, "_menuItemButton_1etan_2")]')))
        # category_buttons = self.driver.find_elements(By.XPATH, '//button[contains(@class, "_menuItemButton_1etan_2")]')
        for button in category_buttons:
            self.driver.execute_script("arguments[0].click();", button)
            sleep(1)  # Wait for the content to load
           
            food_buttons = self.driver.find_elements(By.XPATH, '//div[contains(@class, "_bottom_pqbyt_34")]//button[contains(@class, "_customButton_dzbl6_2")]')
            for food_button in food_buttons:
                try:
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(food_button))
                    self.driver.execute_script("arguments[0].click();", food_button)
                    sleep(1)  # Wait for modal to open
                    item_description = driver.find_elements(By.CLASS_NAME, '_description_1nw6t_10').text
                    table_rows = driver.find_elements(By.XPATH, '//table//tr')
                    allergens = driver.find_element(By.CLASS_NAME, '_allergens_1741a_15').text
                    for row in table_rows:
                        cells = row.find_elements(By.TAG_NAME, 'td')
                        print("Cells:", cells)
                        nutrient = cells[0].text
                        if cells:
                            self.data = self.data.append({
                                'rest_name': 'Wagamama',
                                'collection_date': date.today().strftime("%b-%d-%Y"),
                                'item_name': food_button.text,
                                'item_description': item_description,
                                'allergens': allergens,
                                nutrient: cells[1].text,
                                nutrient + '_100': cells[2].text,
                            })         

                    try: 
                        # Close the modal to return to the menu
                        close_button = driver.find_element(By.XPATH, '//button[@id="close"]')
                        close_button.click()
                    except Exception as e:
                        self.log(f"Failed to close modal: {e}")
                        continue

                except Exception as e:
                    self.log(f"Error navigating to item details: {e}")
                    continue
        self.driver.quit()
        for item in self.data:
            yield item