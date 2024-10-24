import requests
from bs4 import BeautifulSoup

url = "https://news.ycombinator.com/"

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, features="lxml") # Se agrega esto features="lxml" para que no aparezca un warning.
#print(soup)

lista_noticias = soup.find_all("tr",class_="athing") # Esta etiqueta tr contiene el titulo de la noticia
#print(lista_noticias)

for i in lista_noticias:
    #print(i)
    n = i.find("span",class_="rank").text
    titulo = i.find("span",class_="titleline").text
    link = i.find("span",class_="titleline").find("a").get('href') # .get() extrae el valor de una etiqueta. En este caso de hrf

    # a continuacion se captura la etiqueta hermana de i (tr), que corresponde a otro tr pero no tiene id, ni clase ni nada que se pueda identificar, por lo que es necesario utilizar find_next_sibling() para traer la siguiente etiqueta 
    metadata = i.find_next_sibling() # Aqui tengo capturada la etiqueta tr hermana y ya puedo trabajar su informacion dentro
    #print(metadata)
    try:
        puntos_tmp = metadata.find("span", class_="score").text # trae los puntos, si no existen puntos devuelve error
        puntos = int(puntos_tmp.replace("points","").strip()) # cambio el formato de los puntos a valores enteros, quito la palabra points y los espacios
    except:
        puntos = 0 # si no existen puntos lo deja en 0

    try:
        comentarios_tmp = metadata.find("span", class_="subline").text #24 points by skrrtww 3 hours ago  | hide | 4 comments 
        comentarios_tmp = comentarios_tmp.split("|")[-1] # trae el ultimo elemento de la cadena separadas por un |
        comentarios = int(comentarios_tmp.replace("comments","").strip())
    except:
        comentarios = 0

    print(f"{n}- Titulo: {titulo}\nLink: {link}\nPuntos: {puntos}\nComentarios: {comentarios}")