# Banco de España - Automatización de Ratios Sectoriales

Este proyecto automatiza la descarga y procesamiento de ratios sectoriales de sociedades no financieras del Banco de España.

## 📋 Descripción

El proyecto consta de varios scripts que automatizan el proceso completo de:
1. Descarga de ratios sectoriales desde la web del Banco de España
2. Extracción de códigos CNAE
3. Renombrado de archivos descargados
4. Carga de valores en un archivo maestro (masterfile)

## 🚀 Scripts Disponibles

### 1. `1_descargar_ratios_bde.py`
Descarga automáticamente los archivos de ratios sectoriales desde la web del Banco de España.

**Características:**
- Utiliza Selenium para automatizar la navegación web
- Descarga ratios para diferentes códigos CNAE y años
- Guarda los archivos en el directorio `downloads/`

### 2. `2_Extrae lista CNAEs.py`
Extrae la lista de códigos CNAE disponibles.

### 3. `3_Cambio nombre ficheros.py`
Renombra los archivos descargados siguiendo el formato estándar `YYYY_CCCC.xls`:
- `YYYY`: Año
- `CCCC`: Código CNAE

### 4. `4_Carga_valores_en_masterfile.py`
**Script principal de procesamiento**

Procesa todos los archivos del directorio `downloads/` y carga los valores en el archivo maestro.

**Funcionalidad:**
- Recorre todos los archivos `.xls` del directorio `downloads/`
- Extrae el año (primeros 4 dígitos) y el código CNAE (últimos 4 dígitos) del nombre del archivo
- Lee los valores de los ratios (Q1, Q2, Q3) de cada archivo
- Los coloca en la hoja correspondiente al año en `CNAE masterfile.xlsx`
- Ubica los valores en la fila correspondiente al código CNAE

**Uso:**
```bash
python3 4_Carga_valores_en_masterfile.py
```

**Salida esperada:**
```
2025-11-29 10:18:27 - INFO - Procesamiento completado:
  - Archivos procesados exitosamente: 295
  - Archivos con errores: 2
  - Total de archivos: 297
```

## 📊 Estructura de Datos

### Formato de archivos de entrada
Los archivos descargados siguen el formato: `YYYY_CCCC.xls`
- Ejemplo: `2023_0100.xls` → Año 2023, CNAE 0100

### Estructura del Masterfile
El archivo `CNAE masterfile.xlsx` contiene:
- **Hojas**: Una por cada año (ej: 2022, 2023)
- **Filas**: Una por cada código CNAE
- **Columnas**: Ratios con sus cuartiles (ej: R01_Q1, R01_Q2, R01_Q3)

### Ratios incluidos
El sistema procesa los siguientes ratios del Banco de España:
- **R01-R05**: Costes operativos, beneficios y rentabilidades
- **R06-R15**: Estructura del activo
- **R16-R21**: Ratios adicionales de activo
- **R22-R28**: Estructura del pasivo
- **T1**: Tasa de variación de la cifra neta de negocios

Cada ratio incluye tres cuartiles (Q1, Q2, Q3) de la distribución estadística.

## 🛠️ Instalación

### Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación de dependencias
```bash
pip install -r requirements.txt
```

### Dependencias principales
- `selenium>=4.15.0` - Automatización web
- `pandas>=2.0.0` - Procesamiento de datos
- `openpyxl>=3.1.0` - Lectura/escritura de archivos Excel (.xlsx)
- `xlrd>=2.0.0` - Lectura de archivos Excel antiguos (.xls)

## 📁 Estructura del Proyecto

```
BancoEspana/
├── 1_descargar_ratios_bde.py          # Descarga de ratios
├── 2_Extrae lista CNAEs.py            # Extracción de CNAEs
├── 3_Cambio nombre ficheros.py        # Renombrado de archivos
├── 4_Carga_valores_en_masterfile.py   # Carga en masterfile
├── CNAE masterfile.xlsx               # Archivo maestro con todos los datos
├── INSTRUCCIONES.md                   # Instrucciones detalladas
├── requirements.txt                   # Dependencias del proyecto
├── downloads/                         # Archivos descargados (.xls)
├── Descargador_Ratios_BDE/           # Directorio auxiliar
└── README.md                          # Este archivo
```

## 📖 Uso del Sistema Completo

### Flujo de trabajo recomendado:

1. **Descargar ratios**
   ```bash
   python3 1_descargar_ratios_bde.py
   ```

2. **Extraer lista de CNAEs** (si es necesario)
   ```bash
   python3 2_Extrae lista CNAEs.py
   ```

3. **Renombrar archivos**
   ```bash
   python3 3_Cambio nombre ficheros.py
   ```

4. **Cargar valores en masterfile**
   ```bash
   python3 4_Carga_valores_en_masterfile.py
   ```

## 🔍 Verificación de Datos

Para verificar que los datos se han cargado correctamente:

```python
import pandas as pd

# Leer el masterfile
df = pd.read_excel('CNAE masterfile.xlsx', sheet_name='2023')

# Ver las primeras filas
print(df.head())

# Verificar un CNAE específico
cnae_100 = df[df['CNAE'] == 100]
print(cnae_100[['CNAE', 'R01_Q1', 'R01_Q2', 'R01_Q3']])
```

## 📝 Logging

Todos los scripts incluyen logging detallado que muestra:
- ✅ Archivos procesados exitosamente
- ⚠️ Advertencias sobre archivos que no coinciden con el patrón
- ❌ Errores durante el procesamiento
- 📊 Resumen final con estadísticas

## 🤝 Contribuciones

Este es un proyecto interno para la automatización de procesos con datos del Banco de España.

## 📄 Licencia

Los datos procesados provienen del Banco de España y están sujetos a sus términos de uso:
> Se prohíbe la redistribución de los datos, incluso cuando se pretenda hacerlo a título gratuito.
> ©Copyright Banco de España/Registros de España. 2025. Madrid. Reservados todos los derechos.

## 📧 Contacto

Para preguntas o problemas, contactar con el equipo de desarrollo.

---

**Última actualización:** Noviembre 2025
