# Importaciones de bibliotecas estándar
import os 
import random
from time import sleep 

# Importaciones de la biblioteca Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

# Configuración del logging avanzados
from modules.print_advanced import info, trace, warning, error, infoL, traceL, warningL, errorL

import requests
from PIL import Image # Procesa las imagenes para poder descargarlas
import io

class OLXScraper:
    # Constantes de configuración
    PERFIL_CHROME = "3_Webs_Dinamicas/perfil_bot"
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    URL = 'https://www.olx.in/'
    CARGAR_MAS_BTN_XPATH = '//button[@data-aut-id="btnLoadMore"]'
    ITEM_PRODUCTO_XPATH = '//li[@data-aut-id="itemBox3"]'
    BOTON_DISCLAIMER_XPATH = '//button[@class="fc-button fc-cta-consent fc-primary-button"]'
    # Configurables
    OBJETIVO = 20 # Número objetivo de anuncios a cargar
    MAX_INTENTOS = 10
    NOMBRE_ARCHIVO = "Extraccion_OLX"
    RUTA_GUARDADO = "6_Extras/Images_OLX"

    def __init__(self, objetivo=OBJETIVO, max_intentos=MAX_INTENTOS, nombre_archivo=NOMBRE_ARCHIVO, ruta_guardado=RUTA_GUARDADO):
        self.objetivo = objetivo
        self.max_intentos = max_intentos
        self.nombre_archivo = nombre_archivo
        self.ruta_guardado = ruta_guardado
        self.driver = self.configurar_driver()
        infoL("Driver de Selenium configurado.")

        # Crear el directorio de guardado si no existe
        os.makedirs(self.ruta_guardado, exist_ok=True)

    def configurar_driver(self):
        """Configura el driver de Selenium con opciones de usuario y maximización de pantalla."""
        opts = Options()
        opts.add_argument(f"user-agent={self.USER_AGENT}")
        opts.add_argument("--start-maximized")
        opts.add_argument(f"user-data-dir={self.PERFIL_CHROME}")
        opts.add_argument("--headless") # Headless Mode: no abre el navegador. Mayor rapidez de procesos
        return webdriver.Chrome(options=opts)

    def abrir_pagina(self):
        """Abre la página principal y espera unos segundos."""
        self.driver.get(self.URL)
        sleep(random.uniform(5, 7))
        info("Página cargada.")

    def cerrar_dialogo_consentimiento(self):
        """Intenta cerrar Disclaimer (si aparece)."""
        try:
            disclaimer_boton = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.BOTON_DISCLAIMER_XPATH))
            )
            disclaimer_boton.click()
            sleep(random.uniform(2, 5))
            info("Disclaimer cerrado.")
        except TimeoutException:
            warningL("No se encontró Disclaimer.")
        except Exception as e:
            error(f"Error al cerrar Disclaimer: {e}")

    def cargar_hasta_objetivo(self):
        """Hace clic en el botón 'Cargar más' hasta que se alcance el número de anuncios objetivo o el límite de intentos."""
        intentos = 0
        nAnunciosActuales = 0

        while nAnunciosActuales < self.objetivo and intentos < self.max_intentos:
            try:
                boton = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, self.CARGAR_MAS_BTN_XPATH))
                )
                sleep(2)
                ActionChains(self.driver).move_to_element(boton).perform()
                sleep(2)
                boton.click() # click al boton

                # Incrementa el contador de intentos
                intentos += 1
                trace(f"Clic {intentos} realizado en el botón 'Cargar más'.")

                # Verificar cuántos elementos han sido cargados
                nAnunciosActuales = len(self.driver.find_elements(By.XPATH, self.ITEM_PRODUCTO_XPATH))
                trace(f"Elementos actuales cargados: {nAnunciosActuales}")

                if nAnunciosActuales >= self.objetivo:
                    trace(f"Objetivo de {self.objetivo} elementos alcanzado.")
                    break

                sleep(random.uniform(10, 15))

            except StaleElementReferenceException:
                # Botón no es válido en el DOM, probablemente por un cambio en la página
                warning("Referencia de Botón obsoleta. Intentando nuevamente.")
                continue # Reinicia el ciclo para intentar nuevamente
            except Exception as e:
                # Captura cualquier otro error que ocurra durante el clic en el botón
                error(f"Error durante el clic en el botón 'Cargar más': {e}")
                break

        if intentos == self.max_intentos and nAnunciosActuales < self.objetivo:
            warning(f"Límite de {self.max_intentos} intentos alcanzado sin cargar {self.objetivo} elementos.")

        return nAnunciosActuales

    def extraer_datos_productos(self):
        """Extrae y retorna una lista de diccionarios con la información de cada producto."""
        productos = self.driver.find_elements(By.XPATH, self.ITEM_PRODUCTO_XPATH)
        trace(f"Total de productos encontrados: {len(productos)}")

        datos_productos = []
        for n, producto in enumerate(productos, start=1):
            nombre = "Sin información"
            img = "Sin información"

            try:
                # Nombre del producto
                nombre_element = producto.find_elements(By.XPATH, './/span[@data-aut-id="itemTitle"]')
                if nombre_element:
                    nombre = nombre_element[0].text

                # Intenta extraer la imagen del producto
                img_element = producto.find_elements(By.XPATH, './/img')
                if img_element:
                    img = img_element[0].get_attribute("src") # get_attribute() para obtener el valor de un atributo
                
                # Registra información sobre el producto extraído en el log
                info(f"""
                    Producto {n}: {nombre}
                    Imagen: {img}""")
            except Exception as e:
                # Si ocurre un error, registra una advertencia
                warning(f"Producto {n} sin datos completos: {e}")

            # Agrega el producto a la lista de datos con la información extraída
            datos_productos.append({"nombre": nombre, "imagen": img})

        return datos_productos


    def descargar_imagenes(self, datos):
        """Descarga las imagenes de los productos"""
        # Crear carpeta para guardar las imágenes
        output_dir = "6_Extras/Images_OLX"
        os.makedirs(output_dir, exist_ok=True)

        headers = {
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                }

        count = 0
        traceL(datos)
        info(datos)

        # Descargar imágenes
        for d in datos:
            count+=1
            trace(count)
            url_img = d['imagen']
            nombre = d['nombre']
            info(f"Procesando: {nombre}")

            # Verificar si la imagen es válida
            if url_img != "Sin información":
                try:
                    # Descargar la imagen
                    sleep(random.uniform(1, 3))
                    response = requests.get(url_img, headers=headers)
                    response.raise_for_status() # Verifica si la solicitud fue exitosa. Si no (por ejemplo, 404 o 500), lanza una excepción HTTPError.

                    # Abrir y procesar la imagen
                    image = Image.open(io.BytesIO(response.content)).convert('RGB') # Convierte los bytes descargados (`response.content`) en un objeto de imagen usando Pillow.
                    """
                    La respuesta (response.content) contiene los datos binarios de la imagen descargada
                    io.BytesIO crea un flujo de datos en memoria a partir de estos bytes.
                    Image.open() usa este flujo para crear un objeto de imagen que puede manipularse con la biblioteca Pillow.
                    .convert('RGB') Convierte la imagen a RGB para asegurar compatibilidad, especialmente al guardar en formatos como JPEG que no admiten transparencia ni otros modos de color.
                    """
                    file_name = f"{nombre.replace(' ', '_')}.jpg"
                    file_path = os.path.join(output_dir, file_name)

                    # Guardar la imagen
                    image.save(file_path)
                    info(f"Imagen guardada en: {file_path}")

                except Exception as e:
                    error(f"Error al descargar/guardar la imagen {nombre}: {e}")
            else:
                warning(f"No hay información de imagen para: {nombre}")

        trace(f"Todas las imágenes se han procesado. Revisa la carpeta: '{output_dir}'")


    def cerrar_driver(self):
        """Cierra el driver de Selenium y finaliza la sesión."""
        if self.driver:
            self.driver.quit()
            traceL("Driver de Selenium cerrado.")

    def ejecutar(self):
        """Ejecuta el flujo completo de scraping en OLX."""
        self.abrir_pagina()
        self.cerrar_dialogo_consentimiento()
        self.cargar_hasta_objetivo()
        productos = self.extraer_datos_productos()
        self.descargar_imagenes(productos)
        trace(f"Extracción completada. Total de productos: {len(productos)}")
        self.cerrar_driver()

# Ejecución principal
if __name__ == "__main__":
    scraper = OLXScraper()
    scraper.ejecutar()
