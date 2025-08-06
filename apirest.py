from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Ruta del archivo JSON
RUTA_ARCHIVO_JSON = '/home/devasc/labs/devnet-src/python/API-REST/dispositivos.json'

# Cargar dispositivos desde archivo si existe
if os.path.exists(RUTA_ARCHIVO_JSON):
    with open(RUTA_ARCHIVO_JSON, 'r') as f:
        inventario_dispositivos = json.load(f)
        # Convertir claves a enteros (porque JSON las guarda como strings)
        inventario_dispositivos = {int(k): v for k, v in inventario_dispositivos.items()}
        siguiente_id = max(inventario_dispositivos.keys(), default=0) + 1
else:
    inventario_dispositivos = {}
    siguiente_id = 1

# Guardar en el archivo JSON
def guardar_en_archivo():
    with open(RUTA_ARCHIVO_JSON, 'w') as f:
        json.dump(inventario_dispositivos, f, indent=4)

# POST - Agregar dispositivo
@app.route('/dispositivos', methods=['POST'])
def agregar_dispositivo():
    global siguiente_id
    datos_entrada = request.get_json()
    if not datos_entrada or 'nombre' not in datos_entrada or 'tipo' not in datos_entrada:
        return jsonify({"error": "Datos incompletos"}), 400

    dispositivo_actual = {
        "id": siguiente_id,
        "nombre": datos_entrada['nombre'],
        "tipo": datos_entrada['tipo']
    }
    inventario_dispositivos[siguiente_id] = dispositivo_actual
    siguiente_id += 1
    guardar_en_archivo()
    return jsonify(dispositivo_actual), 201

# GET - Listar dispositivos
@app.route('/dispositivos', methods=['GET'])
def listar_dispositivos():
    return jsonify(list(inventario_dispositivos.values())), 200

# PUT - Actualizar dispositivo
@app.route('/dispositivos/<int:dispositivo_id>', methods=['PUT'])
def actualizar_dispositivo(dispositivo_id):
    if dispositivo_id not in inventario_dispositivos:
        return jsonify({"error": "Dispositivo no encontrado"}), 404

    datos_entrada = request.get_json()
    if not datos_entrada:
        return jsonify({"error": "Sin datos"}), 400

    dispositivo_actual = inventario_dispositivos[dispositivo_id]
    dispositivo_actual['nombre'] = datos_entrada.get('nombre', dispositivo_actual['nombre'])
    dispositivo_actual['tipo'] = datos_entrada.get('tipo', dispositivo_actual['tipo'])
    guardar_en_archivo()
    return jsonify(dispositivo_actual), 200

# DELETE - Eliminar dispositivo
@app.route('/dispositivos/<int:dispositivo_id>', methods=['DELETE'])
def eliminar_dispositivo(dispositivo_id):
    if dispositivo_id not in inventario_dispositivos:
        return jsonify({"error": "Dispositivo no encontrado"}), 404

    del inventario_dispositivos[dispositivo_id]
    guardar_en_archivo()
    return '', 204

# Ejecutar servidor Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)
