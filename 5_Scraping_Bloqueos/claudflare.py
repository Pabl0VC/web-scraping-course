"""La siguiente pagina no nos permite utilizar la libreria requests ya que nos devuelve el codigo 403.
En estos casos podemos utilizar la libreria cloudscraper que trabaja con muchos tipos de headers lo que permite pasa ciertos bloqueos"""

import cloudscraper  # Esta librería nos sirve cuando el requests es 403
from bs4 import BeautifulSoup 
import time
import random
import re
################################## CONFIGURACION LOGS #####################################
from colorama import Fore, Style, init
import logging  # Permite registrar mensajes para depuración y seguimiento del flujo del programa en tiempo real.

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
init(autoreset=True)
# Configuración básica del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Funciones para registrar mensajes con colores
def info(msg):
    logging.info(Fore.GREEN + msg + Style.RESET_ALL)

def warning(msg):
    logging.warning(Fore.YELLOW + msg + Style.RESET_ALL)

def error(msg):
    logging.error(Fore.RED + msg + Style.RESET_ALL)

def trace(msg):
    logging.info(Fore.BLUE + msg + Style.RESET_ALL)
############################################################################################

scraper = cloudscraper.create_scraper()  # Crea varios headers (no es necesario pasarle headers que ya que dentro tiene)
url_api = "https://www.zonaprop.com.ar/cocheras-alquiler-capital-federal.html"

intentos = 0
max_intentos = 5

while intentos < max_intentos:
    try:
        info(f"Intento {intentos + 1} de {max_intentos}...")
        response = scraper.get(url_api)

        # Si la respuesta tiene un código de estado 200, salimos del ciclo
        if response.status_code == 200:
            trace("Conexión exitosa.")
            break
        raise ValueError()
    except Exception:
        warning(f"Status Code: {response.status_code}")
        # Esperamos entre 1 y 3 segundos antes de reintentar
        time.sleep(random.uniform(1, 3))
        intentos += 1

# Si no se logró éxito después de los intentos, generamos un error
if intentos == max_intentos:
    raise RuntimeError("No se pudo obtener una respuesta exitosa después de varios intentos.")

# Si todo fue exitoso, continuar con el resto del código
#trace(f"Contenido de la respuesta: {response.text[:10000]}")  # Imprime los primeros 10000 caracteres
if response.status_code == 200:
    soup = BeautifulSoup(response.text, features='lxml')
    #print(soup)

    # Usamos una expresión regular para buscar las clases que comienzan con 'CardContainer'
    divs = soup.find_all('div', class_=re.compile('^CardContainer')) # ^CardContainer: El símbolo ^ indica que la clase debe comenzar con CardContainer. Todo esto es equivalente a //div[starts-with(@class, 'CardContainer')] en XPath.
    print(len(divs))
    time.sleep(random.uniform(1, 3))
    count = 0
    for i in divs:
        count +=1
        info(f"******************* {count} *******************")
        # Buscar la Calle
        calle = i.find('div', class_=re.compile('.*LocationAddress.*')) # Equivalente a ./div[contains(@class,'LocationAddress')]
        if calle:
            trace(f"Calle: {calle.get_text(strip=True)}")
        else:
            print("Calle no encontrada en este div.")

        # Buscar la Ciudad
        ciudad = i.find('h2', class_=re.compile('.*LocationLocation.*')) # Equivalente a ./h2[contains(@class,'LocationLocation')]
        if ciudad:
            trace(f"Ciudad: {ciudad.get_text(strip=True)}")
        else:
            error("Ciudad no encontrada")
        
        # Buscar Precio
        precio = i.find('div', class_=re.compile('^Price-')) # Equivalente a ./div[starts-with(@class,'Price-')]
        if precio:
            trace(f"Precio: {precio.get_text(strip=True)}")
        else:
            error("Precio no encontrado")

        # Buscar Descripcion
        descripcion = i.find('h3', class_=re.compile('^PostingDescription')) # Equivalente a ./h3[starts-with(@class,'PostingDescription')]//text()
        if descripcion:
            trace(f"Descripción: {descripcion.get_text(strip=True)}")
        else:
            error("Descripción no encontrada")
    
