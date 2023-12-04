from datetime import date
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from browserPath import web_browser_path
from selenium.webdriver.chrome.service import Service
from time import sleep 


class A50CrusshSpider(scrapy.Spider):
    name = '50_Crussh'
    allowed_domains = ['crussh.com']
    start_urls = ['https://www.crussh.com/menu/']

    def __init__(self, *args, **kwargs):
        super(A50CrusshSpider, self).__init__(*args, **kwargs)
        # options = webdriver.ChromeOptions()
# options.headless = True  # turn on the headless mode!
        s = Service(web_browser_path)
        self.driver = webdriver.Chrome(service=s)

    def parse(self, response):
        cat_links = set(response.xpath('//a[contains(@href,"menu-category")]/@href').getall())
        for cat_link in cat_links:
            print(cat_link)
            yield scrapy.Request(url=cat_link, callback=self.parse_menu)
    
    def parse_menu(self,response):
        category = response.request.url.split('/')[-2]
        self.driver.get(response.url)
        sleep(10)
        html = self.driver.page_source
        sel = Selector(text=html)
        items = sel.xpath('//div[contains(@data-url, "menu-item/")]')
        for item in items:
            item_link = item.xpath('./@data-url').get()
            # print(item_link)
            yield scrapy.Request(url=item_link, callback=self.parse_item, meta = {'cat':category})

    def parse_item(self, response):
        item_name = response.xpath('//h1[@class="elementor-heading-title elementor-size-default"]/text()').get()
        item_description  = response.xpath('normalize-space(//div[@data-id="496f50a"]/div/text())').get()
        allergens = response.xpath('normalize-space(//h3[@class="elementor-icon-box-title"]/span/text())').get()
        ingredients = ''.join(response.xpath('//div[@data-id="58bb1f8"]/div/p//text()').getall())
        item_dict = {
            'rest_name': 'Crussh',
            'collection_date': date.today().strftime("%b-%d-%Y"),
            'menu_section': response.request.meta['cat'],
            'item_name': item_name, 
            'item_description': item_description, 
            'allergens':allergens,
            'ingredients': ingredients
        }
        nutrients = response.xpath('//table//div//text()').getall()
        my_dict = {}
        for i in range(0, len(nutrients), 3):
            key = nutrients[i]
            value = nutrients[i+2]
            my_dict[key] = value
            my_dict[key+'_100'] = nutrients[i+1]
        item_dict.update(my_dict)
        yield item_dict
        
    # def parse_item(self, response):
    #     items = response.xpath('//div[@class="item"]')
    #     for item in items:
    #         nutrition = item.xpath('./div[@class="data nutritionFacts"]')
    #         headers = nutrition.xpath('./table/thead/tr/th/text()').getall()
    #         rows = nutrition.xpath('./table/tbody/tr')
    #         nutrient_dict = {}
    #         for row in rows:
    #             nutrient = row.xpath('./td[1]/text()').get()
    #             for i in range(2, (len(headers) + 2)):
    #                 try:
    #                     value = row.xpath(f'./td[{i}]/text()').get().replace(',', '.')
    #                 except:
    #                     value = None
    #                 key = nutrient + '_' + headers[i - 2]
    #                 nutrient_dict.update({key: value})
    #         item_dict = {
    #             'rest_name': 'Crussh',
    #             'collection_date': date.today().strftime("%b-%d-%Y"),
    #             'menu_section': response.url.split('/')[-2],
    #             'item_name': item.xpath('./div[@class="header"]/h3/text()').get(),
    #             'item_description': item.xpath('./div[@class="header"]/p[@class="shortDescription"]/text()').get(),
    #             'price': item.xpath('./p[@class="price"]/text()').get(),
    #             'allergens': item.xpath('.//div[@class="data allergens"]/text()').get()
    #         }
    #         item_dict.update(nutrient_dict)
    #         yield item_dict
