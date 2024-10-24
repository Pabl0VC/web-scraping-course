"""En este ejemplo extraeremos titulos y descripcion con Scrapy de una pagina de noticias"""
from scrapy.item import Item
from scrapy.item import Field
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess

#PASOS OBLIGATORIOS
# 1. Definir abstraccion de items
class Noticias(Item):
    titular = Field()
    descripcion = Field()

# 2. Definir spider
class NoticiasSpider(Spider):
    name = "SpiderNoticias"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    start_urls = ['https://www.eluniverso.com/deportes/']

    # 3. Definir la funcion parse
    def parse(self, response):
        sel = Selector(response)
        # 4. Armar la logica para capturar la informacion
        noticias = sel.xpath('//div[contains(@class, "region region-content")]//ul[@class="feed | divide-y relative  "]//div[@class="card | card-sm story flex flex-row space-x-2 items-center   py-2  w-full   "]')
        for noticia in noticias:
            item = ItemLoader(Noticias(), noticia)
            # 5. Capturar los items
            item.add_xpath('titular', './/h2/a/text()')
            item.add_xpath('descripcion', './/p/text()')

            # 6. Yield de los items
            yield item.load_item()

# 7. Ejecutar el codigo. En este caso: scrapy runspider 1_Una_pagina_estatica/5_scrapy_Noticias.py -o data_noticias.json:json

# 8. Tambien podemos ejecutar utilizando las funciones CrawlerProcess() y crawl()
process = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI':'data_noticias.json'
})

process.crawl(NoticiasSpider)

process.start()