import sys
import os
import json
import datetime
from uuid import uuid4

def ExisteDirectorio(ruta) -> bool:
    return os.path.isdir(ruta)

def GenerarUuid():
    return uuid4().hex

def ExisteFile(ruta):
    return os.path.exists(ruta)

def CrearArchivo(ruta: str, contenido=''):
    with open(ruta, "w") as archivo:
        archivo.write(contenido)

def RutaRelativa(ruta) -> str:
    if not ruta.startswith('/'):
        ruta = '/' + ruta
    return sys.path[0] + ruta

def CargarArchivoJson(ruta) -> dict:
    with open(ruta, 'r') as archivo:
        return json.load(archivo)

def EscribirArchivoJson(ruta, contenido):
    with open(ruta, 'w') as archivo:
        json.dump(contenido, archivo, indent=4)

def FechaToStr(fecha: datetime.datetime):
    return fecha.strftime("%d/%m/%Y %H:%M:%S")

def StrToFecha(fecha: str):
    return datetime.datetime.strptime(fecha, "%d/%m/%Y %H:%M:%S")

def ListArchivos(ruta, extension: str, incluir_extension=False):
    archivos = os.listdir(ruta)
    archivos_format = list(filter(lambda archivo: archivo.endswith(extension), archivos))
    if not incluir_extension:
        archivos_sin_extension = list(map(lambda archivo: archivo.rsplit(extension, 1)[0], archivos_format))
        return archivos_sin_extension
    return archivos_format

def ListCarpetas(ruta) -> list[str]:
    todo = os.listdir(ruta)
    carpetas = []
    for dt in todo:
        if os.path.isdir(f"{ruta}/{dt}"):
            carpetas.append(dt)
    return carpetas

def CrearCarpeta(ruta: str):
    os.makedirs(ruta, exist_ok=True)
