from flask import Blueprint, jsonify, request
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models import ConfGeral, User

login_bp = Blueprint('login', __name__)

@login_bp.route('/validar_acesso_configuracao', methods=['POST'])
def validar_acesso_configuracao():

    dados = request.get_json()

    username = dados.get('username', '')
    password = dados.get('password', '')

    user = User.query.filter(
        func.lower(User.username) == username.lower()
    ).first()

    if not user or not check_password_hash(
        user.password_hash,
        password
    ):
        return jsonify({
            'success': False,
            'message': 'Utilizador ou password incorretos!'
        })

    if user.funcao_id != 3:
        return jsonify({
            'success': False,
            'message': 'Apenas administradores podem alterar as configurações.'
        })

    return jsonify({
        'success': True
    })


@login_bp.route('/obter_configuracao')
def obter_configuracao():

    conf = ConfGeral.query.first()

    if not conf:

        return jsonify({
            'pais': 'Portugal',
            'localizacao': 'Ponte de Lima'
        })

    return jsonify(
        conf.to_dict()
    )

@login_bp.route('/guardar_configuracao', methods=['POST'])
def guardar_configuracao():

    dados = request.get_json()

    conf = ConfGeral.query.first()

    if not conf:

        conf = ConfGeral()

        db.session.add(conf)

    conf.pais = dados['pais']
    conf.localizacao = dados['localizacao']

    db.session.commit()

    return jsonify({
        'success': True
    })

    