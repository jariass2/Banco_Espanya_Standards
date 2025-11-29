#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para cargar valores de ratios del Banco de España en el archivo masterfile.

Este script:
1. Recorre todos los archivos .xls del directorio downloads/
2. Extrae el año (primeros 4 dígitos) y el código CNAE (últimos 4 dígitos) del nombre del archivo
3. Lee los valores de los ratios (Q1, Q2, Q3) de cada archivo
4. Los coloca en la hoja correspondiente al año en el archivo CNAE masterfile.xlsx
5. Ubica los valores en la fila correspondiente al código CNAE

Formato de archivos de entrada: YYYY_CCCC.xls (ej: 2023_0100.xls)
- YYYY: Año (determina la hoja del masterfile)
- CCCC: Código CNAE (determina la fila del masterfile)
"""

import os
import pandas as pd
import openpyxl
from pathlib import Path
import re
from typing import Dict, List, Tuple
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MasterfileLoader:
    """Clase para cargar valores de ratios en el masterfile."""
    
    def __init__(self, downloads_dir: str = "downloads", masterfile_path: str = "CNAE masterfile.xlsx"):
        """
        Inicializa el cargador de masterfile.
        
        Args:
            downloads_dir: Directorio con los archivos descargados
            masterfile_path: Ruta al archivo masterfile
        """
        self.downloads_dir = Path(downloads_dir)
        self.masterfile_path = Path(masterfile_path)
        self.masterfile_data = {}  # Diccionario para almacenar datos por año
        
    def parse_filename(self, filename: str) -> Tuple[str, str]:
        """
        Extrae el año y el código CNAE del nombre del archivo.
        
        Args:
            filename: Nombre del archivo (ej: 2023_0100.xls)
            
        Returns:
            Tupla (año, cnae) o (None, None) si no coincide con el patrón
        """
        pattern = r'^(\d{4})_(\d{4})\.xls$'
        match = re.match(pattern, filename)
        
        if match:
            year = match.group(1)
            cnae = match.group(2)
            return year, cnae
        
        return None, None
    
    def extract_ratios_from_file(self, filepath: Path) -> Dict[str, float]:
        """
        Extrae los valores de los ratios de un archivo .xls del BdE.
        
        Args:
            filepath: Ruta al archivo .xls
            
        Returns:
            Diccionario con los ratios y sus valores {ratio_name: {Q1: val, Q2: val, Q3: val}}
        """
        try:
            # Leer el archivo sin encabezado
            df = pd.read_excel(filepath, header=None)
            
            ratios_data = {}
            
            # Buscar la fila donde están los ratios (columna 0 contiene el código del ratio)
            # Los ratios empiezan después de la fila que contiene "Ratio"
            ratio_start_idx = None
            for idx, row in df.iterrows():
                if pd.notna(row[0]) and str(row[0]).strip() == 'Ratio':
                    ratio_start_idx = idx + 1
                    break
            
            if ratio_start_idx is None:
                logger.warning(f"No se encontró la sección de ratios en {filepath.name}")
                return ratios_data
            
            # Extraer los ratios (R01, R02, etc. y T1)
            for idx in range(ratio_start_idx, len(df)):
                row = df.iloc[idx]
                
                # La columna 0 contiene el código del ratio (R01, R02, etc.)
                ratio_code = row[0]
                
                if pd.isna(ratio_code):
                    continue
                
                ratio_code = str(ratio_code).strip()
                
                # Verificar si es un código de ratio válido (R## o T#)
                if not (ratio_code.startswith('R') or ratio_code.startswith('T')):
                    continue
                
                # Las columnas 3, 4, 5 contienen Q1, Q2, Q3 respectivamente
                # (después de la columna de número de empresas)
                try:
                    q1 = pd.to_numeric(row[3], errors='coerce')
                    q2 = pd.to_numeric(row[4], errors='coerce')
                    q3 = pd.to_numeric(row[5], errors='coerce')
                    
                    ratios_data[ratio_code] = {
                        'Q1': q1 if pd.notna(q1) else None,
                        'Q2': q2 if pd.notna(q2) else None,
                        'Q3': q3 if pd.notna(q3) else None
                    }
                except Exception as e:
                    logger.warning(f"Error extrayendo valores para {ratio_code} en {filepath.name}: {e}")
                    continue
            
            return ratios_data
            
        except Exception as e:
            logger.error(f"Error leyendo archivo {filepath.name}: {e}")
            return {}
    
    def load_masterfile(self):
        """Carga el archivo masterfile en memoria."""
        try:
            # Leer todas las hojas del masterfile
            xl_file = pd.ExcelFile(self.masterfile_path)
            
            for sheet_name in xl_file.sheet_names:
                df = pd.read_excel(self.masterfile_path, sheet_name=sheet_name)
                self.masterfile_data[sheet_name] = df
                logger.info(f"Cargada hoja '{sheet_name}' con {len(df)} filas")
                
        except Exception as e:
            logger.error(f"Error cargando masterfile: {e}")
            raise
    
    def update_masterfile_row(self, year: str, cnae: str, ratios_data: Dict[str, Dict[str, float]]):
        """
        Actualiza una fila del masterfile con los datos de ratios.
        
        Args:
            year: Año (nombre de la hoja)
            cnae: Código CNAE (identifica la fila)
            ratios_data: Diccionario con los ratios y sus valores
        """
        # Verificar si existe la hoja para ese año
        if year not in self.masterfile_data:
            logger.warning(f"No existe la hoja '{year}' en el masterfile. Creando nueva hoja...")
            # Crear una nueva hoja basada en la estructura de una existente
            if self.masterfile_data:
                template_df = list(self.masterfile_data.values())[0].copy()
                template_df = template_df.iloc[:0]  # Vaciar datos pero mantener columnas
                self.masterfile_data[year] = template_df
            else:
                logger.error("No hay hojas en el masterfile para usar como plantilla")
                return
        
        df = self.masterfile_data[year]
        
        # Convertir CNAE a entero para comparación
        cnae_int = int(cnae)
        
        # Buscar la fila correspondiente al CNAE
        row_idx = df[df['CNAE'] == cnae_int].index
        
        if len(row_idx) == 0:
            # Si no existe la fila, agregarla
            logger.info(f"Agregando nueva fila para CNAE {cnae} en año {year}")
            new_row = {'CNAE': cnae_int}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            row_idx = [len(df) - 1]
            self.masterfile_data[year] = df
        
        row_idx = row_idx[0]
        
        # Actualizar los valores de los ratios
        updated_count = 0
        for ratio_code, values in ratios_data.items():
            for quartile in ['Q1', 'Q2', 'Q3']:
                col_name = f"{ratio_code}_{quartile}"
                
                if col_name in df.columns:
                    value = values.get(quartile)
                    if value is not None:
                        df.at[row_idx, col_name] = value
                        updated_count += 1
                else:
                    logger.debug(f"Columna {col_name} no existe en el masterfile")
        
        self.masterfile_data[year] = df
        logger.info(f"Actualizados {updated_count} valores para CNAE {cnae} en año {year}")
    
    def save_masterfile(self):
        """Guarda el masterfile actualizado."""
        try:
            with pd.ExcelWriter(self.masterfile_path, engine='openpyxl') as writer:
                for sheet_name, df in self.masterfile_data.items():
                    # Ordenar por CNAE antes de guardar
                    df = df.sort_values('CNAE').reset_index(drop=True)
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    logger.info(f"Guardada hoja '{sheet_name}' con {len(df)} filas")
            
            logger.info(f"Masterfile guardado exitosamente en {self.masterfile_path}")
            
        except Exception as e:
            logger.error(f"Error guardando masterfile: {e}")
            raise
    
    def process_all_files(self):
        """Procesa todos los archivos del directorio downloads."""
        if not self.downloads_dir.exists():
            logger.error(f"El directorio {self.downloads_dir} no existe")
            return
        
        # Obtener todos los archivos .xls
        xls_files = list(self.downloads_dir.glob("*.xls"))
        logger.info(f"Encontrados {len(xls_files)} archivos .xls en {self.downloads_dir}")
        
        if not xls_files:
            logger.warning("No se encontraron archivos para procesar")
            return
        
        # Cargar el masterfile
        self.load_masterfile()
        
        # Procesar cada archivo
        processed_count = 0
        error_count = 0
        
        for filepath in sorted(xls_files):
            filename = filepath.name
            year, cnae = self.parse_filename(filename)
            
            if year is None or cnae is None:
                logger.warning(f"Archivo {filename} no coincide con el patrón esperado (YYYY_CCCC.xls)")
                error_count += 1
                continue
            
            logger.info(f"Procesando {filename} -> Año: {year}, CNAE: {cnae}")
            
            # Extraer ratios del archivo
            ratios_data = self.extract_ratios_from_file(filepath)
            
            if not ratios_data:
                logger.warning(f"No se extrajeron ratios de {filename}")
                error_count += 1
                continue
            
            # Actualizar masterfile
            self.update_masterfile_row(year, cnae, ratios_data)
            processed_count += 1
        
        # Guardar el masterfile actualizado
        if processed_count > 0:
            self.save_masterfile()
        
        # Resumen
        logger.info("=" * 60)
        logger.info(f"Procesamiento completado:")
        logger.info(f"  - Archivos procesados exitosamente: {processed_count}")
        logger.info(f"  - Archivos con errores: {error_count}")
        logger.info(f"  - Total de archivos: {len(xls_files)}")
        logger.info("=" * 60)


def main():
    """Función principal."""
    logger.info("Iniciando carga de valores en masterfile...")
    
    loader = MasterfileLoader(
        downloads_dir="downloads",
        masterfile_path="CNAE masterfile.xlsx"
    )
    
    loader.process_all_files()
    
    logger.info("Proceso finalizado")


if __name__ == "__main__":
    main()
