"""En esta seccion extraeremos informacion pero solo utilizando la libreria Scrapy para realizar el requerimiento y el parseo"""
from scrapy.item import Item
from scrapy.item import Field
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader


# 1. Primero hay que definir la clase de abstraccion de los items que se quieren extraer. En este caso son las preguntas (titulo y descripcion)
class Preguntas(Item):
    """En esta sección definimos la estructura de los datos que queremos extraer utilizando Scrapy. 
    Esto se hace creando una clase que hereda de `Item`, donde cada campo de información es representado por un `Field`."""
    pregunta = Field() # Este campo almacenará el título de la pregunta.
    descripcion = Field() # Este campo almacenará la descripción de la pregunta.
    

class StackOverflowSpide(Spider): # Spider se utiliza para la extraccion de una sola pagina
    name = "MiPrimerSpider" # se debe definir un nombre al spider
    custom_settings ={
        'USER-AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    }    #definir encabezados
    start_urls = ['https://stackoverflow.com/questions'] #definir url en una lista

    # 3. Definimos la funcion del parseo para realizar el requerimiento y trabajar los datos
    def parse(self, response): # con este response realizamos el requererimiento
        sel = Selector(response) # con este selector podemos hacer las consultas a la pagina
        preguntas = sel.xpath('//div[@id="questions"]//div[contains(@class,"s-post-summary ")]') # esto genera una lista con todos los divs con clase s-post-summary
        for i in preguntas:
            item = ItemLoader(Preguntas(), i)
            item.add_xpath('pregunta', './/h3/a/text()') # las capturas siempre comienzan con punto porque ahora no buscaremos en todo el html, solo será en lo que está dentro de preguntas en este caso
            item.add_xpath('descripcion', './/div[@class="s-post-summary--content-excerpt"]/text()')

            yield item.load_item() # esto manda a un archivo la informacion cargada de los items. Esto se hace porque scrapy tiene un marco de trabajo.

        