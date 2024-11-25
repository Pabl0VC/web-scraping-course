from bs4 import BeautifulSoup
import json
import cloudscraper

url = 'https://footdistrict.com/adidas-originals-womens-japan-h-jp9933.html'

# Esta libreria se trabaja igual que requests
# response = requests.get(url_api, headers=headers)
scraper = cloudscraper.create_scraper()  # Crea varios headers
response = scraper.get(url)

print(response)
soup = BeautifulSoup(response.text, features="lxml")

# Las tallas cargan dinamicamente, e inicialmente se encuentran
# dentro de un JSON en el tag script
scripts = soup.find_all('script')
for script in scripts:
    contenido = script.contents
    if len(contenido) > 0:
        script = contenido[0]
        if "Talla" in script:
            texto_script = script
ini = texto_script.find('(') + 1 # Obtengo la posicion de mi cadena donde se encuentra el parentesis abierto
fin = texto_script.find(')') # Obtengo la posicion de mi cadena donde se encuentra el parentesis cerrado

objeto = texto_script[ini:fin] # Con las posiciones, puedo cortar la cadena. A esto se le llama slicing, o obtener un substring.

objeto = json.loads(objeto) # Cargo el json a un diccionario
# Sabiendo la estructura del diccionario lo recorro para obtener la informacion que quiero
tallas = objeto["[data-role=swatch-options]"]["Magento_Swatches/js/swatch-renderer"]["jsonConfig"]["attributes"]["134"]["options"]
for talla in tallas:
    if "No disponible" not in talla["label"]: # filtro las tallas que no estan disponibles
        print (talla["label"]) # Imprimo por pantalla