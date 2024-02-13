from datetime import date

import pandas as pd
import requests
import scrapy

from define_collection_wave import folder
from helpers import create_folder

path_bella = create_folder('81_BellaItalian', folder)

items_all = []
url = 'https://menus.tenkites.com/thebigtg/mobilemenus03'
html = requests.get(url).text
page = scrapy.Selector(text=html)
menus = page.xpath('//div[@class="k10-menu-selector__option"]/span/@data-menu-identifier').getall()
menu_names = page.xpath('//div[@class="k10-menu-selector__option"]/span/span/text()').getall()
missing_items = [
    ['Mozzarella Sticks','614 kcal', 'Crispy coated mozzarella fingers, served with smoked chipotle chilli jam',6.49,614,22.4,47.6,17.1,36.9,14.4,2.0],
    ['Minestrone Soup', '381 kcal','Minestrone with tomato, red pepper and cannellini beans, served with garlic ciabatta bread, finished with basil oil', 6.99,381,6.8,29.9,6.9,25.7,5.7,3.5],
    ['Green Olives', '199 kcal','Large green Amfissa olives, brine soaked and buttery with a tart, citrussy balance',3.99,199,1.9,10.2,0.0,17.0,3.4,5.1],
    ['Mixed Olives', '202 kcal', 'A mix of our green and black olives',3.99,202,1.5,7.1,0.2,18.4,3.1,4.1],
    ['Garlic Dough Balls','549 kcal','Oven baked dough balls tossed in garlic oil and served with garlic butter',5.99,549,7.0,36.7,6.8,40.8,10.5,1.5],
    ['Mozzarella Dough Balls', '497 kcal','Fondue style cheesy dough balls, flavoured with fresh garlic, oregano and mozzarella cheese',7.29,497,14.4,40.7,8.4,30.5,9.2,2.7],
    ['Calamari','579 kcal', 'Lightly dusted deep fried squid, served with lemon & black pepper mayonnaise', 8.49,579,17.5,24.0,2.2,45.3,2.8,3.5]
]
for item in missing_items:
    item_dict = {
        'rest_name': 'Bella Italia',
        'collection_date': date.today().strftime("%b-%d-%Y"),
        'item_name': item[0],
        'item_description': item[2],
        'menu_section': 'A La Carte, Starters',
        'Energy (kCal)':item[4],
        'Protein (g)':item[5],
        'Carb (g)':item[6],
        'of which Sugars (g)':item[7],
        'Fat (g)':item[8],
        'Sat Fat (g)':item[9],
        'Salt (g)':item[10]
        }
    items_all.append(item_dict)

for i in range(len(menus)):
    menu_name = menu_names[i].strip()
    page = scrapy.Selector(text=requests.get(
        f'https://menus.tenkites.com//thebigtg/mobilemenus03?cl=true&mguid={menus[i]}&internalrequest=true').text)
    menu_sections = page.xpath('//section//section')



    for menu_section in menu_sections:
        menu_section_name = menu_section.xpath('normalize-space(.//div[@class="k10-course__name"]/text())').get()
        items = menu_section.xpath('.//div[@class="k10-l-grid__item"]')
        for item in items:
            # if substitution available
            item_vars = item.xpath('.//div[@class="k10-byo__item k10-byo-item k10-byo-item_recipe "]')
            if len(item_vars) == 0:
                item_vars = item.xpath('.//div[@class="k10-recipe__header "]')


                item_description = item.xpath('normalize-space(.//div[@class="k10-byo-item__desc"]/text())').get()
                if len(item_description) < 5:
                    item_description = item.xpath('normalize-space(.//div[@class="k10-recipe__desc"]/text())').get()

            if len(item.xpath('.//div[@class="k10-byo__header"]')) > 0:
                wine_name = item.xpath(
                    'normalize-space(//div[@class="k10-byo__header"]//span[@class="k10-byo__name"]/text())').get()
                wine_description = item.xpath(
                    'normalize-space(//div[@class="k10-byo__header"]//div[@class="k10-byo__desc"]/text())').get()
                for item_var in item_vars:
                    item_name = wine_name + ' ' + item_var.xpath(
                        'normalize-space(.//span[@class="k10-byo-item__name"]/text())').get()
                    item_description = wine_description
                    item_dict = {
                        'rest_name': 'Bella Italia',
                        'collection_date': date.today().strftime("%b-%d-%Y"),
                        'item_name': item_name,
                        'item_description': item_description,
                        'menu_section': menu_name + ', ' + menu_section_name
                    }
                    nutrition_row = item_var.xpath('.//table//tr')
                    for row in nutrition_row:
                        item_dict.update({
                            row.xpath('./td[1]/text()').get():
                                row.xpath('./td[2]/text()').get()
                        })
                    items_all.append(item_dict)
            else:
                for item_var in item_vars:
                    item_name = item_var.xpath('normalize-space(.//span[@class="k10-byo-item__name"]/text())').get()
                    if item_name == '' or len(item_name) > 5:
                        item_name = item_var.xpath('normalize-space(.//span[@class="k10-recipe__name"]/text())').get()
                    item_dict = {
                        'rest_name': 'Bella Italia',
                        'collection_date': date.today().strftime("%b-%d-%Y"),
                        'item_name': item_name,
                        'item_description': item_description,
                        'menu_section': menu_name + ', ' + menu_section_name
                    }
                    nutrition_row = item_var.xpath('.//table//tr')
                    for row in nutrition_row:
                        item_dict.update({
                            row.xpath('./td[1]/text()').get():
                                row.xpath('./td[2]/text()').get()
                        })
                    items_all.append(item_dict)

items_df = pd.DataFrame(items_all)
items_df.to_csv(path_bella + '/bella_items.csv')
