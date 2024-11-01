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


# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OLXScraper:
    # Constantes de configuración
    PERFIL_CHROME = "./3_Webs_Dinamicas/perfil_bot"
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    URL = 'https://www.olx.in/'
    CARGAR_MAS_BTN_XPATH = '//button[@data-aut-id="btnLoadMore"]'
    ITEM_PRODUCTO_XPATH = '//li[@data-aut-id="itemBox3"]'
    BOTON_DISCLAIMER_XPATH = '//button[@class="fc-button fc-cta-consent fc-primary-button"]'
    # Configurables
    OBJETIVO = 100 #Número objetivo de anuncios a cargar
    MAX_INTENTOS = 10
    NOMBRE_ARCHIVO = "Extraccion_OLX"
    RUTA_GUARDADO = "3_Webs_Dinamicas/datos_OLX"

    def __init__(self, objetivo=OBJETIVO, max_intentos=MAX_INTENTOS, nombre_archivo=NOMBRE_ARCHIVO, ruta_guardado=RUTA_GUARDADO):
        """
        Inicializa una instancia de OLXScraper.
        :param objetivo: Número objetivo de anuncios a cargar.
        :param max_intentos: Número máximo de intentos para cargar más anuncios.
        :param nombre_archivo: Nombre del archivo donde se guardarán los datos.
        :param ruta_guardado: Ruta donde se guardarán los datos.
        """
        self.objetivo = objetivo
        self.max_intentos = max_intentos
        self.nombre_archivo = nombre_archivo
        self.ruta_guardado = ruta_guardado
        self.driver = self.configurar_driver()  # Inicializa el driver de Selenium, que permitirá realizar el web scraping y las interacciones automatizadas con la página web.
        logging.info("Driver de Selenium configurado.")

        # Crear el directorio de guardado si no existe
        os.makedirs(self.ruta_guardado, exist_ok=True)

    def configurar_driver(self):
        """Configura el driver de Selenium con opciones de usuario y maximización de pantalla."""
        opts = Options()
        opts.add_argument(f"user-agent={self.USER_AGENT}")
        opts.add_argument("--start-maximized") # Maximiza la ventana al abrir el navegador
        opts.add_argument(f"user-data-dir={self.PERFIL_CHROME}")
        #opts.add_argument("--headless") # Headless Mode: no abre el navegador. Mayor rapidez de procesos
        return webdriver.Chrome(options=opts)

    def mostrar_alerta(self, mensaje):
        """Muestra una alerta en pantalla (opcional)"""
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Alerta", mensaje)
        root.destroy()

    def abrir_pagina(self):
        """Abre la página principal y espera unos segundos."""
        self.driver.get(self.URL)
        sleep(random.uniform(5, 7))
        logging.info("Página cargada.")

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

        while nAnunciosActuales < self.objetivo and intentos < self.max_intentos:
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

                if nAnunciosActuales >= self.objetivo:
                    logging.info(f"Objetivo de {self.objetivo} elementos alcanzado.")
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

        if intentos == self.max_intentos and nAnunciosActuales < self.objetivo:
            logging.warning(f"Límite de {self.max_intentos} intentos alcanzado sin cargar {self.objetivo} elementos.")

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
                logging.info(f"Producto {n}: {nombre} - Precio: {precio} - Descripcion: {descripcion} - Localizacion: {localizacion} - Imagen: {img}")
            except Exception as e:
                # Si ocurre un error, registra una advertencia
                logging.warning(f"Producto {n} sin datos completos: {e}")

            # Agrega el producto a la lista de datos con la información extraída
            datos_productos.append({"nombre": nombre, "precio": precio, "descripcion": descripcion, "localizacion": localizacion, "imagen": img})

        return datos_productos


    def guardar_datos(self, datos):
        """Guarda los datos en JSON, CSV, y como archivo Python, utilizando la ruta y el nombre configurados."""
        ruta_json = os.path.join(self.ruta_guardado, f"{self.nombre_archivo}.json")
        with open(ruta_json, "w", encoding="utf-8") as json_file:
            json.dump(datos, json_file, ensure_ascii=False, indent=4)
        logging.info(f"Datos guardados en {ruta_json}")

        ruta_csv = os.path.join(self.ruta_guardado, f"{self.nombre_archivo}.csv")
        with open(ruta_csv, "w", newline='', encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["nombre", "precio", "descripcion", "localizacion", "imagen"])
            writer.writeheader()
            writer.writerows(datos)
        logging.info(f"Datos guardados en {ruta_csv}")

        ruta_py = os.path.join(self.ruta_guardado, f"{self.nombre_archivo}.py")
        with open(ruta_py, "w", encoding="utf-8") as py_file:
            py_file.write(f"productos = {datos}")
        logging.info(f"Datos guardados en {ruta_py}")

    def cerrar_driver(self):
        """Cierra el driver de Selenium y finaliza la sesión."""
        if self.driver:
            self.driver.quit()
            logging.info("Driver de Selenium cerrado.")

    def ejecutar(self):
        """Ejecuta el flujo completo de scraping en OLX."""
        self.abrir_pagina()
        self.cerrar_dialogo_consentimiento()
        self.cargar_hasta_objetivo()
        productos = self.extraer_datos_productos()
        self.guardar_datos(productos)
        logging.info(f"Extracción completada. Total de productos: {len(productos)}")
        self.cerrar_driver()

# Ejecución principal
if __name__ == "__main__":
    scraper = OLXScraper()  # Puedes pasar parámetros aquí si lo deseas
    scraper.ejecutar()
