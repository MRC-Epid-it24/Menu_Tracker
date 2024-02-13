from datetime import date

import scrapy


class A85RealgreekSpider(scrapy.Spider):
    name = '85_RealGreek'
    allowed_domains = ['www.therealgreek.com']
    start_urls = ['https://www.therealgreek.com/menu/']

    def parse(self, response):
        categories = response.xpath('//h2[@class="h1 text-left scrl-mg-body"]')
        print(categories)
        for category in categories:
            cat_name = category.xpath('./text()').get()
            print('Cat name:',cat_name)
            if cat_name == 'Set Menus' or cat_name == 'Filoxenia Dinner Menu':
                continue
            # print(len(items))
            items = category.xpath(
                '(./parent::div/following-sibling::div[@class="col-sm-6 col-md-6 col-lg-6"])[1]/div/div')
            print(len(items))
            items.append(category.xpath(
                '(./parent::div/following-sibling::div[@class="col-sm-6 col-md-6 col-lg-6 scrl-mg-body"])/div/div'))
            print(len(items))
            if cat_name == 'SOUVLAKI WRAPS':
                items = [['Loukaniko Sausage with Aegean Slaw', '(741kcal)'],['Kalamari with Taramasalata and cucumber ribbons','(428kcal)'],['Pork with Tzatziki','(557kcal)'],['Chicken with Greek mustard sauce', '(751kcal)'],['Chicken with Tzatziki','(620kcal)'],['Lamb Meatballs with minted yoghurt','(559kcal)'],['Halloumi with minted yoghurt', '(714kcal)'],['Falafel with Tahini','(684kcal)'],['Vegan Meatballs with Vegan Aioli', '(673kcal)'],['Planted Vegan Chicken with vegan Tzatziki', '(863Kcal)']]
                for item in items:
                    item_name = item[0]
                    price = 8.25
                    dietary = item[1]
                    item_desc = 'Our gorgeous flatbread filled with chips, fresh tomatoes, red onion and sweet paprika. Please tell your server if you don’t want chips inside! *Kalamari option doesn’t include chips, tomato, onion or paprika.'
                    yield {
                        'collection_date': date.today().strftime("%b-%d-%Y"),
                        'rest_name': 'The Real Greek',
                        'menu_section': cat_name,
                        'item_name': item_name,
                        'price': f'{price:.2f}',
                        'item_description': item_desc,
                        'dietary': dietary,
                    }
                continue
            for item in items:
                item_name = item.xpath('.//h4[@class="the_dish_title"]/text()').get()
                if item_name is None:
                    item_name =item.xpath('.//h4[@class="the_dish_title "]/text()').get()
                if item_name is None:
                    continue

                item_desc = item.xpath('.//div[@class="the_dish_description"]/p/text()').get()
                dietary = item.xpath('normalize-space(.//div[@class="the_dietary_info"]/p/text())').get().replace('GF','').replace(
                    'V','').replace('VG','').replace('G','')

                if item_name == 'LUXURY SORBET':
                    item_desc = 'Lemon (261kcal) / Mango (283kcal)'
                    cals = [int(i.replace('(','').replace('kcal)','')) for i in item_desc.split(' ') if 'kcal' in i]
                    dietary = '(' + str(min(cals)) + '-' + str(max(cals)) + 'kcal)'

                if item_desc is None:
                    item_desc = item.xpath('.//h4[@class="column"]/text()').get()
                price = float(item.xpath('.//h4[@class="price"]/text()').get().strip('pp').strip('Â£'))

                yield {
                    'collection_date': date.today().strftime("%b-%d-%Y"),
                    'rest_name': 'The Real Greek',
                    'menu_section': cat_name,
                    'item_name': item_name,
                    'price': f'{price:.2f}',
                    'item_description': item_desc,
                    'dietary': dietary,
                }
            rhs_items = [['Cold Meze', 'Spicy Feta Dip (Htipiti)', 6.25,
                          'Roasted pepper and cheese dip, finished with a touch of chilli', '(571kcal)'],
                         ['Cold Meze', 'Melitzanosalata', 6.25,
                          'A light and fragrant blend of smoked aubergine, garlic, red onion, roasted red peppers and lemon.',
                          '(391kcal)'],
                         ['Hot Meze', 'Grilled Octopus with Fava', 9.65,
                          'Chargrilled Octopus, tossed in olive oil, garlic and Greek mountain oregano, served on a bed of Yellow Fava.',
                          '(202kcal)'],
                         ['Hot Meze', 'Chicken Monastiraki', 8.75,
                          'Chicken thigh, marinated with Greek herbs, served with tzatziki, onion and tomatoes.',
                          '(342kcal)'],
                         ['Hot Meze', 'BBC Chicken Wings', 7.85,
                          'Succulent chicken wings marinated in a smoked chilli relish.', '(458kcal)'],
                         ['Hot Meze', 'Chicken Skewer', 8.95,
                          'Chicken, skewered with onions and peppers. Served with Aegean Slaw.', '(260kcal)'],
                         ['Hot Meze', 'Lamb Meatballs', 9.00,
                          'Handmade lamb patties grilled and topped with Greek yoghurt, tomato sauce and onions.',
                          '(435kcal)'],
                         ['Hot Meze', 'Lamb Skewer', 9.25,
                          'Lamb, skewered with onions and peppers. Served with Aegean Slaw.', '(395kcal)'],
                         ['Hot Meze', 'Pork Skewer', 8.50,
                          'Pork, skewered with onions and peppers. Served with Aegean Slaw.', '(722kcal)'],
                         ['Hot Meze', 'LOUKANIKO — BEEF & PORK SAUSAGE SKEWER',7.95,
                          'Traditional Greek sausage from Thrace, chargrilled and served with Aegean Slaw.',
                          '(613kcal)'],
                         ['Hot Meze', 'GREEK MOUSSAKA', 9.50,
                          'A classic Greek dish – hearty and rich, with lamb mince. Served as a meze portion. Subject to availability.',
                          '(420kcal)'],
                         ['Sides & Salads', 'Aegean Slaw', 4.70,
                          'Thinly shredded cabbage, carrot, red and green peppers, with an olive oil dressing.',
                          '(240kcal)'],
                         ['Desserts', 'Luxury Ice-Cream', 4.25,
                          'Vanilla (419kcal) / Chocolate (433kcal) / Strawberry (312kcal) / Pistachio (413kcal)',
                          '(312-433kcal)'],
                         ['Desserts', 'Vegan Vanilla Ice-Cream', 4.25, '', '(525kcal)']
                         ]

            for item in rhs_items:
                if item[0] == cat_name:
                    item_name = item[1]
                    price = item[2]
                    item_desc = item[3]
                    dietary = item[4]
                    yield {
                        'collection_date': date.today().strftime("%b-%d-%Y"),
                        'rest_name': 'The Real Greek',
                        'menu_section': cat_name,
                        'item_name': item_name,
                        'price': f'{price:.2f}',
                        'item_description': item_desc,
                        'dietary': dietary,
                    }
            # for item in items_rhs:
            #     yield {
            #         'collection_date': date.today().strftime("%b-%d-%Y"),
            #         'rest_name': 'The Real Greek',
            #         'menu_section': cat_name,
            #         'item_name': item.xpath('.//h4[@class="the_dish_title "]/text()').get(),
            #         'price': item.xpath('.//h4[@class="price"]/text()').get(),
            #         'item_description': item.xpath('.//div[@class="the_dish_description"]/p/text()').get(),
            #         'dietary': item.xpath('normalize-space(.//div[@class="the_dietary_info"]/p/text())').get(),
            #     }
