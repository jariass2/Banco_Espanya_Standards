# 📥 Descargador Automático de Ratios Sectoriales - Banco de España

Este script automatiza la descarga de todos los archivos Excel de ratios sectoriales disponibles en la página del Banco de España.

## 🔧 Requisitos Previos

### 1. Python 3.7 o superior
Verifica tu versión:
```bash
python --version
```
o
```bash
python3 --version
```

### 2. Google Chrome
El script utiliza Chrome/Chromium. Asegúrate de tenerlo instalado.

### 3. ChromeDriver
ChromeDriver debe estar instalado y accesible. Opciones:

#### Opción A: Instalación automática (recomendada)
```bash
pip install webdriver-manager
```
Luego modifica la línea del script:
```python
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
```

#### Opción B: Instalación manual
- Descarga ChromeDriver desde: https://chromedriver.chromium.org/downloads
- Asegúrate de que la versión coincida con tu versión de Chrome
- Añade ChromeDriver al PATH del sistema

## 📦 Instalación

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

o directamente:
```bash
pip install selenium
```

### 2. Verificar instalación
```bash
python -c "import selenium; print(selenium.__version__)"
```

## 🚀 Uso

### Ejecución básica
```bash
python descargar_ratios_bde.py
```

o en algunos sistemas:
```bash
python3 descargar_ratios_bde.py
```

### ¿Qué hace el script?

1. **Abre el navegador Chrome** y accede a la página del Banco de España
2. **Rellena automáticamente** el formulario de registro requerido
3. **Identifica todos los sectores** de actividad disponibles
4. **Para cada sector**:
   - Selecciona el sector
   - Elige el ejercicio más reciente
   - Selecciona "todas las empresas" como tamaño
   - Selecciona España como país
   - Descarga el archivo Excel correspondiente
5. **Guarda todos los archivos** en `~/Descargas/Ratios_BDE/`

### Directorio de descarga
Por defecto, los archivos se guardan en:
- **Windows**: `C:\Users\TuUsuario\Descargas\Ratios_BDE\`
- **Mac/Linux**: `~/Descargas/Ratios_BDE/`

## ⚙️ Personalización

### Cambiar directorio de descarga
Modifica la línea en `main()`:
```python
directorio_base = "/ruta/personalizada/de/descarga"
```

### Modo headless (sin ventana visible)
Descomenta esta línea en `configurar_navegador()`:
```python
chrome_options.add_argument("--headless")
```

### Seleccionar parámetros específicos
Modifica la función `descargar_excel_sector()`:
- **Ejercicio**: Cambia `select_ejercicio.select_by_index(1)` al índice deseado
- **Tamaño**: Cambia `select_dimension.select_by_index(1)` según:
  - Todas las empresas
  - Pequeñas empresas
  - Medianas empresas
  - Grandes empresas
- **País**: Cambia `select_pais.select_by_visible_text("España")` al país deseado

## 📊 Salida Esperada

```
======================================================================
DESCARGADOR DE RATIOS SECTORIALES - BANCO DE ESPAÑA
======================================================================

📁 Directorio de descargas: /home/usuario/Descargas/Ratios_BDE

🌐 Iniciando navegador...
🔗 Accediendo a: https://app.bde.es/rss_www/Ratios

📝 Rellenando formulario de registro...
✓ Formulario de registro rellenado

🔍 Buscando sectores de actividad...
✓ Encontrados 88 sectores de actividad

📥 Iniciando descarga de 88 sectores...

[1/88] Procesando: Industrias extractivas
  → Descargando: Industrias extractivas
  ✓ Descargado: ratio_sector_12345.xls

[2/88] Procesando: Industria manufacturera
  → Descargando: Industria manufacturera
  ✓ Descargado: ratio_sector_67890.xls

...

======================================================================
RESUMEN DE DESCARGAS
======================================================================
✓ Exitosas: 88
✗ Fallidas: 0
📁 Archivos guardados en: /home/usuario/Descargas/Ratios_BDE
======================================================================

🔒 Cerrando navegador...
✓ Proceso finalizado
```

## 🐛 Solución de Problemas

### Error: "ChromeDriver not found"
- Instala ChromeDriver correctamente (ver sección de requisitos)
- O usa `webdriver-manager` para instalación automática

### Error: "Element not found"
- La página web puede haber cambiado su estructura
- Verifica que la URL sigue siendo válida
- Aumenta los tiempos de espera en el script

### El navegador se cierra inmediatamente
- Revisa que todas las dependencias estén instaladas
- Verifica los mensajes de error en la consola

### Los archivos no se descargan
- Verifica que tienes permisos de escritura en el directorio de descarga
- Comprueba que Chrome permite descargas automáticas
- Revisa la configuración de seguridad del navegador

### Timeout en las descargas
- Aumenta `max_espera` en `descargar_excel_sector()` (línea ~120)
- Mejora tu conexión a Internet
- Intenta ejecutar en horarios de menos tráfico

## 📝 Notas

- El script respeta pausas entre descargas para no sobrecargar el servidor
- Puedes ver el proceso en tiempo real (navegador visible por defecto)
- Los archivos Excel mantienen el nombre generado por el servidor del BDE
- El proceso puede tardar varios minutos dependiendo del número de sectores

## ⚠️ Disclaimer

Este script es para uso educativo y personal. Asegúrate de cumplir con los términos de uso del Banco de España al descargar datos de su sitio web.

## 📧 Soporte

Si encuentras problemas o necesitas personalizar el script, revisa:
- La documentación de Selenium: https://selenium-python.readthedocs.io/
- Los términos de uso del BDE: https://app.bde.es/rss_www/Ratios

---

**Última actualización**: 2025
**Versión**: 1.0
