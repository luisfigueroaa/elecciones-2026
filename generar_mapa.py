import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import json

def dibujar_mapa_departamento(ubigeo, color):
    mapa_dep = mapa[mapa['ubigeo'] == ubigeo]

    fig, ax = plt.subplots(1, 1, figsize=(10, 12))
    mapa.plot(ax=ax, color=mapa['color'], edgecolor='#000', linewidth=0.5, alpha=0.2)
    mapa_dep.plot(ax=ax, edgecolor='#000', linewidth=0.5, color=color)

    plt.axis('off')
    output_path = f'mapas/{ubigeo}.png'
    plt.savefig(output_path, dpi=100, bbox_inches='tight', transparent=True)
    plt.close()

mapa_file = "data/mapas/peruLow.json"

with open(mapa_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

for feature in data['features']:
    feature['properties']['ubigeo'] = feature.get('id')

#resultados csv onpe
df_resultados = pd.read_csv("data/resultados_tabla.csv", dtype={'ubigeo': str})

#mapa geojson con id(ubigeo) en features
mapa = gpd.GeoDataFrame.from_features(data['features'])

#hacer un merge 
mapa = mapa.merge(df_resultados, on='ubigeo', how='left')
mapa['color'] = mapa['color'].fillna('#D3D3D3')

fig, ax = plt.subplots(1, 1, figsize=(10, 12))
mapa.plot(ax=ax, color=mapa['color'], edgecolor='#000', linewidth=0.5)

plt.axis('off')
output_path = 'mapas/peru.png'
plt.savefig(output_path, dpi=100, bbox_inches='tight', transparent=True)

#pintar por departamento
for index, fila in mapa.iterrows():
    cod_ubigeo = fila['ubigeo']
    color_voto = fila['color']
    
    if pd.notna(cod_ubigeo) and cod_ubigeo != 'None':
        dibujar_mapa_departamento(cod_ubigeo, color_voto)
    
    print(f'Mapa {cod_ubigeo} generado correctamente')

print('Mapa generado correctamente')