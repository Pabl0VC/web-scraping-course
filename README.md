# Web Scraping Course Code
Este repositorio contiene el código desarrollado durante un curso de web scraping. Incluye ejemplos prácticos utilizando diversas herramientas y librerías de scraping como `requests`, `BeautifulSoup`, `lxml` y `Scrapy`. Cada directorio y archivo representa ejercicios y proyectos que muestran distintas técnicas de extracción de datos de sitios web.

## Estructura del Proyecto
**requests**: Ejemplos básicos utilizando la librería `requests` para realizar peticiones HTTP.

**BeautifulSoup**: Ejercicios con `BeautifulSoup` para la extracción de datos y el parsing de HTML.

**Scrapy**: Código que implementa spiders avanzados para la recolección de datos masivos.

**lxml**: Ejemplos de parsing y manipulación de HTML con `lxml`.

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
Cada directorio contiene scripts independientes que puedes ejecutar para ver ejemplos específicos. A continuación, te explicamos cómo ejecutar los principales:

### Ejecutar un Script con Requests y BeautifulSoup
Dirígete al directorio del script y ejecuta:

```bash
python nombre_del_script.py
```
### Ejecutar un Spider de Scrapy
Para ejecutar el spider, navega al directorio donde esté ubicado y usa el siguiente comando:

```bash
scrapy runspider nombre_del_spider.py
```
Los datos recolectados se almacenarán en archivos CSV o JSON, según lo configurado en cada script.

## Contribuciones
Este repositorio no está abierto a contribuciones externas. Sin embargo, puedes utilizar el código como referencia personal o en tus propios proyectos.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.