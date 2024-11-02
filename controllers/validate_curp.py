from flask import Blueprint, jsonify, request
from load_xml import load_transitions

validate_curp_bp = Blueprint('validar_curp', __name__)

initial_state = 'q0'
accept_states = {'q42'}

def validate_curp_with_turing_machine(curp):
    state = initial_state
    tape = list(curp) + ['']
    head = 0
    archivo_xml = "MT_CURP.jff"
    transitions = load_transitions(archivo_xml)

    while state not in accept_states:
        symbol = tape[head] if head < len(tape) else ''
        key = (state, symbol)
        
        if key in transitions:
            write, move, new_state = transitions[key]
            if head < len(tape):
                tape[head] = write
            if move == 'R':
                head += 1
            elif move == 'L' and head > 0:
                head -= 1
            state = new_state
        else:
            return False
    
    return True

@validate_curp_bp.route('/validar_curp', methods=['POST'])
def validar_curp():
    data = request.get_json()
    curp = data.get('curp')
    
    if not curp:
        return jsonify({"error": "La CURP es requerida"}), 400
    
    es_valida = validate_curp_with_turing_machine(curp)
    
    if es_valida:
        return jsonify({"curp": curp, "valida": True}), 200
    else:
        return jsonify({"curp": curp, "valida": False}), 400