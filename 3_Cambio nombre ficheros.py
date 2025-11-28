import os
import re

def transformar_nombre_archivo(nombre_archivo):
    # Patrón para identificar archivos con el formato "YYYY_XXXX_b_YYYYMMDD.xls"
    # Ejemplo: 2023_A011_b_20251119.xls, 2023_A01_b_..., 2023_A_b_...
    patron = r'(\d{4})_([A-Z](\d*))_b_\d+\.xls'
    
    # Buscar coincidencias con el patrón
    coincidencia = re.match(patron, nombre_archivo)
    
    if coincidencia:
        # Extraer el año y los dígitos
        anio = coincidencia.group(1)
        numeros = coincidencia.group(3)
        
        # Rellenar con ceros a la derecha hasta tener 3 dígitos
        # Si no hay números (ej: "A"), será "000"
        if not numeros:
            numeros = "000"
        else:
            numeros = numeros.ljust(3, '0')
        
        # Formatear el nuevo nombre de archivo
        # Se mantiene la lógica de usar los números y añadir un 0 al final
        nuevo_nombre = f"{anio}_{numeros}0.xls"
        
        print(f"Transformando: {nombre_archivo} -> {nuevo_nombre}")
        return nuevo_nombre
    else:
        # print(f"No se pudo transformar: {nombre_archivo}")
        return None

def renombrar_archivos_en_directorio(directorio):
    # Obtener la lista de archivos en el directorio
    archivos = os.listdir(directorio)
    
    for archivo in archivos:
        # Obtener la ruta completa del archivo
        ruta_archivo = os.path.join(directorio, archivo)
        
        # Verificar si es un archivo y si cumple con el formato especificado
        if os.path.isfile(ruta_archivo):
            nuevo_nombre = transformar_nombre_archivo(archivo)
            
            if nuevo_nombre:
                # Obtener la ruta completa del nuevo nombre de archivo
                nueva_ruta_archivo = os.path.join(directorio, nuevo_nombre)
                
                # Renombrar el archivo
                os.rename(ruta_archivo, nueva_ruta_archivo)
                print(f"Renombrado: {archivo} -> {nuevo_nombre}")

# Obtener el directorio donde se encuentra este script
directorio_script = os.path.dirname(os.path.abspath(__file__))

# Carpeta "downloads" dentro del directorio del script
directorio_downloads = os.path.join(directorio_script, "downloads")

# Verificar si la ruta del directorio es correcta
if not os.path.exists(directorio_downloads):
    print(f"El directorio {directorio_downloads} no existe.")
else:
    print(f"Buscando archivos en: {directorio_downloads}")
    # Renombrar archivos en la carpeta "downloads"
    renombrar_archivos_en_directorio(directorio_downloads)