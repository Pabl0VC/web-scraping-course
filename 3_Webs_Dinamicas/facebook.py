# Importaciones de bibliotecas estándar
import random  # Proporciona funciones para generar números aleatorios.
from time import sleep  # Permite pausar la ejecución del programa durante un tiempo específico.

# Importaciones de la biblioteca Selenium
from selenium import webdriver  # Importa el módulo principal de Selenium para controlar navegadores.
from selenium.webdriver.chrome.options import Options  # Permite configurar opciones para el navegador Chrome.
from selenium.webdriver.common.by import By  # Proporciona métodos para localizar elementos en el DOM.
from selenium.webdriver.support.ui import WebDriverWait  # Proporciona una espera explícita para elementos del DOM.
from selenium.webdriver.support import expected_conditions as EC  # Contiene condiciones comunes para esperar elementos.
from selenium.common.exceptions import StaleElementReferenceException  # Excepciones comunes para manejar errores en Selenium.

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
class FacebookScraper:
    # Constantes de configuración
    PERFIL_CHROME = "3_Webs_Dinamicas/perfil_bot"
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    URL = 'https://www.facebook.com/elcorteingles'

    def __init__(self):
        self.driver = self.configurar_driver()  # Inicializa el driver de Selenium, que permitirá realizar el web scraping y las interacciones automatizadas con la página web.
        info("Driver de Selenium configurado.")

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
        info("Página cargada.")
    
    def cerrar_driver(self):
        """Cierra el driver de Selenium y finaliza la sesión."""
        if self.driver:
            self.driver.quit()
            info("Driver de Selenium cerrado.")

    # Simplemente remplazo el 20000 en la cadena del script, por un numero que dependa de la iteracion en que me encuentro actualmente
    def getScrollingScript(self, iteration): 
        """Funcion para obtener el Script de Scrolling dependiendo de cuantos scrollings ya he hecho"""
        scrollingScript = """window.scrollTo(0, 20000)""" # en este caso no se pasa la clase de una etiqueta debido a que el scroll es en toda la pagina

        return scrollingScript.replace('20000', str(20000 * (iteration + 1))) # mientras mas escrolls llevo dando, mas pixeles voy bajando.

    def scrolling(self):
        """Logica de Scrolling"""
        SCROLLS = 0 # Determina la cantidad de scrolls realizados
        while (SCROLLS != 1): # Decido que voy a hacer 3 scrollings
            self.driver.execute_script(self.getScrollingScript(SCROLLS)) # Ejecuto el script para hacer scrolling del contenedor
            # execute_script() permite ejecutar scripts de JS
            sleep(random.uniform(1, 2)) # Entre cada scrolling espero un tiempo
            SCROLLS += 1 # sumo 1 al contador de scrolls
            warning("SCROLL")
    
    def cerrar_disclaimer(self):
        """Verifica aparicion de Disclaimer. Si lo encuentra lo cierra"""
        try:
            disclaimer = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Cerrar"]'))) # Espera 10s por disclaimer
            trace("Se encontró Disclaimer...")
            disclaimer.click() # Clic en cerrar Disclaimer (X)
            trace("Disclaimer cerrado")
        except:
            warning("No se encontró disclaimer")

    def extraccion_comentarios(self):
        try:
            contenedor_comentarios = self.driver.find_elements(By.XPATH, '')
            info("ENTRA A EXTRAER")
            sleep(5)


        except StaleElementReferenceException:
            error("Fallo en la extraccion de opiniones")

    def ejecutar(self):
        """Ejecuta el flujo completo de MercadoLibreScraper"""
        self.abrir_pagina()
        self.cerrar_disclaimer()
        #self.scrolling()
        self.extraccion_comentarios()
        info("Extracción completada.")
        self.cerrar_driver()

# Ejecución principal
if __name__ == "__main__":
    scraper = FacebookScraper()
    scraper.ejecutar()