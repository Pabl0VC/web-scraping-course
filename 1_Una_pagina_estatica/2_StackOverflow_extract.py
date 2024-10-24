import requests
# En este ejemplo utilizaremos la libreria BeatifulSoap para el parseo
from bs4 import BeautifulSoup # permite parsear(analizar) el HTML y luego extraer la data


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

url = "https://stackoverflow.com/questions"

response = requests.get(url, headers=headers)
#print(response) # <Response [200]>

soup = BeautifulSoup(response.text, features="lxml") # Entrega todo el HTML parseado
#print(soup) # por convencion se utiliza la variable soup

# Con esto ya podemos extraer datos

# 1. Extraer el titulo y la descripcion de cada pregunta en StackOverflow
contenedor_preguntas = soup.find(id="questions") # find() solo devuelve un elemento (en este caso todo el elemento con id que corresponde al contenedor de todas las preguntas)
#print(contenedor_preguntas)

lista_preguntas = contenedor_preguntas.find_all("div", class_="s-post-summary") # se utiliza class_ porque en python class es una palabra reservada para otra cosa
# find_all() devuelve una lista con todos los elementos que concuerden con la busqueda
#print(lista_preguntas)
n= 0
for i in lista_preguntas:
    n += 1
    titulo = i.find("a").text # Trae el titulo que se encuentra en el elemento a
    desc = i.find(class_="s-post-summary--content-excerpt").text # Trae el texto del elemento con la siguiente clase
    desc = desc.replace('\n', '').strip() # quita los saltos de linea y elimina los espacios al inicio y final de la cadena
    print(f"{n}.- Titulo: {titulo}\n    Descripción: {desc}")