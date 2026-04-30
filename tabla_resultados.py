import json
import os
import pandas as pd
import csv

# --- CONFIGURACIÓN ---
UBIGEOS_FILE = "data/departamentos.json"
INPUT_DIR = "data/departamentos"
OUTPUT_FILE = "data/resultados_tabla.csv"

# Diccionario de Colores
colores_partidos = {
    "JUNTOS POR EL PERÚ": "#FF0000",
    "FUERZA POPULAR": "#FF8C00",
    "RENOVACIÓN POPULAR": "#00FFFF",
    "PARTIDO DEL BUEN GOBIERNO": "#FFFF00",
    "PARTIDO CÍVICO OBRAS": "#008000",
    "DEFAULT": "#D3D3D3"
}

IGNORAR = ["VOTOS EN BLANCO", "VOTOS NULOS", "VOTOS IMPUGNADOS"]

def generar_csv_final():
    # 1. Mapear nombres de departamentos
    nombres_deps = {}
    if os.path.exists(UBIGEOS_FILE):
        with open(UBIGEOS_FILE, 'r', encoding='utf-8') as f:
            data_u = json.load(f)
            for d in data_u.get('data', []):
                nombres_deps[str(d['ubigeo'])] = str(d['nombre'])

    resultados = []
    
    if not os.path.exists(INPUT_DIR):
        print(f"❌ Error: La carpeta {INPUT_DIR} no existe.")
        return

    archivos = [f for f in os.listdir(INPUT_DIR) if f.endswith('.json')]

    for arc in archivos:
        ubigeo_id = str(arc.replace('.json', ''))
        nombre_dep = nombres_deps.get(ubigeo_id, f"Ubigeo {ubigeo_id}")
        
        path = os.path.join(INPUT_DIR, arc)
        with open(path, 'r', encoding='utf-8') as f:
            try:
                content = json.load(f)
                if content.get("success") and content.get("data"):
                    # Buscar primer partido real
                    ganador_real = None
                    for cand in content["data"]:
                        nombre_p = cand["nombreAgrupacionPolitica"].strip().upper()
                        if nombre_p not in IGNORAR:
                            ganador_real = cand
                            break
                    
                    if ganador_real:
                        partido_nombre = ganador_real["nombreAgrupacionPolitica"].strip()
                        candidato_nombre = ganador_real.get("nombreCandidato", "N/A").strip()
                        
                        resultados.append({
                            "ubigeo": ubigeo_id,
                            "departamento": nombre_dep,
                            "partido": partido_nombre,
                            "candidato": candidato_nombre, # <--- Nueva columna
                            "votos_cantidad": int(ganador_real.get("totalVotosValidos", 0)),
                            "porcentaje": float(ganador_real.get("porcentajeVotosValidos", 0)),
                            "color": colores_partidos.get(partido_nombre.upper(), colores_partidos["DEFAULT"])
                        })
            except Exception as e:
                print(f"Error procesando {arc}: {e}")

    # 3. Guardar con tipos de datos protegidos (QUOTE_NONNUMERIC)
    if resultados:
        df = pd.DataFrame(resultados).sort_values("departamento")
        
        # Guardar CSV
        df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC)
        
        print(f"✅ CSV generado con éxito: {OUTPUT_FILE}")
        print("\nPrevisualización del archivo:")
        print(df[["departamento", "candidato", "partido", "porcentaje"]].head())
    else:
        print("❌ No se encontraron datos.")

if __name__ == "__main__":
    generar_csv_final()