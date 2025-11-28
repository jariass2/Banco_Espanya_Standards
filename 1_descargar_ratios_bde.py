#!/usr/bin/env python3
"""
Script para descargar automáticamente todos los archivos Excel de ratios sectoriales
del Banco de España (https://app.bde.es/rss_www/Ratios)
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def configurar_navegador(directorio_descarga):
    """Configura el navegador Chrome con opciones de descarga"""
    chrome_options = Options()
    
    # Configurar directorio de descarga
    prefs = {
        "download.default_directory": directorio_descarga,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Opcional: ejecutar en modo headless (sin ventana visible)
    # chrome_options.add_argument("--headless")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def rellenar_formulario_registro(driver):
    """Rellena el formulario inicial de registro"""
    try:
        wait = WebDriverWait(driver, 10)
        
        # Tipo de entidad
        tipo_entidad = Select(wait.until(EC.presence_of_element_located((By.ID, "entidad"))))
        tipo_entidad.select_by_index(1)  # Seleccionar primera opción disponible
        
        # Objetivo del estudio
        objetivo = Select(wait.until(EC.presence_of_element_located((By.ID, "objetivo"))))
        objetivo.select_by_index(1)  # Seleccionar primera opción disponible
        
        # País
        pais = Select(wait.until(EC.presence_of_element_located((By.ID, "paisRegistro"))))
        pais.select_by_visible_text("España")
        
        print("✓ Formulario de registro rellenado")
        time.sleep(1)
        
    except Exception as e:
        print(f"⚠ Error al rellenar formulario de registro: {e}")

def obtener_sectores(driver):
    """Obtiene todos los sectores de actividad disponibles"""
    try:
        wait = WebDriverWait(driver, 10)
        select_sector = Select(wait.until(EC.presence_of_element_located((By.ID, "sector"))))
        
        sectores = []
        for option in select_sector.options:
            if option.get_attribute("value"):  # Ignorar opciones vacías
                sectores.append({
                    'value': option.get_attribute("value"),
                    'text': option.text
                })
        
        print(f"✓ Encontrados {len(sectores)} sectores de actividad")
        return sectores
        
    except Exception as e:
        print(f"✗ Error al obtener sectores: {e}")
        return []

def descargar_excel_sector(driver, sector_value, sector_text, directorio_base):
    """Descarga el archivo Excel para un sector específico"""
    try:
        wait = WebDriverWait(driver, 10)
        
        # Seleccionar sector
        select_sector = Select(wait.until(EC.presence_of_element_located((By.ID, "sector"))))
        select_sector.select_by_value(sector_value)
        time.sleep(0.5)
        
        # El ejercicio ya viene seleccionado por defecto con el más reciente
        # Esperamos a que el elemento esté presente para asegurar que la página cargó
        wait.until(EC.presence_of_element_located((By.ID, "ejercicio")))
        time.sleep(0.5)
        
        # Seleccionar tamaño (Menos de 50 millones)
        select_dimension = Select(wait.until(EC.presence_of_element_located((By.ID, "dimension"))))
        select_dimension.select_by_value("1")  # Value "1" is "Menos de 50 millones"
        time.sleep(0.5)
        
        # Seleccionar país España
        select_pais = Select(wait.until(EC.presence_of_element_located((By.ID, "pais"))))
        select_pais.select_by_visible_text("España")
        time.sleep(0.5)
        
        # Buscar y hacer clic en el botón de descarga Excel
        # El botón es un input type="button" con value="Consultar en EXCEL"
        try:
            boton_excel = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//input[@value='Consultar en EXCEL']")
            ))
            
            # Contar archivos antes de la descarga
            archivos_antes = set(os.listdir(directorio_base))
            
            boton_excel.click()
            print(f"  → Descargando: {sector_text}")
            
            # Verificar si aparece el popup de "Datos no disponibles"
            try:
                # Esperar brevemente a que aparezca el botón Aceptar
                boton_aceptar = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@value='Aceptar']"))
                )
                boton_aceptar.click()
                print(f"  ⚠ Datos no disponibles para {sector_text} (Popup aceptado)")
                return False
            except TimeoutException:
                # No apareció el popup, continuar esperando la descarga
                pass
            
            # Esperar a que el archivo se descargue
            tiempo_espera = 0
            max_espera = 30  # 30 segundos máximo
            
            while tiempo_espera < max_espera:
                time.sleep(1)
                archivos_despues = set(os.listdir(directorio_base))
                nuevos_archivos = archivos_despues - archivos_antes
                
                # Verificar si hay un archivo nuevo que no sea temporal (.crdownload, .tmp)
                archivos_completos = [f for f in nuevos_archivos 
                                     if not f.endswith(('.crdownload', '.tmp', '.part'))]
                
                if archivos_completos:
                    archivo_descargado = archivos_completos[0]
                    print(f"  ✓ Descargado: {archivo_descargado}")
                    return True
                
                tiempo_espera += 1
            
            print(f"  ⚠ Timeout esperando descarga para {sector_text}")
            driver.save_screenshot(f"debug_timeout_{sector_value}.png")
            return False

        except TimeoutException:
            print(f"  ⚠ Could not find download button for {sector_text}")
            driver.save_screenshot(f"debug_no_button_{sector_value}.png")
            return False
            
    except Exception as e:
        print(f"  ✗ Error descargando {sector_text}: {e}")
        driver.save_screenshot(f"debug_error_{sector_value}.png")
        return False

def main():
    """Función principal"""
    print("="*70)
    print("DESCARGADOR DE RATIOS SECTORIALES - BANCO DE ESPAÑA")
    print("="*70)
    
    # Configurar directorio de descargas
    # Configurar directorio de descargas
    # Usar el directorio 'downloads' dentro del directorio actual del script
    directorio_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")
    os.makedirs(directorio_base, exist_ok=True)
    print(f"\n📁 Directorio de descargas: {directorio_base}\n")
    
    driver = None
    
    try:
        # Configurar navegador
        print("🌐 Iniciando navegador...")
        driver = configurar_navegador(directorio_base)
        
        # Acceder a la página
        url = "https://app.bde.es/rss_www/Ratios"
        print(f"🔗 Accediendo a: {url}")
        driver.get(url)
        time.sleep(2)
        
        # Rellenar formulario de registro
        print("\n📝 Rellenando formulario de registro...")
        rellenar_formulario_registro(driver)
        
        # Obtener todos los sectores
        print("\n🔍 Buscando sectores de actividad...")
        sectores = obtener_sectores(driver)
        
        if not sectores:
            print("✗ No se encontraron sectores disponibles")
            return
        
        # Descargar Excel para cada sector
        print(f"\n📥 Iniciando descarga de {len(sectores)} sectores...\n")
        exitosos = 0
        fallidos = 0
        
        for i, sector in enumerate(sectores, 1):
            print(f"[{i}/{len(sectores)}] Procesando: {sector['text']}")
            
            if descargar_excel_sector(driver, sector['value'], sector['text'], directorio_base):
                exitosos += 1
            else:
                fallidos += 1
            
            time.sleep(2)  # Pausa entre descargas
        
        # Resumen final
        print("\n" + "="*70)
        print("RESUMEN DE DESCARGAS")
        print("="*70)
        print(f"✓ Exitosas: {exitosos}")
        print(f"✗ Fallidas: {fallidos}")
        print(f"📁 Archivos guardados en: {directorio_base}")
        print("="*70)
        
    except Exception as e:
        print(f"\n✗ Error crítico: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if driver:
            print("\n🔒 Cerrando navegador...")
            time.sleep(2)
            driver.quit()
        
        print("✓ Proceso finalizado")

if __name__ == "__main__":
    main()
