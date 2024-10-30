"""En este ejemplo extraeremos solo verticalmente el nombre, puntuacion, descripcion y facilidades
de los hoteles que aparecen en la primera pagina de una busqueda en TripAdvisor"""
from typing import Any
from scrapy.http import Response
from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose # MapCompose sirve para pre-procesar datos extraidos del html, antes de guardarlos en el archivo
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess

class Hotel(Item):
    nombre = Field()
    puntuacion = Field()
    descripcion = Field()
    facilidades = Field()

class TripAdvisor(CrawlSpider):# Cuando queremos hacer un scraping vertical y/u horizontal heredamos la clase CrawlSpider
    name = "Hoteles"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 2
}
    start_urls = ['https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html'] # Desde aqui se va a ingresar a cada sublink que corresponde a cada hotel

    download_delay = 2 # Se utiliza para evitar baneos. Realiza un tiempo de espera (en segundos) entre cada requerimiento que scrapy haga a cada pagina a partir de la ruta semilla.
    
    # Orquestador de CrawSpider: Son reglas que definen a cuales sublinks de la URL semilla el spider tiene o no que ir en busqueda de informacion.
    # Para escribir las reglas debemos encontrar un patron para ingresar a los sublinks
    rules = (
        Rule(
            LinkExtractor ( # esta clase permite ingresar a los sublinks
                allow = r'/Hotel_Review-g303845-', # mediante regex indicamos el patron que encotramos en los sublinks que queremos ir
            ),
            follow = True, # indico si quiero seguir (True) o no (False) el patron indicado
            callback = "parse_hotel" # aqui ingresamos el nombre de la funcion que queremos utilizar al ingresar en los sublinks
        ), # Importante esta coma para que funcione la clase Rule
    )
    # Desde aqui hacia abajo estamos ingresando a cada sublink para capturar la informacion
    def parse_hotel(self, response): # la funcion puede tener cualquier nombre pero debe ser el mismo del callback
        sel = Selector(response) # Capturamos todo el arbol del la pagina del hotel (sublink)
        item = ItemLoader(Hotel(), sel) # Por cada pagina es solo un hotel por lo que no iteramos y trabajamos con todo el arbol de la pagina

        item.add_xpath('nombre', '//h1[@id="HEADING"]/text()')
        item.add_xpath('puntuacion', '//span[@class="kJyXc P"]/text()')
        item.add_xpath('descripcion', '//div[@id="ABOUT_TAB"]//div[@class="fIrGe _T"]//text()', # //text() nos permite obtener el texto de todos los hijos
                        MapCompose(lambda i:i.replace('\n', '').replace('\r', ''))) # Es posible utilizar Map Compose con funciones anonimas o haciendo la funcion por fuera de la funcion y llamandola aquí
        item.add_xpath('facilidades', '//div[@data-test-target="amenity_text"]/text()')

        yield item.load_item()

#scrapy runspider 2_Scraping_Horizontal_Vertical/1_Vertical_extraction.py -o data_hoteles.json:json


process = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI':'data_hoteles.json'
})

process.crawl(TripAdvisor)

process.start()
