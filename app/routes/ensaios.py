
from flask import Blueprint, jsonify
from app.models import Ensaio, Testes

ensaios_bp = Blueprint('ensaios', __name__)


@ensaios_bp.route('/ensaios/<ensaio_numero>/testes', methods=['GET'])
def get_testes_por_ensaio(ensaio_numero):

    ensaio = Ensaio.query.filter_by(ensaio=ensaio_numero).first()

    if not ensaio:
        return jsonify([])

    testes = Testes.query.filter_by(ensaio_id=ensaio.id).all()

    result = [
        {
            "ordem": t.ordem,
            "nome": t.teste.teste if t.teste else None,
            "criarpasta": t.teste.criarpasta if t.teste else False
        }
        for t in sorted(testes, key=lambda x: x.ordem or 0)
        if t.teste and t.teste.criarpasta
    ]

    return jsonify(result)
