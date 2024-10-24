import requests # realiza los requerimientos http para extraer el HTML
from lxml import html # permite parsear(analizar) el HTML y luego extraer la data

# Encabezados que se enviarán con la solicitud
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# URL de la página objetivo
url = 'https://www.wikipedia.org/'

# Solicitud GET al servidor
response = requests.get(url, headers=headers)
print(response) # <Response [200]>

print(response.text) # Devuelve todo el HTML de la pagina

# Se 'parsea' el HTML recibido
parser = html.fromstring(response.text)

# Imprimimos el parseador para ver su estructura
print(parser) # <Element html at 0x1028e67a0>

# Con el parseador ya podemos comenzar a extraer datos


# Extraccion desde id con funciones de la libreria lxml
ingles = parser.get_element_by_id("js-link-box-en") # <Element a at 0x102396a20>
print (ingles.text_content()) # English 6,895,000+ articles


# Podemos capturar informacion mas precisa con XPaths
# xpath() devuelve una lista de elementos, incluso si solo encuentra un elemento.
english = parser.xpath("//a[@id='js-link-box-en']/small/text()")  # con text() traemos solo el valor del elemento
print(english)

# Capturar todos los idiomas con xpaths
all_languages = parser.xpath("//div[contains(@class, 'central-featured-lang')]//strong/text()")
print(all_languages) # ['English', 'æ\x97¥æ\x9c¬èª\x9e', 'Ð\xa0Ñ\x83Ñ\x81Ñ\x81ÐºÐ¸Ð¹', 'EspaÃ±ol', 'Deutsch', 'FranÃ§ais', 'ä¸\xadæ\x96\x87', 'Italiano', 'PortuguÃªs']

# Capturar todos los idiomas con lxml
languages = parser.find_class('central-featured-lang') # trae todos los elementos con la clase 'central-featured-lang'
print(languages) # [<Element div at 0x10577aa70>, <Element div at 0x10577aac0>, <Element div at 0x10577af20>, <Element div at 0x10577af70>, <Element div at 0x10577afc0>, <Element div at 0x10577b010>, <Element div at 0x10577b060>, <Element div at 0x10577b0b0>, <Element div at 0x10577b100>, <Element div at 0x10577b150>]
# itera cada elemento y podemos utilizar text_content() para ver su contenido
for i in languages:
    print(i.text_content())
