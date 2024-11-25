import time
import random
import requests
from lxml import html
import os
import re

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

url_semilla = "https://file-examples.com/index.php/sample-documents-download/sample-xls-download/" # Pagina principal

def download_file(url, folder):
    # Crear la carpeta si no existe
    if not os.path.exists(folder):
        os.makedirs(folder)

    response = requests.get(url, headers=headers) # Se conecta a pagina principal

    # Parsear el HTML con lxml
    tree = html.fromstring(response.text)

    # Usar XPath para extraer la información deseada
    links = tree.xpath('//table[@id="table-files"]//a/@href') # Lista de links de descargas

    # Descargar cada archivo
    for link in links:
        print("-" * 40)
        file_name = link.split("/")[-1]  # Obtener el nombre del archivo desde el enlace, ej: 'https://file-examples.com/wp-content/storage/2017/02/file_example_XLS_10.xls'
        file_path = os.path.join(folder, file_name)  # Crear la ruta completa para guardar archivo, ej: 6_Extras/files/file_example_XLS_10.xls

        print(f"Descargando {file_name}...")
        file_response = requests.get(link, headers=headers, allow_redirects=True) # Se conecta a cada link de descarga
        tree = html.fromstring(file_response.text)
        scripts = tree.xpath("//script[contains(text(), 'window.location.href.replace')]/text()") # Extraer el contenido del script
        
        if scripts:
            script_content = scripts[0]
            match = re.search(r"file-examples.com/storage/([^/]+?)/", script_content) # Buscar el valor del token en el script
            if match:
                token = match.group(1)
                print(f"Token extraído: {token}")
                url_download = link.replace("wp-content/storage/", f"storage/{token}/") # Actualiza el link de descarga segun el token
                print(f"Link de descarga: {url_download}")
                file_download = requests.get(url_download, headers=headers, allow_redirects=True)  # Descargar el archivo (pero solo está en memoria en file_download.content)
            else:
                print("No se encontró el Token.")
        else:
            print("No se encontró el script en la página.")
        time.sleep(random.uniform(1, 3))

        if file_download.status_code == 200:  # Comprueba si la descarga fue exitosa
            with open(file_path, "wb") as file: # Se crea un archivo vacío en el disco
                time.sleep(random.uniform(1, 3))
                file.write(file_download.content) #  Guardar el archivo en disco
            print(f"{file_name} guardado EXITOSAMENTE!!!")
        else:
            print(f"Error al descargar {file_name}")

download_file(url_semilla,"6_Extras/files")  # Obtener los datos de las ciudades y temperaturas

