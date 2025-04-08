# 📊 Plantilla Base ETL - Lectura de Archivos Excel (`SO_Stock`)

Este proyecto es una **plantilla inicial** para comenzar un proceso ETL (Extracción, Transformación y Carga), centrado en buscar archivos Excel de ventas o inventario con un nombre tipo `SO_Stock*.xlsx`, consolidarlos y validarlos como parte de un flujo de procesamiento.

## 🧩 ¿Qué hace este script?

- Busca archivos Excel en un directorio con prefijo `SO_Stock` y extensión `.xlsx`.
- Carga múltiples archivos en un solo `DataFrame`.
- Valida columnas requeridas y datos nulos.
- Maneja errores de forma robusta con bloques `try-except`.
- Genera un archivo `.txt` delimitado por tabuladores con los datos consolidados.

---

## 📂 Estructura del Proyecto

```
etl_so_stock/
│
├── funciones_genericas_etl.py    # Funciones reutilizables (limpieza, transformación, etc.)
├── etl_so_stock.py               # Script principal (el que estás leyendo)
├── README.md                     # Documentación del proyecto
└── SO_Stock_Enero.xlsx           # Archivos de ejemplo (no incluidos en el repo)
```

---

## ⚙️ Requisitos

- Python 3.8 o superior
- Librerías:
  - `pandas`
  - `openpyxl`

Instálalos con:

```bash
pip install pandas openpyxl
```

---

## ▶️ ¿Cómo usarlo?

Desde consola, ejecuta el script con los siguientes parámetros:

```bash
python etl_so_stock.py <chain_id> <fecha>
```

- `chain_id`: ID de la cadena (entero).
- `fecha`: Fecha del proceso en formato `YYYYMMDD`.

### Ejemplo:

```bash
python etl_so_stock.py 101 20250407
```

---

## 🧪 Validaciones implementadas

- Revisión de columnas obligatorias: si una no existe o tiene valores nulos, lanza un error.
- Validación de existencia de archivos.
- Errores de lectura de archivos se registran y no detienen el proceso general.

---

## 📤 Salida generada

Si todo se ejecuta correctamente, se genera un archivo:

```
sellout_<fecha>.txt
```

Ejemplo:

```
sellout_20250407.txt
```

- Formato: texto delimitado por tabulaciones (`.txt`)
- Contenido: todos los datos consolidados de los archivos leídos.

---

## 🧼 Funciones incluidas

### `leer_archivos_xlsx(...)`

Busca archivos en el directorio con cierto prefijo y extensión.

### `cargar_datos_en_dataframe(...)`

Lee varios archivos Excel y concatena su contenido.

### `validar_datos(...)`

Verifica que existan las columnas obligatorias y que no tengan valores nulos.

### `main(...)`

Orquesta todo el flujo del proceso ETL, manejando errores y generando el archivo de salida.

---

## 🧠 Notas adicionales

- Este script está diseñado como punto de partida para un proyecto ETL.
- Puedes extenderlo fácilmente agregando funciones de transformación, conexión a base de datos, generación de reportes, etc.
- Asegúrate de tener en el mismo directorio el archivo `funciones_genericas_etl.py` si utilizas funciones auxiliares.

---

