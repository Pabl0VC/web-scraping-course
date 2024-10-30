"""
    - Otro ejemplo de la utilizacion de Scrapy
    - Uso de .get() y .getall() para obtener información de la página
ULTIMA VEZ EDITADO: 29 OCTUBRE 2024
"""
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess

class Articulo(Item):
    titulo = Field()
    citaciones = Field() 
    autores = Field()
    url = Field()

class GoogleScholar(CrawlSpider):
    name = 'googlescholar'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'DEPTH_LIMIT': 1, # Para definir que solo se vaya a un nivel de profundidad
        'FEED_EXPORT_FIELDS':['titulo', 'citaciones', 'autores', 'url'], # definimos el orden del csv
        'CONCURRENT_REQUESTS': 1, # Maneja las concurrencias, es decir, a cuantas paginas ingresa scrapy a la misma vez. Por defecto son 16. Bajar este numero protege de baneos
    }

    allowed_domains = ['scholar.google.com']

    start_urls = ['https://scholar.google.com/scholar?as_ylo=2023&q=AI&hl=en&as_sdt=0,5']

    download_delay = 2

    rules = (
        Rule( # Regla de movimiento VERTICAL hacia las citaciones de dicho articulo
            LinkExtractor(
                restrict_xpaths='.//div[@class="gs_fl gs_flb"]',
                allow=r'cites=' # "Si la URL contiene este patron, haz un requerimiento a esa URL"
            ), follow=True, callback="parse_start_url"),
    )

    # Para extraer informacion desde la url semilla debemos utilizar este nombre de la funion parse_start_url
    def parse_start_url(self, response): 
        sel = Selector(response)

        articulos = sel.xpath('.//div[@class="gs_ri"]')
        

        for articulo in articulos:
            item = ItemLoader(Articulo(), articulo)

            # Hacemos .getall() debido a que el texto del titulo puede venir dentro de varios tags dentro del <a>
            titulo = articulo.xpath('.//h3/a//text()').getall() # .getall() nos devuelve una lista de textos de todos los hijos; que podemos unir 
            titulo = "".join(titulo) 

            # Obtenemos la URL del articulo
            url = articulo.xpath('.//h3/a/@href').get() # extraemos el valor del atributo href. get() solo trae el primer resultado

            # Obtenemos los autores del articulo
            autores = articulo.xpath('.//div[@class="gs_a"]//text()').getall()
            autores = "".join(autores)
            autores = autores.split('-')[0].strip() # separa la cadena segun guines (-) y se queda solo con el primer elemento y limpia los espacios

            # Intentamos obtener el numero de citaciones (ya que no siempre existirá)
            # Por eso inicializamos el valor de la variable en 0 
            citaciones = 0
            try:
                citaciones = articulo.xpath('.//div[@class="gs_fl gs_flb"]/a[contains(@href, "cites")]/text()').get() # nos devuelve 'Cited by 23'
                citaciones = citaciones.replace('Cited by ', '') # Quitamos el 'Cited by ' para solo quedarnos con el numero
            except:
                pass #si es que no encuentra el xpath de citaciones no pasa nada y continua el codigo

            # En este caso utilizaremos add_value (tambien se puede con add_xpath. La ventaja es que con add_value podemos modificar directamente la extraccion)
            item.add_value('titulo', titulo)
            item.add_value('citaciones', citaciones)
            item.add_value('url', url)
            item.add_value('autores', autores)
            yield item.load_item()


process = CrawlerProcess({
    'FEED_FORMAT': 'csv',
    'FEED_URI':'data_GoogleScholar.csv',
    'FEED_EXPORT_ENCODING':'utf-8',
})

process.crawl(GoogleScholar)

process.start()