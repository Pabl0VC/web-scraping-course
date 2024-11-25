import logging
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import os
import json
import csv

# Importaciones para la interfaz gráfica
import tkinter as tk  # Importa Tkinter para crear interfaces gráficas de usuario (GUIs).
from tkinter import messagebox  # Proporciona cuadros de mensaje para mostrar alertas al usuario.

"""
Funcionalidades utilizadas en proyecto:
    - configurar_driver()
    - mostrar_alerta()
    - abrir_pagina()
    - cerrar_driver()
    - guardar_datos()
    - cargar_configuracion():
"""

def configurar_driver(perfil_chrome, user_agent):
    """Configura el driver de Selenium con opciones de usuario y maximización de pantalla."""
    opts = Options()
    opts.add_argument(f"user-agent={user_agent}")
    opts.add_argument("--start-maximized")
    opts.add_argument(f"user-data-dir={perfil_chrome}")
    return webdriver.Chrome(options=opts)

def mostrar_alerta(mensaje):
    """Muestra una alerta en pantalla (opcional)"""
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Alerta", mensaje)
    root.destroy()

def abrir_pagina(driver, url):
    """Abre la página principal y espera unos segundos."""
    driver.get(url)
    sleep(random.uniform(5, 7))
    logging.info("Página cargada.")

def cerrar_driver(driver):
    """Cierra el driver de Selenium y finaliza la sesión."""
    if driver:
        driver.quit()
        logging.info("Driver de Selenium cerrado.")

def guardar_datos(datos, nombre_archivo, ruta_guardado, formatos):
    """Guarda los datos en los formatos especificados (JSON, CSV, Python)."""
    if 'json' in formatos:
        ruta_json = os.path.join(ruta_guardado, f"{nombre_archivo}.json")
        with open(ruta_json, "w", encoding="utf-8") as json_file:
            json.dump(datos, json_file, ensure_ascii=False, indent=4)
        logging.info(f"Datos guardados en {ruta_json}")

    if 'csv' in formatos:
        ruta_csv = os.path.join(ruta_guardado, f"{nombre_archivo}.csv")
        with open(ruta_csv, "w", newline='', encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["nombre", "precio", "descripcion", "localizacion", "imagen"])
            writer.writeheader()
            writer.writerows(datos)
        logging.info(f"Datos guardados en {ruta_csv}")

    if 'py' in formatos:
        ruta_py = os.path.join(ruta_guardado, f"{nombre_archivo}.py")
        with open(ruta_py, "w", encoding="utf-8") as py_file:
            py_file.write(f"productos = {datos}")
        logging.info(f"Datos guardados en {ruta_py}")

def cargar_configuracion(ruta_config):
    """Lee la configuracion establecida desde config.json"""
    with open(ruta_config, 'r', encoding='utf-8') as archivo:
        configuracion = json.load(archivo)
    return configuracion
