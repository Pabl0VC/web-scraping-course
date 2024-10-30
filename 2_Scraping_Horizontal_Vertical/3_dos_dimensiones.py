"""
    - Extraer informacion sobre Articulos, Reviews y Videos en IGN.
    - Aprender a realizar extracciones de informacion de diferente tipo al mismo tiempo
    - Aprender a realizar extracciones verticales y horizontales utilizando reglas
    - Aprender a realizar extracciones con dos dimensiones de horizontalidad
ULTIMA VEZ EDITADO: 28 OCTUBRE 2024
"""
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess


# Como queremos extraer 3 tipos de informacion debemos crear una clase por cada uno
class Noticia(Item):
    titulo = Field()
    contenido = Field()

class Resena(Item):
    titulo= Field()
    calificacion = Field()

class Video(Item):
    titulo = Field()
    fecha_publicacion = Field()


class IgnCrawler(CrawlSpider): # Esta clase puede llevar cualquier nombre. Lo importante es llamar a la clase CrawlSpider
    name = "Videojuegos"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 5
}
    
    allowed_domains = ['latam.ign.com']

    start_urls = ['https://latam.ign.com/se/?model=&q=ps5']

    download_delay = 2

    rules = ( # En este caso debemos hacer 5 reglas

        # HORIZONTALIDAD POR TIPO DE INFORMACION (Noticia, Resena, Video) => No tiene callback ya que aqui no voy a extraer datos
        Rule(
            LinkExtractor ( # esta clase permite ingresar a los sublinks
                allow = r'type=', # los links de las secciones tienen este patron
            ),
            follow = True,
        ),
        
        # HORIZONTALIDAD DE PAGINACION EN CADA TIPO => No tiene callback ya que aqui no voy a extraer datos
        Rule(
            LinkExtractor(
                allow = r'&page=\d+', #al cambiar de pagina se añade este patron en los links
            ),
            follow = True,
        ),

        # REGLAS VERTICALES (EXTRACCION)
        # Una regla por cada tipo de contenido donde ire verticalmente
        # Cada una tiene su propia funcion parse que extraera los items dependiendo de la estructura del HTML donde esta cada tipo de item
        Rule( # VERTICALIDAD DE NOTICIAS
            LinkExtractor(
                allow = r'/news/',
            ),
            follow=True,
            callback = 'parseNoticias',
        ),
        Rule( # VERTICALIDAD DE RESEÑAS
            LinkExtractor(
                allow = r'/review/',
            ),
            follow=True,
            callback = 'parseResenas',
        ),
        Rule( # VERTICALIDAD DE VIDEOS
            LinkExtractor(
                allow = r'/video/',
            ),
            follow=True,
            callback = 'parseVideos',
        ),
    )

    def parseNoticias(self, response):
        item = ItemLoader(Noticia(), response)

        item.add_xpath('titulo', '//h1[@id ="id_title"]/text()')
        item.add_xpath('contenido', '//div[@id ="id_text"]//*/text()') # //*/text(): trae el texto de todos los hijos con cualquier etiqueta

        yield item.load_item()

    def parseResenas(self, response):
        item = ItemLoader(Resena(), response)

        item.add_xpath('titulo', '//div[@class="article-headline"]/h1/text()')
        item.add_xpath('calificacion', '//div[@class="review"]//span[@class="side-wrapper side-wrapper hexagon-content"]/div/text()')

        yield item.load_item()

    def parseVideos(self, response):
        item = ItemLoader(Video(), response)

        item.add_xpath('titulo', '//h1/text()')
        item.add_xpath('fecha_publicacion', '//span[@class="publish-date"]/text()')

        yield item.load_item()


process = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI':'data_IGN.json',
})

process.crawl(IgnCrawler)

process.start()