from flask import Blueprint, jsonify, request, session
from sqlalchemy import func, or_

from app.models import Horas, Templatenormas, Testes, User
from app.utils.datas import parse_data_iso
from app.utils.horas import parse_horas_iso
from .. import db
from services.horas_service import (
    recalcular_teste_horas
)
from services.testes_service import (
    atualizar_horasesgotadas,
    calcular_horas_teste
)

horas_bp = Blueprint('horas', __name__)

@horas_bp.route('/horas/<int:id>', methods=['DELETE'])
def delete_horas(id):

    try:

        hora = Horas.query.get_or_404(id)

        teste_id = hora.teste_id

        db.session.delete(hora)

        if teste_id:
            recalcular_teste_horas(
                teste_id
            )

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Registo de horas eliminado com sucesso!'
        })

    except Exception as e:

        db.session.rollback()

        return jsonify({
            'success': False,
            'error': f'Erro ao eliminar registo: {str(e)}'
        }), 500

@horas_bp.route('/horas/<int:id>', methods=['PUT'])
def update_horas(id):

    data = request.get_json(silent=True) or {}

    tipo = (data.get('tipo') or '').strip().lower()
    manual_val = (data.get('manual') or '').strip() if 'manual' in data else None

    if tipo == 'manual' or ('manual' in data):

        ok, detalhe = validar_manual_por_regras(manual_val)

        if not ok:
            return jsonify({
                'success': False,
                'error': 'Valor manual invalido.',
                'code': detalhe
            }), 400

    try:

        hora = Horas.query.get_or_404(id)

        teste_antigo = hora.teste_id

        for field in [
            'tecnico_id',
            'data',
            'horas',
            'ensaio_id',
            'codigog_id',
            'teste_id',
            'obs'
        ]:

            if field in data:
                setattr(hora, field, data[field])

        if 'manual' in data:
            hora.manual = (manual_val or None)

        teste_novo = hora.teste_id

        if teste_antigo:
            recalcular_teste_horas(
                teste_antigo
            )

        if (
            teste_novo
            and teste_novo != teste_antigo
        ):
            recalcular_teste_horas(
                teste_novo
            )

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Horas atualizadas com sucesso!'
        })

    except Exception as e:

        db.session.rollback()

        return jsonify({
            'success': False,
            'error': f'Erro ao atualizar horas: {str(e)}'
        }), 500



@horas_bp.route('/horas/inserir', methods=['POST'])
def inserir_horas():

    try:

        payload = request.get_json(silent=True) or {}

        user = User.query.get(session['user_id'])

        ensaio_id = payload.get('ensaio_id')
        teste_id = payload.get('teste_id')
        horas_in = payload.get('horas')

        data_str = (
            payload.get('data')
            or payload.get('dia')
            or payload.get('date')
        )

        obs = (payload.get('obs') or '').strip()

        if not ensaio_id or not teste_id:
            return jsonify({
                'error': 'ensaio_id e teste_id são obrigatórios.'
            }), 400

        try:
            dia = parse_data_iso(data_str)
        except ValueError as ve:
            return jsonify({
                'error': str(ve)
            }), 400

        try:
            horas_val = parse_horas_iso(horas_in)
        except ValueError as ve:
            return jsonify({
                'error': str(ve)
            }), 400

        if horas_val <= 0:
            return jsonify({
                'error': 'As horas devem ser superiores a zero.'
            }), 400

        teste = (
            db.session.query(Testes)
            .filter(
                Testes.id == teste_id,
                Testes.ensaio_id == ensaio_id
            )
            .with_for_update()
            .first()
        )

        if not teste:
            return jsonify({
                'error': 'Teste não encontrado para o ensaio indicado.'
            }), 404

        info = calcular_horas_teste(teste)

        if not info:
            return jsonify({
                'error': 'Não foi possível calcular as horas disponíveis.'
            }), 400

        horas_max = info["horas_max"]
        horas_colocadas = info["horas_colocadas"]
        restantes = info["horas_disponiveis"]
        
        TOLERANCIA_HORAS = 0.05

        if horas_val > (restantes + TOLERANCIA_HORAS):
            return jsonify({
                'error': 'Horas excedem as disponíveis para este teste.',
                'horas_max': horas_max,
                'horas_colocadas': horas_colocadas,
                'horas_disponiveis': restantes
            }), 409

        reg = Horas(
            tecnico_id=user.id,
            data=dia,
            horas=float(horas_val),
            ensaio_id=int(ensaio_id),
            teste_id=int(teste_id),
            obs=obs if obs else None
        )

        db.session.add(reg)

        # grava o registo na sessão antes do cálculo
        db.session.flush()

        info = atualizar_horasesgotadas(teste.id)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Horas inseridas com sucesso.',
            'horas_max': info["horas_max"],
            'horas_colocadas': info["horas_colocadas"],
            'horas_disponiveis': info["horas_disponiveis"]
        }), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({
            'error': f'Erro ao inserir horas: {str(e)}'
        }), 500
    