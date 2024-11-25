import inspect
from colorama import Fore, Style, init
import logging

# Inicializar colorama
init(autoreset=True)

# Configuración de colores
LEVEL_COLORS = {
    "INFO": Fore.GREEN + Style.BRIGHT,
    "WARNING": Fore.YELLOW + Style.BRIGHT,
    "ERROR": Fore.RED + Style.BRIGHT,
    "TRACE": Fore.BLUE + Style.BRIGHT,
}
CONTENT_COLORS = {
    "INFO": Fore.GREEN,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
    "TRACE": Fore.BLUE,
}
METADATA_COLOR = Fore.BLACK
DATE_COLOR = Fore.BLACK  # Para el color de la fecha
DASH_COLOR = Fore.BLACK  # Para el color de los guiones

# Crear un logger específico
logger = logging.getLogger("print_advanced")
logger.setLevel(logging.DEBUG)

# Clase personalizada para formatear el log
class ColorFormatter(logging.Formatter):
    def format(self, record):
        # Cambiar DEBUG a TRACE
        if record.levelname == "DEBUG":
            record.levelname = "TRACE"

        # Aplicar colores
        level_color = LEVEL_COLORS.get(record.levelname, Fore.WHITE)
        content_color = CONTENT_COLORS.get(record.levelname, Fore.WHITE)
        metadata_color = METADATA_COLOR

        # Obtener información personalizada
        lineno = getattr(record, "custom_lineno", "")
        filename = getattr(record, "custom_filename", "Desconocido")

        # Formatear nivel y mensaje
        record.levelname = f"{level_color}{record.levelname}{Style.RESET_ALL}"
        record.msg = f"{content_color}{record.msg}{Style.RESET_ALL}"

        # Si `lineno` tiene valor, mostrarlo
        formatted_message = f"{record.levelname} {DASH_COLOR}- {record.msg}"
        if lineno:  # Solo agregar la línea si hay una
            formatted_message += f" {DASH_COLOR}- {metadata_color}L: {lineno}{Style.RESET_ALL}"

        # Formatear la fecha sin milisegundos
        log_time = self.formatTime(record, "%Y-%m-%d %H:%M:%S")  # Fecha y hora
        log_time = f"{DATE_COLOR}{log_time} -{Style.RESET_ALL}"  # Color de la fecha

        return f"{log_time} {formatted_message}"

# Configuración del handler
formatter = ColorFormatter('%(asctime)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.handlers = [handler]

# Función que ajusta el nivel de stack y loggea
def _log_with_metadata(level, msg, with_line=False):
    frame = inspect.stack()[2]  # Marco de llamada que genera el log
    logger.log(
        getattr(logging, level.upper()),
        msg,
        extra={
            "custom_lineno": frame.lineno if with_line else "",
            "custom_filename": frame.filename,
        },
        stacklevel=2,  # Capturar el contexto real de la llamada
    )

# Funciones para logueo sin línea
def info(msg):
    _log_with_metadata("info", msg, with_line=False)

def warning(msg):
    _log_with_metadata("warning", msg, with_line=False)

def error(msg):
    _log_with_metadata("error", msg, with_line=False)

def trace(msg):
    _log_with_metadata("debug", msg, with_line=False)

# Funciones para logueo con línea
def infoL(msg):
    _log_with_metadata("info", msg, with_line=True)

def warningL(msg):
    _log_with_metadata("warning", msg, with_line=True)

def errorL(msg):
    _log_with_metadata("error", msg, with_line=True)

def traceL(msg):
    _log_with_metadata("debug", msg, with_line=True)

# Uso
if __name__ == "__main__":
    # Usar las funciones sin la línea de código
    info("1. Mensaje informativo sin línea")
    trace("2. Mensaje de depuración sin línea")
    warning("3. Mensaje de advertencia sin línea")
    error("4. Mensaje de error sin línea")

    # Usar las funciones con la línea de código
    infoL("5. Mensaje informativo con línea")
    traceL("6. Mensaje de depuración con línea")
    warningL("7. Mensaje de advertencia con línea")
    errorL("8. Mensaje de error con línea")

    info({'nombre':'Peter'})
    trace({'nombre':'Joe'})
    error({'nombre':'Carl'})


    infoL({'name':'Peter'})
    traceL({'name':'Joe'})
    errorL({'name':'Carl'})


    info([0,3,2])
    trace([0,3,2])
    error([0,3,2])
    info(type([0,3,2]))
    traceL(type([0,3,2]))
