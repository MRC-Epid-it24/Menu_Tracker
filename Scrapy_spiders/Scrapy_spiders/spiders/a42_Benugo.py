import json
from datetime import date

import scrapy


def get_nutrient(nutrient_name, item):
    try:
        return item.get('nutrition').get(nutrient_name)
    except:
        return None


class A41BenugoSpider(scrapy.Spider):
    name = '42_Benugo'
    allowed_domains = ['www.benugo.com']
    start_urls = ['https://www.benugo.com/sites/cafes/benugo-st-pancras/']

    def parse(self, response):
        dat = response.xpath('//div[@class="product-menu-wrapper"]/script/text()').get()
        menus = json.loads(dat.split('`')[1]).get('Menus')
        # save all the json data 
        with open('Benugo.json', 'w') as f:
            json.dump(menus, f)
        for menu in menus: 
            menu_section = menu.get('Name')
            subsections = menu.get('Sections')
            for subsection in subsections: 
                section_name = subsection.get('Name')
                items = subsection.get('Recipes')
                for item in items: 
                    nutrients = item.get('Nutrs')
                    item_dict = {
                        'rest_name': 'Benugo Cafe',
                        'collection_date': date.today().strftime("%b-%d-%Y"),
                        'menu_section': menu_section + ',' + section_name,
                        'item_name': item.get('Name'),
                        'item_description': item.get('Desc'),
                        'servingsize': item.get('Sizes')[0].get('Size'),
                        'servingsizeunit': item.get('Sizes')[0].get('Uom1'),
                    }
                    for nutrient in nutrients: 
                        item_dict.update({
                            nutrient.get('Desc'): nutrient.get('PerServ'),
                            nutrient.get('Desc') + '_100': nutrient.get('Per100g')
                        })
                    yield item_dict

        # for menu_section in menu_sections[1:]:
        #     menu_section = json.loads(menu_section)
        #     menu_section_name = menu_section['name']
        #     sub_sections = menu_section['hasMenuSection']
        #     for sub_section in sub_sections:
        #         items = sub_section['hasMenuItem']
        #         sub_section_name = sub_section['name']
        #         for item in items:
        #             yield {
        #                 'rest_name': 'Benugo Cafe',
        #                 'collection_date': date.today().strftime("%b-%d-%Y"),
        #                 'menu_section': menu_section_name + ',' + sub_section_name,
        #                 'item_name': item.get('name'),
        #                 'item_description': item.get('description'),
        #                 'carb': get_nutrient('carbohydrateContent', item),
        #                 'kcal': get_nutrient('calories', item),
        #                 'protein': get_nutrient('proteinContent', item),
        #                 'satfat': get_nutrient('saturatedFatContent', item),
        #                 'sugar': get_nutrient('sugarContent', item),
        #                 'salt': get_nutrient('sodiumContent', item),
        #                 'vegetarian': item.get('suitableForDiet')
        #             }
