import json

resultados_json = "data/resultados.json"
departamentos_json = "data/departamentos.json"

with open(resultados_json, 'r', encoding='utf-8') as f:
    resultados = json.load(f)

with open(departamentos_json, 'r', encoding='utf-8') as f:
    departamentos = json.load(f)

with open('plantilla.html', 'r', encoding='utf-8') as f:
    plantilla = f.read()

filas_html = ""

for item in resultados["data"]:
    agrupacion = item.get('nombreAgrupacionPolitica')
    nombre = item.get('nombreCandidato') or item.get('nombreAgrupacionPolitica')
    votos = item.get('totalVotosValidos', 0)
    # Formatear números con separador de miles
    votos_fmt = f"{votos:,}".replace(" ", ",")

    porcentaje = item.get('porcentajeVotosValidos', 0)
    porcentaje = f"{float(porcentaje):.3f}"

    filas_html += f"""
    <tr>
        <td>{agrupacion}</td>
        <td>{nombre}</td>
        <td class="num">{votos_fmt}</td>
        <td class="num">{porcentaje}%</td>
    </tr>"""

lista_dep_html = ""
for dep in departamentos["data"]:
    ubigeo = dep.get('ubigeo')
    nombre_dep = dep.get('nombre')
    
    lista_dep_html += '<span>'
    lista_dep_html += f'[<a href="#" class="enlace-mapa" data-img="{ubigeo}.png">{nombre_dep}</a>]&nbsp\n'
    lista_dep_html += '</span>'

# Hacer el reemplazo
html_final = plantilla.replace('{{tabla-resultados}}', filas_html)
html_final = html_final.replace('{{lista-departamentos}}', lista_dep_html)

# Guardar el resultado
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_final)

print("index.html generado")
