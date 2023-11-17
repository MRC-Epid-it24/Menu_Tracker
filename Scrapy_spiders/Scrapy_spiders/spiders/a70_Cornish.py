# import re
from datetime import date
import scrapy
import urllib.parse
import re


class A70CornishSpider(scrapy.Spider):
    name = '70_Cornish'
    allowed_domains = ['thecornishbakery.com']
    start_urls = ['https://thecornishbakery.com/pages/allergens']

    def parse(self, response):
        sections = response.xpath('//section[@class="section-faq accordion"]')
        for section in sections:
            section_name = section.xpath('./h2/text()').get()
            items = section.xpath('.//div[@class="faq-list__item-content"]/p')
            for item in items: 
                item_name = item.xpath('./strong/text()').get()
                if item_name !='\xa0':
                    description = ','.join(item.xpath('./text()').getall())
                    try: 
                        kcal = re.search(pattern='[0-9]+kcal', string = description).group(0)
                    except: 
                        kcal = None
                    yield{
                        'collection_date': date.today().strftime("%b-%d-%Y"),
                        'rest_name': 'The Cornish Bakery',
                        'item_name': item_name,
                        'menu_section': section_name,
                        'item_description': description,
                        'kcal': kcal
                    }

    # def parse_item(self, response):
    #     # nutrition = response.xpath('//table/tbody/tr')
    #     # nutrition_dict = {}
    #     # for row in nutrition:
    #     #     values = row.xpath('./td/text()').getall()
    #     #     nutrition_dict.update({values[0]+'_100':values[1],
    #     #                            values[0]+'_perserving': values[2]})
    #     ingredients = response.xpath('(//span[@class="metafield-multi_line_text_field"])[1]/text()').getall()
    #     allergens = [allergen for allergen in ingredients if 'Allergens:' in allergen][0]
    #     item_dict = {
    #         'collection_date': date.today().strftime("%b-%d-%Y"),
    #         'rest_name': 'The Cornish Bakery',
    #         'item_name': response.xpath('normalize-space(//h1[@class="product__title"]/text())').get(),
    #         'item_description': ''.join(
    #             response.xpath('//div[@class="product-description rte"]//span/text()').getall()),
    #         'price': response.xpath('normalize-space(//div[@class="product__price"]/span/text())').get(),
    #         'ingredients': ''.join(ingredients),
    #         'allergens': allergens,
    #         # 'servingsize':  re.compile('\d+').search(response.xpath('(//th[@scope="col"])[3]/p[1]/text()').get()).group(0),
    #         # 'nutrition_url': 'https:'+ response.xpath('//div[@class="image__fill fade-in-image"]/@style').get().split('url(')[1].replace(');',''),
    #         'product_url': response.url
    #     }
    #     # item_dict.update(nutrition_dict)
    #     yield item_dict



# for the ones with the custom builder -> small batch of code to download the data for individual pastries 

# builder_url = 'https://thecornishbakery.com/apps/builder?b=nhNf7NXilUGOQUGzaCeS7tL1'
# urls = response.xpath('//div[@class="bxp-owl-item"]//a/@title-strip').getall()
# urls = list(set(urls))
# for url in urls: 
#     content = urllib.parse.unquote(url)
#     content_page = scrapy.Selector(text = content)

