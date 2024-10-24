"""En este ejemplo extraeremos titulos y noticias con Scrapy para hacer el requerimiento
y Beautiful Soup para el parseo del arbol (HTML)"""
from scrapy.item import Item
from scrapy.item import Field
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
import json

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
        soup = BeautifulSoup(response.body, 'lxml') # al utilizar scrapy con BeautifulSouo se debe utilizar .body
        contenedor_noticias = soup.find_all("div", class_="chain-section")
        print(f"*******************{contenedor_noticias[0]}")
        for contenedor in contenedor_noticias:
            noticias = contenedor.find_all('div', class_='card | card-sm story flex flex-row space-x-2 items-center   py-2  w-full   ')
            for noticia in noticias:
                item = ItemLoader(Noticias(), response.body)

                titular = noticia.find('h2').text
                descripcion = noticia.find('p').text
                
            
                item.add_value('titular', titular) # En estos casos debo utilizar add_value
                item.add_value('descripcion', descripcion)

                yield item.load_item()



# 7. Ejecutar el codigo. En este caso: scrapy runspider 1_Una_pagina_estatica/5_scrapy_Noticias.py -o data_noticias.json:json