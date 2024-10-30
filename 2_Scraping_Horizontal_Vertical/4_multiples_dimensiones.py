"""
    - Extraer todas las opiniones de los usuarios que dejan reviews en hoteles de Santiago en Tripadvisor
    - Aprender a realizar extracciones de dos niveles de verticalidad y dos niveles de horizontalidad
    - Aprender a reducir el espectro de busqueda para filtrar URLs en las reglas
    - Evitar obtener URLs repetidas
ULTIMA VEZ EDITADO: 28 OCTUBRE 2024
"""
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose


class Opinion(Item):
    titulo = Field()
    calificacion = Field()
    contenido = Field()
    autor = Field()

class TripAdivisorCrawl(CrawlSpider): # Esta clase puede llevar cualquier nombre. Lo importante es llamar a la clase CrawlSpider
    name = "OpinionesTripAdvisor"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 50
}

    allowed_domains = ['tripadvisor.com']

    start_urls = ['https://www.tripadvisor.com/Hotels-g294305-Santiago_Santiago_Metropolitan_Region-Hotels.html']

    download_delay = 2

    # En este caso necesitamos 4 reglas para la extraccion
    rules = (
        Rule(
            LinkExtractor(  # PAGINACION DE HOTELES (HORIZONTALIDAD DE PRIMER NIVEL)
                allow=r'-oa'
            ), follow=True), # No tiene callback porque aun no voy a extraer datos de aqui. Solamente voy a seguir otras URLs.
        Rule(
            LinkExtractor(  # DETALLE DE HOTELES (VERTICALIDAD DE PRIMER NIVEL)
                allow=r'/Hotel_Review-',
                restrict_xpaths=['//div[@data-automation="hotel-card-title"]/a'] # Evita obtener URLs repetidas reduciendo el espectro de busqueda de las URLs a solamente un contenedor especifico dentro de un XPATH
            ), follow=True), # No tiene callback porque aun no voy a extraer datos de aqui. Solamente voy a seguir otras URLs.
        Rule(
            LinkExtractor(  # HORIZONTALIDAD DE OPINIONES DE UN HOTEL (HORIZONTALIDAD DE SEGUNDO NIVEL)
                allow=r'-or'
            ), follow=True), # No tiene callback porque aun no voy a extraer datos de aqui. Solamente voy a seguir otras URLs.
        Rule(
            LinkExtractor(  # DETALLE DE PERFIL DE USUARIO (VERTICALIDAD DE SEGUNDO NIVEL)
                allow=r'/Profile/',
                restrict_xpaths=['//div[@data-test-target="reviews-tab"]'] # Evita obtener URLs repetidas reduciendo el espectro de busqueda de las URLs a solamente un contenedor especifico dentro de un XPATH
            ), follow=True, callback='parseOpinion'), # Aqui si voy a utilizar el callback, debido a que en estas paginas es donde yo quiero extraer datos
    )

    def obtener_calificacion(self,texto):
        return int(texto.split('_')[-1]) / 10 # devuelve los valores en formato 4.5 o 5.0

    def parseOpinion(self, response):
        sel = Selector(response)
        autor = sel.xpath('//h1/span/text()').get() # como el autor es el mismo por cada iteracion solo necesitamos obtenerlo una vez.
            # Como en  este caso estamos obteniendo el texto a través del selector necesitamos utilizar la funcion get()
        
        contenedor_opiniones = sel.xpath('//div[@id="content"]/div/div')
        for opinion in contenedor_opiniones:
            item = ItemLoader(Opinion(), opinion)
            
            item.add_value('autor', autor) # aqui traemos el texto de autor extraido desde el selector
            item.add_xpath('titulo', './/div[@class="AzIrY b _a VrCoN"]/text()') # del las busquedas deben ser relativas (.//)
            
            # para las calificaciones el valor se tiene que obtener desde un atributo(class)
            # al final del xpath en vez de text() utilizamos @<atributo>
            # luego aplicamos una funcion para limpiar el resultado
            item.add_xpath('calificacion', './/a/div/span[contains(@class, "ui_bubble_rating")]/@class',MapCompose(self.obtener_calificacion))

            item.add_xpath('contenido', './/q/text()')
        
            yield item.load_item()


process = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI':'data_tripAdvidor.json',
    'FEED_EXPORT_ENCODING':'UTF-8',
})

process.crawl(TripAdivisorCrawl)

process.start()