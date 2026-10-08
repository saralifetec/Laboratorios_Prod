from datetime import date

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
    """
    Insere horas num teste de um ensaio, garantindo que não excede as horas máximas
    definidas pelo template da norma: horas_max = duracaomontagem + (tempopp * qtd_do_teste).
    Verifica novamente no momento do commit (com lock) para evitar concorrência.
    """
    try:
        payload = request.get_json(silent=True) or {}
        user = payload.get('tecnico_id')
        ensaio_id = payload.get('ensaio_id')
        teste_id  = payload.get('teste_id')
        horas_in  = payload.get('horas')
        data_str  = payload.get('data') or payload.get('dia') or payload.get('date')
        obs       = (payload.get('obs') or '').strip()

        # Validações básicas
        if not ensaio_id or not teste_id:
            return jsonify({'error': 'ensaio_id e teste_id são obrigatórios.'}), 400

        # Data é obrigatória no modelo
        try:
            dia = _parse_data_iso(data_str)
        except ValueError as ve:
            return jsonify({'error': str(ve)}), 400

        try:
            horas_val = _parse_horas(horas_in)
        except ValueError as ve:
            return jsonify({'error': str(ve)}), 400


        if horas_val <= 0:
            return jsonify({'error': 'As horas devem ser superiores a zero.'}), 400


        print("ENSAIO_ID:", ensaio_id)
        print("TESTE_ID:", teste_id)
        # 1) Bloquear a linha do teste para evitar corrida (precisa InnoDB e transação)
        teste = (db.session.query(Testes)
                .filter(Testes.id == teste_id, Testes.ensaio_id == ensaio_id)
                .with_for_update()
                .first())

        if not teste:
            return jsonify({'error': 'Teste não encontrado para o ensaio indicado.'}), 404
        print("TESTE ENCONTRADO:", teste)
        ensaio = teste.ensaio
        if not ensaio or not ensaio.norma_id:
            return jsonify({'error': 'O ensaio não tem norma associada. Não é possível calcular horas máximas.'}), 400

        # 2) Obter template desta norma para este tipo de teste
        tpl = (Templatenormas.query
            .filter_by(norma_id=ensaio.norma_id, teste_id=teste.teste_id)
            .first())
        if not tpl:
            return jsonify({'error': 'Teste não existe no template da norma do ensaio.'}), 400

   
        qtd_pecas = teste.qtd or 0
        horas_max = (tpl.duracaomontagem or 0.0) + ((tpl.tempopp or 0.0) * qtd_pecas)

        # 3) Recalcular horas já colocadas (no momento, dentro do lock/mesma transação)
        horas_colocadas = (
            db.session.query(func.sum(Horas.horas))
            .filter(Horas.teste_id == teste.id)
            .filter(or_(Horas.extra.is_(False), Horas.extra.is_(None)))
            .scalar()
        ) or 0.0

        restantes = round(horas_max - horas_colocadas, 4)

        if horas_val > restantes + 1e-9:
            # Conflito: alguém pode ter lançado horas entretanto
            return jsonify({
                'error': 'Horas excedem as disponíveis para este teste.',
                'horas_max': round(horas_max, 2),
                'horas_colocadas': round(horas_colocadas, 2),
                'horas_disponiveis': round(max(0.0, restantes), 2)
            }), 409

        # 4) Inserir horas — técnico é SEMPRE o utilizador autenticado
        reg = Horas(
            tecnico_id=user,
            data=dia,
            horas=float(horas_val),
            ensaio_id=int(ensaio_id),
            teste_id=int(teste_id),
            obs=obs if obs else None
        )
        db.session.add(reg)
        db.session.commit()

        # 5) Devolver totals atualizados
        novas_colocadas = horas_colocadas + float(horas_val)
        novas_disp = max(0.0, horas_max - novas_colocadas)

        return jsonify({
            'success': True,
            'message': 'Horas inseridas com sucesso.',
            'horas_max': round(horas_max, 2),
            'horas_colocadas': round(novas_colocadas, 2),
            'horas_disponiveis': round(novas_disp, 2)
        }), 201

    except Exception as e:
        db.session.rollback()
        # Opcional: current_app.logger.exception("Erro ao inserir horas")
        return jsonify({'error': f'Erro ao inserir horas: {str(e)}'}), 500


def _parse_horas(value):
    """
    Converte '2.5' -> 2.5, '2,5' -> 2.5, '02:30' -> 2.5
    Levanta ValueError se inválido.
    """
    if value is None:
        raise ValueError("Valor de horas vazio.")
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip()
    if not s:
        raise ValueError("Valor de horas vazio.")
    if ":" in s:
        try:
            h_str, m_str = s.split(":")
            h = int(h_str)
            m = int(m_str)
            if h < 0 or m < 0 or m >= 60:
                raise ValueError
            return h + (m / 60.0)
        except Exception:
            raise ValueError("Formato de horas inválido. Use HH:MM (ex.: 02:30).")
    else:
        # suporta vírgula decimal
        s = s.replace(",", ".")
        try:
            v = float(s)
            return v
        except Exception:
            raise ValueError("Formato de horas inválido. Use número (ex.: 2.5) ou HH:MM (ex.: 02:30).")


def _parse_data_iso(dstr):
    """
    Converte 'YYYY-MM-DD' em date. Levanta ValueError se inválido.
    """
    if not dstr:
        raise ValueError("Data é obrigatória.")
    try:
        return date.fromisoformat(dstr)
    except Exception:
        raise ValueError("Formato de data inválido. Use YYYY-MM-DD.")