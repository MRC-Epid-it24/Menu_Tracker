import re
from time import sleep

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from define_collection_wave import folder
from helpers import create_folder, web_browser_path

path_costa = create_folder('3_CostaCoffee', folder)

costa_url = "https://www.costa.co.uk/menu/"
options = webdriver.ChromeOptions()
# options.headless = True  # turn on the headless mode!
s = Service(web_browser_path)
browser = webdriver.Chrome(service=s)
browser.get(costa_url)
sleep(20)
# accept cookie
browser.find_element(by=By.ID, value='onetrust-accept-btn-handler').click()
sleep(3)
drink_buttons = browser.find_elements(by=By.XPATH, value= '//div[@data-cy = "product-item"]')


def parse_item(page, size=None, milk=None):
    soup = BeautifulSoup(page, 'html.parser')
    product_detail = soup.find_all('div', {'class': 'productViewstyles__DataWrapper-sc-1f5jhow-1 fZAjTD'})
    if product_detail:
        product_name = product_detail[0].h1.text if product_detail[0].h1 else product_detail[0].h2.text
        product_description = product_detail[0].p.text if product_detail[0].p else "N/A"
        product_ingredients = soup.find('div', {'class': 'ingredients'}).text if soup.find('div', {
        'class': 'ingredients'}) else "N/A"
        row_dict = {'Product_Name': product_name, 'Product_Description': product_description,
            'Size': size, 'Milk': milk,
            'Product_Ingredients': product_ingredients}
        print("\n\n\nProduct Detail:\n\n\n", row_dict, "\n\n\n")
    else:
        # print("The page with error: \n", page, "\n\n")
        print("\n\n\n The page has error: \n\n\n")
        return {}
    alltables = soup.find_all('table')
    table_titles = [table.h2.text for table in alltables]
    
    # nutrition information collection
    if alltables:
        nutrition_table = alltables[0]
        nutrition_columns = [name.text for name in nutrition_table.findAll('th')]
        nutrition_columns2 = [re.sub('\(.*?\)', '', name) for name in nutrition_columns]
        In_Store = [s for i, s in enumerate(nutrition_columns) if 'In-Store' in s]
        In_Store_column = In_Store[0] if In_Store else 'NA'
        Take_Out = [s for i, s in enumerate(nutrition_columns) if 'Take-Out' in s]
        Take_Out_column = Take_Out[0] if Take_Out else 'NA'
        serving_size_In_Store = In_Store_column[In_Store_column.find("(") + 1:In_Store_column.find(")")]
        serving_size_Take_Out = Take_Out_column[Take_Out_column.find("(") + 1:Take_Out_column.find(")")]
        if row_dict:
            for row in nutrition_table.findAll('tr')[1:]:
                text = [item.text for item in row.findAll('td')]
                for i in range(len(text) - 1):
                    row_dict.update({text[0] + '_' + nutrition_columns2[i + 1]: text[i + 1]})
            row_dict.update({'ServingSize_In_Store': serving_size_In_Store,
                            'ServingSize_Take_Out': serving_size_Take_Out})

        # allergen table
        allergen_table = alltables[3]
        for row in allergen_table.findAll('tr'):
            text = [item.text for item in row.findAll('td')]
            if row_dict:
                row_dict.update({text[0]: text[1]})
        # gluten table
        gluten_table = alltables[2]
        for row in gluten_table.findAll('tr'):
            text = [item.text for item in row.findAll('td')]
            if row_dict:
                row_dict.update({text[0]: text[1]})
        return row_dict
    
    else:
        print("The page has no table: \n\n\n")

        if row_dict:
            return row_dict
        else:
            return {}

records = []
for drink in drink_buttons:
    print('\n\n', drink.text, '\n\n')
    # # The page is broken. Skip it.
    # if drink.text == 'Mint Tea':
    #     continue
    category = drink.find_element(by = By.XPATH, value = "../../h2[@class='categoryHeader']").text
    print('\n', category, '\n')
    browser.execute_script("arguments[0].click();", drink)

    # aria-controls="content-allergens-information"
    # aria-controls="content-nutritional-information"
    sleep(5)
    sizes = browser.find_elements(by=By.XPATH, value='//div[@class="filterGroup size"]/button')
    #value='//p[contains(@class, "customiseDrinkstyles__StyledCustomiseDrink-sc-19htd1k-0 hTNDBE") and contains(@class, 'igsAgt')]/following-sibling::div[contains(@class, 'filterGroup')][1]//button')
    milk_choices = browser.find_elements(by=By.XPATH, value='//div[@class="filterGroup milk"]/button')
    if len(sizes) > 0:
        for size in sizes:
            browser.execute_script("arguments[0].click();", size)
            if len(milk_choices) > 0:
                for milk in range(len(milk_choices)):
                    browser.execute_script("arguments[0].click();", milk_choices[milk])
                    row = parse_item(page=browser.page_source, milk=milk_choices[milk].text, size=size.text)
                    row.update({'Category': category})
                    records.append(row)
            else:
                row = parse_item(page=browser.page_source, size=size.text)
                row.update({'Category': category})
                records.append(row)
    else:
        if len(milk_choices) > 0:
            for milk in range(len(milk_choices)):
                browser.execute_script("arguments[0].click();", milk_choices[milk])
                row = parse_item(page=browser.page_source, milk=milk_choices[milk].text)
                row.update({'Category': category})
                records.append(row)
        else:
            row = parse_item(page=browser.page_source)
            row.update({'Category': category})
            records.append(row)
    close_button = browser.find_element(by=By.XPATH, value = '//button[@class="productViewstyles__CloseButton-sc-1f5jhow-2 eISAhT"]')
    close_button.click()
    sleep(2)

browser.find_element(by=By.XPATH, value = '//button[@data-cy ="page-select__food"]').click()
food_button = browser.find_elements(by=By.XPATH, value= '//div[@data-cy = "product-item"]')


for food in range(len(food_button)):
    # category = food_button[food].find_element_by_xpath(
    #     ".//parent::div/preceding-sibling::div[@class='category-header']").text
    category = food_button[food].find_element_by_xpath("../../h2[@class='categoryHeader']").text
    browser.execute_script("arguments[0].click();", food_button[food])
    sleep(4)
    try:
        row = parse_item(page=browser.page_source)
        row.update({'Category': category})
        records.append(row)
    except:
        print('item not captured')
    close_button = browser.find_element(by=By.XPATH, value='//button[@class="productViewstyles__CloseButton-sc-1f5jhow-2 eISAhT"]')
    close_button.click()
    sleep(2)

browser.quit()
costa = pd.DataFrame(records)
# costa = costa.append(food_records)
costa.to_csv(path_costa + '/costa_items.csv')