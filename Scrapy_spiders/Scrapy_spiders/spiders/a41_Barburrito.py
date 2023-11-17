import scrapy
from datetime import date


class A41BarburritoSpider(scrapy.Spider):
    name = '41_Barburrito'
    allowed_domains = ['tkmenus.com']
    start_urls = ['https://tkmenus.com/barburrito']

    def parse(self, response):
        items = response.xpath('//div[@class="k10-byo-item__name-container"]')
        for item in items: 
            name = item.xpath('normalize-space(./span[@class="k10-byo-item__name-wrapper"]/text())').get()
            kcal = item.xpath('normalize-space(./span[@class="k10-byo-item__nutrient_energy"]/text())').get()
            yield{
                'rest_name': 'Barburrito',
                'collection_date': date.today().strftime("%b-%d-%Y"),
                'item_name': name, 
                'kcal': kcal
            }


