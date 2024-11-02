from flask import Blueprint, request, jsonify
from datetime import datetime
import random
import string
import unicodedata

generate_curp_bp = Blueprint('generar_curp', __name__)

#NO LEER POR FAVOR
PALABRAS_PROHIBIDAS = {
    'BACA', 'BAKA', 'BUEI', 'BUEY', 'CACA', 'CACO', 'CAGA', 'CAGO', 'CAKA',
    'CAKO', 'COGE', 'COGI', 'COJA', 'COJE', 'COJI', 'COJO', 'COLA', 'CULO',
    'FALO', 'FETO', 'GETA', 'GUEI', 'GUEY', 'JETA', 'JOTO', 'KACA', 'KACO',
    'KAGA', 'KAGO', 'KAKA', 'KAKO', 'KOGE', 'KOGI', 'KOJA', 'KOJE', 'KOJI',
    'KOJO', 'KOLA', 'KULO', 'LILO', 'LOCA', 'LOCO', 'LOKA', 'LOKO', 'MAME',
    'MAMO', 'MEAR', 'MEAS', 'MEON', 'MIAR', 'MION', 'MOCO', 'MOKO', 'MULA',
    'MULO', 'NACA', 'NACO', 'PEDA', 'PEDO', 'PENE', 'PIPI', 'PITO', 'POPO',
    'PUTA', 'PUTO', 'QULO', 'RATA', 'ROBA', 'ROBE', 'ROBO', 'RUIN', 'SENO',
    'TETA', 'VACA', 'VAGA', 'VAGO', 'VAKA', 'VUEI', 'VUEY', 'WUEI', 'WUEY'
}

def reemplazar_n(texto):
    return texto.replace('Ñ', 'X').replace('ñ', 'X')

def limpiar_texto(texto):
    texto_normalizado = unicodedata.normalize('NFD', texto)
    texto_sin_acentos = ''.join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn')
    return texto_sin_acentos

def procesar_nombre(nombre):
    nombres = nombre.split()
    if len(nombres) > 1 and nombres[0].upper() in ['JOSE', 'MARIA', 'JOSÉ', 'MARÍA']:
        return nombres[1]
    return nombres[0]

def generar_curp(nombre, apellido_paterno, apellido_materno, fecha_nacimiento, sexo, estado):
    nombre = reemplazar_n(nombre)
    apellido_paterno = reemplazar_n(apellido_paterno)
    apellido_materno = reemplazar_n(apellido_materno) if apellido_materno else 'X'

    nombre_procesado = procesar_nombre(nombre)

    primera_letra_apellido_paterno = limpiar_texto(apellido_paterno[0].upper())
    primera_vocal_interna_apellido_paterno = limpiar_texto(next(
        (char for char in apellido_paterno[1:] if char.lower() in 'aeiouáéíóúü'), 'X'
    ).upper())
    
    curp = (
        primera_letra_apellido_paterno +
        primera_vocal_interna_apellido_paterno +
        limpiar_texto(apellido_materno[0].upper()) +
        limpiar_texto(nombre_procesado[0].upper())
    )

    if curp in PALABRAS_PROHIBIDAS:
        curp = curp[0] + 'X' + curp[2:]

    fecha = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
    curp += fecha.strftime("%y%m%d")

    curp += sexo[0].upper()
    curp += estado.upper()

    curp += ''.join([
        (c := next((char for char in apellido_paterno[1:] if char.lower() not in 'aeiouáéíóúü'), 'X')).upper(),
        (c := next((char for char in apellido_materno[1:] if char.lower() not in 'aeiouáéíóúü'), 'X')).upper(),
        (c := next((char for char in nombre_procesado[1:] if char.lower() not in 'aeiouáéíóúü'), 'X')).upper()
    ])

    homoclave = random.choice(string.digits + string.ascii_uppercase) + random.choice(string.digits)
    curp += homoclave

    return curp

@generate_curp_bp.route('/generar_curp', methods=['POST'])
def generar_curp_api():
    data = request.get_json()
    nombre = data.get("nombre")
    apellido_paterno = data.get("apellido_paterno")
    apellido_materno = data.get("apellido_materno")
    fecha_nacimiento = data.get("fecha_nacimiento")
    sexo = data.get("sexo")
    estado = data.get("estado")

    if not all([nombre, apellido_paterno, fecha_nacimiento, sexo, estado]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    curp = generar_curp(nombre, apellido_paterno, apellido_materno, fecha_nacimiento, sexo, estado)
    return jsonify({"curp": curp})