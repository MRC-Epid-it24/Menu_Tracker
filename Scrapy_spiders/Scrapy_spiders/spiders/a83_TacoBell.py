import re
from datetime import date

import scrapy
from datetime import date
from scrapy import Spider
from collections import Counter



class A83TacobellSpider(scrapy.Spider):
    name = '83_TacoBell'
    allowed_domains = ['www.nutritionix.com']
    start_urls = ['https://www.nutritionix.com/taco-bell-uk/menu/premium']

    def parse(self, response):
        nutrient_dict = {}
        tablerows = response.xpath('//tbody/tr')
        cat_names = []
        for counter,row in enumerate(tablerows):
            if row.xpath('./@class').get() == 'subCategory':
                cat_name = row.xpath('.//h3/text()').get()
                print('Cat name:',cat_name, counter)
                cat_names.append([cat_name,counter])

        print(cat_names)
        odd_items = response.xpath('//tr[@class="odd"]')
        even_items = response.xpath('//tr[@class="even"]')
        items = [element for pair in zip(odd_items,even_items) for element in pair]

        list = {'Featured': [x for x in range(12)], 'Tacos': [x for x in range(12, 31)],
                'Burritos': [x for x in range(31, 41)], 'Specialties': [x for x in range(41, 61)],
                'Sides': [x for x in range(57, 84)], 'Desserts': [x for x in range(84, 89)],
                'Drinks': [x for x in range(89, 123)], 'Cravings Value Menu': [x for x in range(123, 128)],
                'Meatless': [x for x in range(128, 132)], 'Add-Ons': [x for x in range(132, 141)],
                'Single Portions': [x for x in range(141, 155)], 'Meals': [x for x in range(155, 350)]}
        for index, item in enumerate(items):
            name = item.xpath('.//a[@class = "nmItem"]/text()').get()
            kcal = item.xpath('.//td[@headers="inmGrid_c2"]/text()').get()
            kj = item.xpath('.//td[@headers="inmGrid_c1"]/text()').get()
            fat = str(item.xpath('.//td[@headers="inmGrid_c3"]/text()').get())
            sat_fat = item.xpath('.//td[@headers="inmGrid_c4"]/text()').get()
            carb = item.xpath('.//td[@headers="inmGrid_c5"]/text()').get()
            sugars = item.xpath('.//td[@headers="inmGrid_c6"]/text()').get()
            fibre = item.xpath('.//td[@headers="inmGrid_c7"]/text()').get()
            protein = item.xpath('.//td[@headers="inmGrid_c8"]/text()').get()
            salt = item.xpath('.//td[@headers="inmGrid_c9"]/text()').get()
            cat_name = [key for key, value in list.items() if index in value][0]
            item_dict = {
                'collection_date': date.today().strftime("%b-%d-%Y"),
                'rest_name': 'Taco Bell',
                'menu_section': cat_name,
                'item_name': name,
                'Energy (kj)': kj,
                'Energy (kcal)': kcal,
                'Total Fat (g)':fat,
                'Saturated Fat (g)':sat_fat,
                'Carbohydrates (g)': carb,
                'Sugars (g)': sugars,
                'Fibre (g)': fibre,
                'Protein (g)': protein,
                'Salt (g)': salt
            }
            item_dict.update(nutrient_dict)
            yield item_dict
