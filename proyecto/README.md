
# OLX Web Scraper

## Descripción del Proyecto
Este proyecto utiliza Selenium para realizar web scraping en la plataforma OLX. La elección de Selenium se debe a que OLX utiliza carga dinámica de productos, lo que significa que la información se carga en la página de manera asincrónica. Esto hace que las bibliotecas tradicionales como Scrapy o Requests no sean efectivas, ya que no pueden manejar el DOM que se actualiza en tiempo real.

El scraper extrae información relevante de los productos, incluyendo nombre, precio, descripción, localización e imágenes, y guarda estos datos en un archivo en el formato especificado (CSV, JSON o Python). Además, se implementa un enfoque de Programación Orientada a Objetos (POO) y modularización, lo que permite un código más limpio, fácil de mantener y reutilizable en futuros proyectos.

## Tabla de Contenidos

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Detalles Técnicos](#detalles-técnicos)
- [Licencia](#licencia)

---

## Requisitos

1. **Python 3.10+**
2. **Google Chrome**
3. **Dependencias del proyecto** (ver sección de Instalación)

## Instalación

1. Clona el repositorio en tu máquina local:

   ```bash
   git clone https://github.com/Pabl0VC/web-scraping-course
   cd WebScraping/proyecto
   ```

2. Crea un entorno virtual (opcional pero recomendado):

   ```bash
   python3 -m venv env
   source env/bin/activate  # En Linux/Mac
   env\Scripts\activate  # En Windows
   ```

3. Instala las dependencias requeridas:

   ```bash
   pip install -r requirements.txt
   ```

## Configuración

Antes de ejecutar el scraper, configura los parámetros en el archivo `config.json` en la carpeta `proyecto`:

```json
{
    "PERFIL_CHROME": "./3_Webs_Dinamicas/perfil_bot",
    "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "RUTA_GUARDADO": "proyecto/resultados_scraping",
    "OBJETIVO": 120,
    "MAX_INTENTOS": 10,
    "NOMBRE_ARCHIVO": "Extraccion_OLX",
    "FORMATO_GUARDADO": ["csv","py","json"],
    "OLX": {
        "URL": "https://www.olx.in/",
        "CARGAR_MAS_BTN_XPATH": "//button[@data-aut-id='btnLoadMore']",
        "ITEM_PRODUCTO_XPATH": "//li[@data-aut-id='itemBox3']",
        "BOTON_DISCLAIMER_XPATH": "//button[@class='fc-button fc-cta-consent fc-primary-button']"
    }
}
```
### Opciones de Personalización

- `OBJETIVO`: Número (***entero***) objetivo de productos a extraer. *ej: 120*

- `MAX_INTENTOS`: Máximo número (***entero*** ) de intentos para hacer clic en "Cargar más" si no se alcanza el objetivo. *ej: 10*

- `NOMBRE_ARCHIVO`: Nombre del archivo donde se guardarán los datos extraídos. *ej: "Extraccion_OLX"*

- `FORMATO_GUARDADO`: Formatos en los que se pueden guardar los datos extraídos. ["csv", "py", "json"]. *ej: ["csv"]*


### Otras Configuraciones
Las siguientes configuraciones son opcionales y pueden ser necesarias si el scraper deja de funcionar debido a cambios en la estructura de la página web, cambios en el user-agent o cambios en los XPaths:
- `URL`: **NO** modificar.

- `RUTA_GUARDADO`: Ruta donde se guardarán los resultados del scraping. **NO** modificar.

- `USER_AGENT`: Especifica el user-agent que emula el navegador. Es importante actualizarlo si OLX realiza cambios que bloqueen el acceso a scrapers.

- **XPaths**: Asegúrate de que los XPaths proporcionados para los elementos de la página sean correctos. Si OLX cambia su diseño, es posible que necesites ajustar los XPaths en `ITEM_PRODUCTO_XPATH`, `CARGAR_MAS_BTN_XPATH` o `BOTON_DISCLAIMER_XPATH`.

## Uso

Para ejecutar el scraper, asegúrate de estar en la carpeta `proyecto` y usa el siguiente comando:

```bash
python main.py
```

Esto ejecutará el scraping en OLX y guardará los datos en la carpeta especificada (`./resultados_scraping`) en el formato deseado.

## Estructura del Proyecto

```plaintext
WebScraping/
└── proyecto/
    ├── main.py                   # Script principal que ejecuta el scraping
    ├── modules/
    │   ├── scraper.py             # Contiene la clase OLXScraper y su lógica de scraping
    │   └── utils.py               # Módulo de utilidades con funciones de configuración y guardado
    ├── resultados/                # Carpeta donde se guardarán los archivos extraídos
    └── config.json                # Archivo de configuración del scraper
```

## Licencia

Este proyecto está bajo la Licencia MIT. Puedes utilizar y modificar libremente este código para fines personales o comerciales. 

--- 

### Nota

Este proyecto es solo para fines educativos. Al hacer scraping, respeta los términos de servicio del sitio y considera las políticas de uso y privacidad de OLX.

---
