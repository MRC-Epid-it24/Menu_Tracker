from datetime import date

import scrapy


class A72TimhortonsSpider(scrapy.Spider):
    name = '72_TimHortons'
    allowed_domains = ['timhortons.co.uk']
    start_urls = ['https://timhortons.co.uk/menu']

    def parse(self, response):
        categories = response.xpath('//div[@class="menu-items box-grid small-up-2 medium-up-3 large-up-4"]')
        for category in categories:
            items = category.xpath('./a')
            cat_name = items[0].xpath('./div/@class').get().replace('anchor', '')
            for item in items:
                item_name = item.xpath('./p/text()').get()
                item_url = 'https://timhortons.co.uk/' + item.xpath('./@href').get()
                # id = item_url.replace('#', '')
                yield scrapy.Request(item_url, meta = {'menu_section': cat_name,'item_name': item_name}, callback=self.parse_item)

    def parse_item(self,response): 
                # modal = response.xpath(f'//div[@id="{id}"]')
                # vegetarian = modal.xpath('.//p[@class="calorie-disclaimer"]/text()').getall()
                # nutrition = modal.xpath('.//dl')
        nutrition = response.xpath('//div[@class="information_detail"]//table[1]//tr')
        servingsize = nutrition.xpath('.//th[contains("Serving Size", text())]/parent::tr/td/text()').get()
        item_dict = {
            'collection_date': date.today().strftime("%b-%d-%Y"),
            'rest_name': 'Tim Hortons',
            'menu_section': response.request.meta['menu_section'], 
            'menu_id': response.request.url.split('/')[-1],
            'item_name': response.request.meta['item_name'],
            'servingsize': servingsize,
        }
        for row in nutrition[2:]:
            header = row.xpath('.//th/text()').get()
            values = row.xpath('.//td/text()').getall()
            # fix a bug in the website cold brew item
            if len(values) == 2:
                item_dict.update({header + '_perserving': values[0], header + '_percent': values[1]})
            else:
                if len(values) == 1:
                    if '%' in values[0]:
                        item_dict.update({header + '_percent': values[0]})
                    else:
                        item_dict.update({header + '_perserving': values[0]})
        yield item_dict
