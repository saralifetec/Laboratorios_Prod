from calendar import monthrange
from datetime import date
from flask import Blueprint, app, jsonify, request, session
from app.models import Codigosg, ConfHorasAuto, Horas, User
from services.resumo_horas_service import obter_resumo_horas

index_bp = Blueprint('index', __name__)

@index_bp.route('/home/resumo_horas')
def home_resumo_horas():

    user = User.query.get(session['user_id'])
    funcao_id = user.funcao_id

    laboratorio_id = request.args.get('laboratorio_id', type=int)
    ano = request.args.get('ano', type=int)
    mes = request.args.get('mes', type=int)

    if ano is None or mes is None or laboratorio_id == '':
        return jsonify([])

    if funcao_id == 1:

        tecnicos = [user]

    elif funcao_id in (2, 3):

        if laboratorio_id == 0:
            tecnicos = User.query.all()
        else:
            tecnicos = User.query.filter_by(
                laboratorio_id=laboratorio_id
            ).all()

    else:
        return jsonify([])

    return jsonify(
        obter_resumo_horas(
            tecnicos,
            ano,
            mes
        )
    )