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
class GooglePlacesScraper:
    # Constantes de configuración
    PERFIL_CHROME = "3_Webs_Dinamicas/perfil_bot"
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    URL = 'https://www.google.com/maps/place/Amaz%C3%B3nico/@40.423706,-3.6872655,17z/data=!4m8!3m7!1s0xd422899dc90366b:0xce28a1dc0f39911d!8m2!3d40.423715!4d-3.6850997!9m1!1b1!16s%2Fg%2F11df4t5hhs?entry=ttu&g_ep=EgoyMDI0MTAyOS4wIKXMDSoASAFQAw%3D%3D'

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
        # Este es el Script de JS para realizar scrolling. Le hago scroll a un contenedor.
        # La clase debe ser de la etiqueta que envuelve toda la zona donde se hace el scrolling
        #Scrolling = (Horizontal, vertical). En este caso se va a hacer scroll 20mil pixeles hacia abajo
        scrollingScript = """ 
        document.getElementsByClassName('m6QErb DxyBCb kA9KIf dS8AEf XiKgde ')[0].scroll(0, 20000)
        """
        return scrollingScript.replace('20000', str(20000 * (iteration + 1))) # mientras mas escrolls llevo dando, mas pixeles voy bajando.

    def scrolling(self):
        """Logica de Scrolling"""
        SCROLLS = 0 # Determina la cantidad de scrolls realizados
        while (SCROLLS != 1): # Decido que voy a hacer 3 scrollings
            self.driver.execute_script(self.getScrollingScript(SCROLLS)) # Ejecuto el script para hacer scrolling del contenedor
            # execute_script() permite ejecutar scripts de JS
            sleep(random.uniform(1, 2)) # Entre cada scrolling espero un tiempo
            SCROLLS += 1 # sumo 1 al contador de scrolls
            info(f"n Scrolls = {SCROLLS}")

    def extraccion_opiniones(self):
        try:
            n_usuarios = 0
            opiniones = self.driver.find_elements(By.XPATH, '//div[@class="jftiEf fontBodyMedium "]') # capturo todos los containers de las opiniones
            for i in opiniones:
                self.driver.switch_to.window(self.driver.window_handles[0]) # se posiciona en la pestaña principal
                n_usuarios += 1
                trace(f"******************* Entra a extraer las opiniones del usuario: {n_usuarios} *******************")
                link = i.find_element(By.XPATH, './div/div/div/button') # Capturo el boton de cada opinion para ingresar al perfil del usuario
                link.click() # clic en foto del usuario
                sleep(5)
                self.driver.switch_to.window(self.driver.window_handles[1]) # le doy foco a la nueva pestaña que se abre (la pestaña 0 es primera que se abrió)
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="jftiEf fontBodyMedium t2Acle FwTFEc azD0p"]'))) # Espera que apareza el elemento container de cada opinion
                # Aplicamos la misma logica de scroll anterior(reutilizamos la funcion scrolling)
                self.scrolling()
                opinionesUsuarios = self.driver.find_elements(By.XPATH,'//div[@class="jftiEf fontBodyMedium t2Acle FwTFEc azD0p"]')
                usuario = self.driver.find_element(By.XPATH,'//h1').text
                trace(f"*************** Opiniones usuario: '{usuario.upper()}' ***************")
                n = 0
                for j in opinionesUsuarios:
                    n += 1
                    info(f"********** {n} *************")
                    try:
                        rating = j.find_element(By.XPATH,'.//span[@class="kvMYJc"]').get_attribute('aria-label')
                        opinion = j.find_element(By.XPATH,'.//span[@class="wiI7pd"]').text
                    except:
                        warning("Fallo en capturar la opinion del usuario")
                    trace(f"Rating: {rating} \nOpinión: {opinion}")
                    info("****************************************")
                self.driver.close()
                    #break
                if n_usuarios == 3:
                    break
        except StaleElementReferenceException:
            error("Fallo en la extraccion de opiniones")

    def ejecutar(self):
        """Ejecuta el flujo completo de MercadoLibreScraper"""
        self.abrir_pagina()
        self.scrolling()
        self.extraccion_opiniones()
        info(f"Extracción completada.")
        self.cerrar_driver()

# Ejecución principal
if __name__ == "__main__":
    scraper = GooglePlacesScraper()
    scraper.ejecutar()