# Web Scraping Course Code
Este repositorio contiene el código desarrollado durante un curso de web scraping. Incluye ejemplos prácticos utilizando diversas herramientas y librerías de scraping como `requests`, `BeautifulSoup`, `lxml` y `Scrapy`. Cada directorio y archivo representa ejercicios y proyectos que muestran distintas técnicas de extracción de datos de sitios web.

## Estructura del Proyecto
- **requests**: Ejemplos básicos utilizando la librería `requests` para realizar peticiones HTTP.

- **BeautifulSoup**: Ejercicios con `BeautifulSoup` para la extracción de datos y el parsing de HTML.

- **Scrapy**: Código que implementa spiders avanzados para la recolección de datos masivos.

- **lxml**: Ejemplos de parsing y manipulación de HTML con `lxml`.

## Requisitos del Sistema
- Python 3.x
- pip (para la instalación de dependencias)

## Instalación de Dependencias
Para clonar este repositorio e instalar las dependencias, sigue los siguientes pasos:

1. Clona el repositorio:

```bash
git clone https://github.com/Pabl0VC/web-scraping-course.git
cd web-scraping-course
```
2. Instala las dependencias usando el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Uso
Uso
Cada script Python puede ejecutarse de manera individual. La mayoría de los spiders de Scrapy utilizan la clase CrawlerProcess para correr directamente como scripts de Python.

Por ejemplo:

```python
from scrapy.crawler import CrawlerProcess
from my_spider import MySpider


process = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI': 'output.json'
})

process.crawl(MySpider)
process.start()
```

Esto permite ejecutar el spider directamente con:

```bash
python nombre_del_script.py
```

## Estructura del Proyecto
La estructura del repositorio es la siguiente:

```graphql
web-scraping-course/
│
├── 1_beautifulsoup_example.py      # Ejemplo usando BeautifulSoup para extraer datos
├── 2_requests_example.py           # Ejemplo de uso simple de requests
├── 3_scrapy_example.py             # Spider básico con Scrapy
├── 4_scrapy_StackOverflow.py       # Scrapeo de preguntas en StackOverflow
├── data/                           # Directorio para almacenar los datos extraídos
├── requirements.txt                # Lista de dependencias
└── README.md                       # Documentación del proyecto
```
Los datos recolectados se almacenarán en archivos CSV o JSON, según lo configurado en cada script.

## Ejemplos
Algunos de los ejemplos de scraping incluidos:

1. BeautifulSoup y Requests: Extracción de datos de páginas web simples.

2. Spider de Scrapy: Spider automatizado para extraer preguntas y descripciones de StackOverflow.

3. Exportación de Datos: Almacenamiento de los datos extraídos en JSON, CSV u otros formatos.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.