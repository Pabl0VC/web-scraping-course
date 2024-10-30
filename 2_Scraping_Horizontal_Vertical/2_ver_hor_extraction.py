"""OBJETIVO: 
    - Extraer informacion sobre los productos en la pagina de Mercado Libre Mascotas
    - Realizar extracciones verticales y horizontales utilizando reglas
ULTIMA VEZ EDITADO: 25 OCTUBRE 2024
"""
from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess

class Articulo(Item):
    titulo = Field()
    precio = Field()
    descripcion = Field()

class MercadoLibreCrawler(CrawlSpider):
    name = "ArticulosML"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 5 # indica el numero de subpaginas que buscará por cada paginacion
}
    
    allowed_domains = ['listado.mercadolibre.cl', 'mercadolibre.cl','articulo.mercadolibre.cl']    # ingresar patrones de dominios para restringir las busquedas

    start_urls = ['https://listado.mercadolibre.cl/mascotas-perros']

    download_delay = 2

    rules = (   # como vamos a trabajar de manera horizontal y vertical necesitamos a lo menos dos reglas

        #Paginacion (horizontal)
        Rule(
            LinkExtractor ( # esta clase permite ingresar a los sublinks
                allow = r'_Desde_',
            ),
            follow = True,
            # Aqui no ponemos callback porque aqui no queremos extraer datos
        ), # Importante esta coma
        
        # Detalle de los productos (vertical)
        Rule(
            LinkExtractor(
                allow = r'/MLC',
            ),
            follow = True,
            callback = "parse_mercadoLibre", # este parametro solo lo definimos en las reglas que llevan a la pagina de extraccion
        ), # Importante esta coma
    )

    def limpiar_texto(self,texto:str):
        nuevo_texto = texto.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').strip()
        return nuevo_texto


    # Desde aqui hacia abajo estamos ingresando a cada sublink para capturar la informacion
    def parse_mercadoLibre(self, response):
        sel = Selector(response)
        item = ItemLoader(Articulo(), sel)

        item.add_xpath('titulo', '//h1/text()',MapCompose(self.limpiar_texto))
        item.add_xpath('precio', '//div[@class="ui-pdp-price__second-line"]//span[@style="font-size:36px"]//span[@class="andes-money-amount__fraction"]/text()')
        item.add_xpath('descripcion', '//p[@class="ui-pdp-description__content"]/text()',MapCompose(self.limpiar_texto))
        

        yield item.load_item()


process = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI':'data_ML.json',
})

process.crawl(MercadoLibreCrawler)

process.start()