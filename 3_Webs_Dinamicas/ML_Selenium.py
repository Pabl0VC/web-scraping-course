# Importaciones de bibliotecas estándar
import os  # Proporciona funciones para interactuar con el sistema operativo, como manejar rutas y archivos.
import logging  # Permite registrar mensajes para depuración y seguimiento del flujo del programa en tiempo real.
import random  # Proporciona funciones para generar números aleatorios.
from time import sleep  # Permite pausar la ejecución del programa durante un tiempo específico.

# Importaciones de la biblioteca Selenium
from selenium import webdriver  # Importa el módulo principal de Selenium para controlar navegadores.
from selenium.webdriver.chrome.options import Options  # Permite configurar opciones para el navegador Chrome.
from selenium.webdriver.common.by import By  # Proporciona métodos para localizar elementos en el DOM.
from selenium.webdriver.common.action_chains import ActionChains  # Permite realizar acciones complejas como movimientos del mouse.
from selenium.webdriver.support.ui import WebDriverWait  # Proporciona una espera explícita para elementos del DOM.
from selenium.webdriver.support import expected_conditions as EC  # Contiene condiciones comunes para esperar elementos.
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException  # Excepciones comunes para manejar errores en Selenium.

# Importaciones para la interfaz gráfica
import tkinter as tk  # Importa Tkinter para crear interfaces gráficas de usuario (GUIs).
from tkinter import messagebox  # Proporciona cuadros de mensaje para mostrar alertas al usuario.

# Importaciones para manejar formatos de datos
import json  # Permite trabajar con datos en formato JSON, facilitando la lectura y escritura.
import csv  # Proporciona funciones para leer y escribir archivos en formato CSV.

import re


# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MercadoLibreScraper:
    # Constantes de configuración
    PERFIL_CHROME = "3_Webs_Dinamicas/perfil_bot"
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    #URL = 'https://listado.mercadolibre.cl/bujias-mg3#D[A:bujias%20mg3]'
    URL = 'https://listado.mercadolibre.cl/closet-6-puertas#D[A:closet%206%20puertas]'
    NOMBRE_ARCHIVO = "Extraccion_ML_Selenium"
    RUTA_GUARDADO = "3_Webs_Dinamicas/resultados_ML_Selenium"

    def __init__(self):
        self.driver = self.configurar_driver()  # Inicializa el driver de Selenium, que permitirá realizar el web scraping y las interacciones automatizadas con la página web.
        logging.info("Driver de Selenium configurado.")

        # Crear el directorio de guardado si no existe
        os.makedirs(self.RUTA_GUARDADO, exist_ok=True)

    def configurar_driver(self):
        """Configura el driver de Selenium con opciones de usuario y maximización de pantalla."""
        opts = Options()
        opts.add_argument(f"user-agent={self.USER_AGENT}")
        opts.add_argument("--start-maximized") # Maximiza la ventana al abrir el navegador
        opts.add_argument(f"user-data-dir={self.PERFIL_CHROME}")
        #opts.add_argument("--headless") # Headless Mode: no abre el navegador. Mayor rapidez de procesos
        return webdriver.Chrome(options=opts)

    def abrir_pagina(self):
        """Abre la página principal y espera unos segundos."""
        self.driver.get(self.URL)
        sleep(random.uniform(5, 7))
        logging.info("Página cargada.")
    
    def cerrar_driver(self):
        """Cierra el driver de Selenium y finaliza la sesión."""
        if self.driver:
            self.driver.quit()
            logging.info("Driver de Selenium cerrado.")
    
    def disclaimer_cookies(self):
        try:
            disclaimer = self.driver.find_element(By.XPATH, '//button[@class="cookie-consent-banner-opt-out__action cookie-consent-banner-opt-out__action--primary cookie-consent-banner-opt-out__action--key-accept"]')
            disclaimer.click()
            print("Se hizo clic en cookies")
        except:
            print("No se encontró disclaimer")
    
    def captura_informacion(self):
        """Ingresa a cada anuncio y extrae informacion y pasa a siguiente pagina"""
        datos_productos = []
        paginacion = True
        while paginacion:
            """Captura todos los links de los productos"""
            productos_encontrados = self.driver.find_elements(By.XPATH, '//li/div[@class="ui-search-result__wrapper"]//h2/a')
            links_productos = []
            for producto in productos_encontrados:
                html = producto.get_attribute('outerHTML')
                link_encontrado = re.findall(r'href="([^"]+)"', html)
                links_productos.append(link_encontrado)

            """Ingresa a cada producto mediante su link y extrae informacion"""
            logging.info(f"Cantidad de productos encontrados: {len(links_productos)}")
            count = 0
            for i in links_productos:
                count +=1
                try:
                    sleep(2)
                    self.driver.get(i[0]) # Ingresa al anuncio
                    logging.info(f"Página del producto '{count}' cargada.")
                    
                    # Captura de información
                    producto = self.driver.find_element(By.XPATH,'//h1[@class]').text
                    precio = self.driver.find_element(By.XPATH,'//div[@class="ui-pdp-price__second-line"]//span[@data-testid="price-part"]//span[@class="andes-money-amount__fraction"]').text

                    # Agrega el producto a la lista de datos con la información extraída
                    datos_productos.append({"producto": producto, "precio": precio})

                    self.driver.back()
                    sleep(2)
                except:
                    print("No se pudo ingresar a la pagina del producto")

                if count == 3: # Detiene el flujo hasta el producto 3 (temporal)
                    break
                
            #Pasa a la siguiente pagina
            try:
                sleep(2)
                logging.info("Buscando boton 'Siguiente'")
                siguiente = self.driver.find_element(By.XPATH, '//a[@title="Siguiente"]')
                siguiente.click()
                logging.info("Pasa a la siguiente pagina")
            except:
                logging.info("Ya no existen más paginas")
                paginacion = False

        return datos_productos


    def guardar_datos_json(self, datos):
        """Guarda los datos en archivo JSON, utilizando la ruta y el nombre configurados."""
        ruta_json = os.path.join(self.RUTA_GUARDADO, f"{self.NOMBRE_ARCHIVO}.json")
        with open(ruta_json, "w", encoding="utf-8") as json_file:
            json.dump(datos, json_file, ensure_ascii=False, indent=4)
        logging.info(f"Datos guardados en {ruta_json}")
    
    def guardar_datos_csv(self, datos):
        """Guarda los datos en archivo CSV, utilizando la ruta y el nombre configurados."""
        ruta_csv = os.path.join(self.RUTA_GUARDADO, f"{self.NOMBRE_ARCHIVO}.csv")
        with open(ruta_csv, "w", newline='', encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["producto", "precio"])
            writer.writeheader()
            writer.writerows(datos)
        logging.info(f"Datos guardados en {ruta_csv}")


    def ejecutar(self):
        """Ejecuta el flujo completo de MercadoLibreScraper"""
        self.abrir_pagina()
        self.disclaimer_cookies()
        datos = self.captura_informacion()
        self.guardar_datos_json(datos)
        self.guardar_datos_csv(datos)
        logging.info(f"Extracción completada.")
        self.cerrar_driver()

# Ejecución principal
if __name__ == "__main__":
    scraper = MercadoLibreScraper()
    scraper.ejecutar()