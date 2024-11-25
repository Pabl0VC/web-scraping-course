import os
import logging
import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

# Importar utils de forma dinámica
try:
    from .utils import abrir_pagina, configurar_driver, guardar_datos, cerrar_driver, cargar_configuracion # Ejecuta desde main.py
except ImportError:
    from utils import abrir_pagina, configurar_driver, guardar_datos, cerrar_driver , cargar_configuracion# Ejecucion desde scraper.py

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Trae la configuración desde el archivo JSON
config = cargar_configuracion('proyecto/config.json')

class OLXScraper:
    """CONSTANTES:
    Estas constantes representan configuraciones y selectores que no cambian durante la ejecución.
    """
    URL = config['OLX']['URL'] # URL de la página OLX que se usará para el scraping
    CARGAR_MAS_BTN_XPATH = config['OLX']['CARGAR_MAS_BTN_XPATH'] # XPath para el botón "Cargar más" en OLX (permite cargar más resultados)
    ITEM_PRODUCTO_XPATH = config['OLX']['ITEM_PRODUCTO_XPATH'] # XPath de cada elemento de producto en la lista de resultados
    BOTON_DISCLAIMER_XPATH = config['OLX']['BOTON_DISCLAIMER_XPATH'] # XPath para el botón Disclaimer (si aparece al cargar la página)
    PERFIL_CHROME = config['PERFIL_CHROME'] # Ruta del perfil de Chrome que Selenium utilizará
    USER_AGENT = config['USER_AGENT'] # Cadena del user-agent para emular un navegador específico
    OBJETIVO = config['OBJETIVO'] # Número objetivo de productos a cargar en la página
    MAX_INTENTOS = config['MAX_INTENTOS'] # Máximo número de intentos para hacer clic en "Cargar más" si no se alcanza el objetivo
    NOMBRE_ARCHIVO = config['NOMBRE_ARCHIVO'] # Nombre del archivo en el cual se guardarán los datos extraídos
    RUTA_GUARDADO = config['RUTA_GUARDADO'] # Ruta del directorio donde se guardarán los archivos con los datos extraídos
    FORMATO_GUARDADO = config['FORMATO_GUARDADO']  # Formato en el que se guardarán los datos (json, csv, py)

    def __init__(self):
        """CONSTRUCTOR
        Este método inicializa el driver de Selenium utilizando las configuraciones de PERFIL_CHROME 
        y USER_AGENT. Configurar el driver aquí permite reutilizar la misma instancia en todas las 
        funciones de la clase sin tener que reconfigurarlo. Además, se asegura de que el directorio de 
        guardado especificado en RUTA_GUARDADO exista, creándolo si es necesario.
        """
        self.driver = configurar_driver(self.PERFIL_CHROME, self.USER_AGENT) # Inicializa el driver de Selenium con el perfil de Chrome y el user-agent configurado
        logging.info("Driver de Selenium configurado.")
        
        # Crear el directorio de guardado si no existe
        os.makedirs(self.RUTA_GUARDADO, exist_ok=True)

    def cerrar_dialogo_consentimiento(self):
        """Intenta cerrar Disclaimer (si aparece)."""
        try:
            disclaimer_boton = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.BOTON_DISCLAIMER_XPATH))
            )
            disclaimer_boton.click()
            sleep(random.uniform(2, 5))
            logging.info("Disclaimer cerrado.")
        except TimeoutException:
            logging.warning("No se encontró Disclaimer.")
        except Exception as e:
            logging.error(f"Error al cerrar Disclaimer: {e}")

    def cargar_hasta_objetivo(self):
        """Hace clic en el botón 'Cargar más' hasta que se alcance el número de anuncios objetivo o el límite de intentos."""
        intentos = 0
        nAnunciosActuales = 0

        while nAnunciosActuales < self.OBJETIVO and intentos < self.MAX_INTENTOS:
            try:
                # Espera hasta 20 segundos para encontrar el boton "Cargar más" y hacer clic
                boton = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, self.CARGAR_MAS_BTN_XPATH))
                )
                sleep(2)
                ActionChains(self.driver).move_to_element(boton).perform() # Desplaza la vista hacia el botón para asegurarse de que esté visible
                sleep(2)
                boton.click() # click al boton

                # Incrementa el contador de intentos
                intentos += 1
                logging.info(f"Clic {intentos} realizado en el botón 'Cargar más'.")

                # Verificar cuántos elementos han sido cargados
                nAnunciosActuales = len(self.driver.find_elements(By.XPATH, self.ITEM_PRODUCTO_XPATH))
                logging.info(f"Elementos actuales cargados: {nAnunciosActuales}")

                if nAnunciosActuales >= self.OBJETIVO:
                    logging.info(f"Objetivo de {self.OBJETIVO} elementos alcanzado.")
                    break

                sleep(random.uniform(10, 15))

            except StaleElementReferenceException:
                # Se lanza cuando el elemento ya no es válido en el DOM, probablemente por un cambio en la página
                logging.warning("Referencia de elemento obsoleta. Intentando nuevamente.")
                continue # Reinicia el ciclo para intentar nuevamente
            except Exception as e:
                # Captura cualquier otro error que ocurra durante el clic en el botón
                logging.error(f"Error durante el clic en el botón 'Cargar más': {e}")
                break # Sale del ciclo en caso de un error inesperado

        if intentos == self.MAX_INTENTOS and nAnunciosActuales < self.OBJETIVO:
            logging.warning(f"Límite de {self.MAX_INTENTOS} intentos alcanzado sin cargar {self.OBJETIVO} elementos.")

        return nAnunciosActuales

    def extraer_datos_productos(self):
        """Extrae y retorna una lista de diccionarios con la información de cada producto."""
        productos = self.driver.find_elements(By.XPATH, self.ITEM_PRODUCTO_XPATH)
        logging.info(f"Total de productos encontrados: {len(productos)}")

        datos_productos = []
        for n, producto in enumerate(productos, start=1):
            # Inicializa los valores como "Sin información"
            nombre = "Sin información"
            precio = "Sin información"
            descripcion = "Sin información"
            localizacion = "Sin información"
            img = "Sin información"

            try:
                # Intenta extraer el precio del producto
                precio_element = producto.find_elements(By.XPATH, './/span[@data-aut-id="itemPrice"]')
                if precio_element:
                    precio = precio_element[0].text

                # Intenta extraer el nombre del producto
                nombre_element = producto.find_elements(By.XPATH, './/span[@data-aut-id="itemTitle"]')
                if nombre_element:
                    nombre = nombre_element[0].text

                # Intenta extraer la descripción del producto
                descripcion_element = producto.find_elements(By.XPATH, './/span[@data-aut-id="itemDetails"]')
                if descripcion_element:
                    descripcion = descripcion_element[0].text

                # Intenta extraer la localizacion del producto
                localizacion_element = producto.find_elements(By.XPATH, './/span[@data-aut-id="item-location"]')
                if localizacion_element:
                    localizacion = localizacion_element[0].text

                # Intenta extraer la imagen del producto
                img_element = producto.find_elements(By.XPATH, './/img')
                if img_element:
                    img = img_element[0].get_attribute("src") # get_attribute() para obtener el valor de un atributo
                
                # Registra información sobre el producto extraído en el log
                logging.info(f"Producto {n}: {nombre} - Precio: {precio} - Descripcion: {descripcion} - Localizacion: {localizacion} - Imagen: {img} \n")
            except Exception as e:
                # Si ocurre un error, registra una advertencia
                logging.warning(f"Producto {n} sin datos completos: {e}")

            # Agrega el producto a la lista de datos con la información extraída
            datos_productos.append({"nombre": nombre, "precio": precio, "descripcion": descripcion, "localizacion": localizacion, "imagen": img})

        return datos_productos

    def ejecutar(self):
        """Abre la página, cierra el Disclaimer, carga más anuncios hasta alcanzar el objetivo, extrae datos de productos y los guarda en el archivo especificado"""
        abrir_pagina(self.driver, self.URL)
        self.cerrar_dialogo_consentimiento()
        self.cargar_hasta_objetivo()
        productos = self.extraer_datos_productos()
        logging.info(f"Extracción completada. Total de productos: {len(productos)}")
        guardar_datos(productos, self.NOMBRE_ARCHIVO, self.RUTA_GUARDADO, self.FORMATO_GUARDADO)
        cerrar_driver(self.driver) 

# # Ejecuta el scraper si el archivo se ejecuta directamente
if __name__ == "__main__":
    scraper = OLXScraper()
    scraper.ejecutar()