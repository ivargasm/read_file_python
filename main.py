from datetime import timedelta
import json
import os
from sys import argv
from typing import List
import pandas as pd
import glob

# Importación de funciones ETL genéricas personalizadas
import funciones_genericas_etl as generic  # type: ignore


# ========================
# Configuración global
# ========================

DIRECTORIO_DEFECTO = os.path.dirname(os.path.abspath(__file__))


# ========================
# Funciones utilitarias
# ========================

def leer_archivos_xlsx(directorio: str, prefijo: str = "SO_Stock", extension: str = ".xlsx") -> List[str]:
    """
    Busca archivos en el directorio con un prefijo y extensión específicos.

    Parámetros:
        directorio (str): Ruta del directorio donde buscar los archivos.
        prefijo (str): Prefijo del nombre de los archivos a buscar.
        extension (str): Extensión de los archivos (por defecto ".xlsx").

    Retorna:
        List[str]: Lista de rutas de archivos que cumplen con el criterio de búsqueda.
    """
    try:
        archivos = glob.glob(f"{directorio}/*{prefijo}*{extension}")
        return archivos
    except Exception as e:
        print(f"[Error] No se pudieron listar archivos en {directorio}: {e}")
        return []


def cargar_datos_en_dataframe(directorio: str, archivos: List[str]) -> pd.DataFrame:
    """
    Lee varios archivos Excel y los concatena en un solo DataFrame.

    Parámetros:
        directorio (str): Ruta donde se encuentran los archivos.
        archivos (List[str]): Lista de nombres de archivos a cargar.

    Retorna:
        pd.DataFrame: DataFrame consolidado con la información de todos los archivos.
    """
    dataframes = []
    for archivo in archivos:
        ruta_completa = os.path.join(directorio, archivo)
        try:
            df = pd.read_excel(ruta_completa, engine='openpyxl', dtype={'UPC': str, 'Código Tienda': str})
            dataframes.append(df)
            print(f"[OK] Archivo cargado: {archivo}")
        except Exception as e:
            print(f"[Error] Falló la carga del archivo {archivo}: {e}")

    if not dataframes:
        print("[Advertencia] No se cargó ningún archivo correctamente.")
        return pd.DataFrame()

    return pd.concat(dataframes, ignore_index=True)


def validar_datos(df: pd.DataFrame, columnas: List[str]) -> None:
    """
    Valida que las columnas requeridas existan y no contengan valores nulos.

    Parámetros:
        df (pd.DataFrame): DataFrame a validar.
        columnas (List[str]): Lista de nombres de columnas requeridas.

    Lanza:
        ValueError: Si falta alguna columna o si alguna contiene valores nulos.
    """
    for columna in columnas:
        if columna not in df.columns:
            raise ValueError(f"La columna '{columna}' no existe en el DataFrame.")
        if df[columna].isnull().any():
            raise ValueError(f"La columna '{columna}' contiene valores nulos.")



# ========================
# Función principal
# ========================

def main(chain_id: int, date:int, directorio: str = DIRECTORIO_DEFECTO):
    """
    Función principal que orquesta el flujo de carga, limpieza y transformación de los datos.

    Parámetros:
        chain_id (int): ID de la cadena.
        date (int): Fecha en formato YYYYMMDD.
        directorio (str): Ruta del directorio donde se encuentran los archivos Excel.
    """
    try:
        archivos = leer_archivos_xlsx(prefijo="SO_Stock", directorio=directorio)
        if not archivos:
            print("[Error] No se encontraron archivos para procesar.")
            return

        df = cargar_datos_en_dataframe(directorio, archivos)
        if df.empty:
            print("[Error] El DataFrame está vacío después de intentar cargar los archivos.")
            return

        

        # Mostrar resultado final
        print(f"[OK] Proceso completado exitosamente. Registros procesados: {len(df)}")
        df.to_csv(f'sellout_{date}.txt', sep='\t', index=False)
        print(f"Archivo generado: sellout_{date}.txt")

    except ValueError as ve:
        print(f"[Error de validación] {ve}")
    except Exception as e:
        print(f"[Error inesperado] {e}")


# ========================
# Punto de entrada
# ========================

if __name__ == "__main__":
    try:
        script, chain_id, date = argv
        main(int(chain_id), int(date))
    except ValueError:
        print("[Error] El parámetro chain_id debe ser un número entero.")
    except Exception as e:
        print(f"[Error al ejecutar el script] {e}")
