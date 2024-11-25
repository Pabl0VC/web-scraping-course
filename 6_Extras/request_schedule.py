import schedule
import time
import random
import requests
from lxml import html
import os
import csv

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

start_urls = [
    "https://www.accuweather.com/es/cl/santiago/60449/weather-forecast/60449",
    "https://www.accuweather.com/es/ar/buenos-aires/7894/weather-forecast/7894",
    "https://www.accuweather.com/es/es/madrid/308526/weather-forecast/308526",
]

def temp_actual():
    datos = []  # Lista para almacenar las tuplas de ciudad y temperatura
    # Por cada una de las URLs que quiero extraer...
    for url in start_urls:
        print("-" * 40)
        time.sleep(random.uniform(1, 3))
        response = requests.get(url, headers=headers)

        # Parsear el HTML con lxml
        tree = html.fromstring(response.text)
            
        # Usar XPath para extraer la información deseada
        ciudad_get = tree.xpath('//h1[@class]/text()') # Ciudad
        ciudad = ciudad_get[0].split(',')[0].strip()
        temperatura_get = tree.xpath('//div[@class="cur-con-weather-card__body"]//div[@class="temp"]/text()') # Temperatura actual
        temperatura = temperatura_get[0].strip()
        hora_get = tree.xpath('//p[@class="cur-con-weather-card__subtitle"]/text()')
        hora = hora_get[0].strip()
        print(f"{hora} : {ciudad} : {temperatura}")

        # Agregar los datos a la lista
        datos.append((hora, ciudad, temperatura))

    return datos  # Devolver los datos para ser usados en guardar_csv


def guardar_csv(datos, csv_file):
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Escribir encabezado si el archivo es nuevo
        if not file_exists:
            writer.writerow(["HORA","CIUDAD","TEMPERATURA"])

        # Escribir los datos
        writer.writerows(datos)


def ejecutar():
    datos = temp_actual()  # Obtener los datos de las ciudades y temperaturas
    guardar_csv(datos, "6_Extras/clima.csv")  # Pasar los datos a la función de guardado


# Logica de schedule
schedule.every(1).minutes.do(ejecutar) # Cada 1 minuto ejecutar la funcion temp_actual()
# Llamamos a la funcion fuera del lazo para una primera llamada instantanea
ejecutar()
# Reviso la cola de procesos cada segundo, para verificar si tengo que correr algun proceso pendiente
while True:
    schedule.run_pending() # Correr procesos que esten pendientes de ser ejecutados.
    time.sleep(1) # Para no saturar el CPU de mi maquina (por el while true), espero 1 segundo entre cada iteracion