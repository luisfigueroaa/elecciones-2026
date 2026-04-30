import json
import requests
import os
import time

# Configuración de rutas
UBIGEOS_FILE = "data/departamentos.json"
OUTPUT_DIR = "data/departamentos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Headers mínimos necesarios
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "es-PE,es;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://resultadoelectoral.onpe.gob.pe/main/presidenciales",
    "Origin": "https://resultadoelectoral.onpe.gob.pe",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=1, i",
}

def descargar_datos():
    # 1. Cargar tus ubigeos
    with open(UBIGEOS_FILE, 'r', encoding='utf-8') as f:
        archivo_json = json.load(f)
    
    # 2. Acceder a la lista que está dentro de la clave 'data'
    departamentos = archivo_json.get('data', [])

    for dep in departamentos:
        # Ahora sí, dep es un diccionario como {"ubigeo": "010000", "nombre": "AMAZONAS"}
        ubigeo = dep.get('ubigeo')
        nombre = dep.get('nombre')
        
        print(f"Descargando datos para {nombre} ({ubigeo})...")

        url = (
            f"https://resultadoelectoral.onpe.gob.pe/presentacion-backend/eleccion-presidencial/"
            f"participantes-ubicacion-geografica-nombre?"
            f"tipoFiltro=ubigeo_nivel_01&idAmbitoGeografico=1&ubigeoNivel1={ubigeo}&idEleccion=10"
        )

        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                output_path = os.path.join(OUTPUT_DIR, f"{ubigeo}.json")
                with open(output_path, 'w', encoding='utf-8') as out_f:
                    json.dump(response.json(), out_f, indent=4, ensure_ascii=False)
                print(f"Guardado: {output_path}")
            else:
                print(f"Error {response.status_code} en {nombre}")

        except Exception as e:
            print(f"Falló conexión para {nombre}: {e}")

        time.sleep(0.5)

if __name__ == "__main__":
    descargar_datos()