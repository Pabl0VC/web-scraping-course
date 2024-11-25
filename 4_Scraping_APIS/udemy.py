import os
import csv
import cloudscraper

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

# CONFIGURACION DE HEADERS
# Aqui ingresamos algunos "Requests Headers" del navegador para capturar correctamente la informacion de la api
headers = {
    # El encabezado de referer es importante. Sin esto, este API en especifico me respondera 403
    "Referer": "https://www.udemy.com/courses/search/?p=2&q=python&src=ukw",
    'Accept-Language': 'es-ES,es;q=0.9',
}
# Utilizamos cloudscraper debido al mecanismo anti detección de bots de Udemy
scraper = cloudscraper.create_scraper()

n_curso = 0
datos = []
for i in range(1,4): # Se itera cada pagina
    url_api = f'https://www.udemy.com/api-2.0/search-courses/?src=ukw&q=python&skip_price=true&p={str(i)}' # ingreso el numero de pagina
    response = scraper.get(url_api, headers=headers)
    print(response)

    data = response.json()
    #print(data)

    cursos = data["courses"]
    
    for i in cursos:
        n_curso += 1
        # Extraemos los datos y los almacenamos en el diccionario
        curso_data = {
        "CURSO": i['title'],
        "DESCRIPCION": i['headline'],
        "CALIFICACION": round(i['rating'], 2)
        }
        # Añadimos el diccionario a la lista de datos
        datos.append(curso_data)
        info(f"{n_curso}\nCURSO:{i['title']}\nDESCRIPCION: {i['headline']}\nCALIFICACION: {round(i['rating'],2)}")

#Guarda los datos en archivo CSV
ruta_csv = os.path.join('4_Scraping_APIS', "extraccion_api_Udemy.csv")
with open(ruta_csv, "w", newline='', encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["CURSO", "DESCRIPCION", "CALIFICACION"])
    writer.writeheader()
    writer.writerows(datos)
trace(f"Datos guardados en extraccion_api_Udemy.csv")