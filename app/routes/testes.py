
import traceback
from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from .. import db
from app.models import Ensaio, Testes
from services.testes_service import atualizar_horasesgotadas
from app.utils.datas import parse_data
from services.testes_service import calcular_horas_teste
from services.testes_service import atualizar_todos_horasesgotadas


testes_bp = Blueprint('testes', __name__)

@testes_bp.route('/testes/update/<int:id>', methods=['POST'])
def update_teste(id):

    teste = Testes.query.get_or_404(id)

    data = request.json or {}

    qtd_original = teste.qtd

    for field in [
        'ensaio_id',
        'teste_id',
        'ordem',
        'qtd',
        'prefixo',
        'primeirapeca',
        'datainicio',
        'duracao',
        'datafim',
        'maquina_id',
        'obs',
        'user_id',
        'fator',
        'bemprimeira',
        'motivofalhaensaio_id'
    ]:
        if field in data:
            setattr(teste, field, data[field])

    nova_qtd = teste.qtd

    if nova_qtd != qtd_original:
        atualizar_horasesgotadas(id)

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Teste atualizado com sucesso'
    })

@testes_bp.route('/disponiveis')
def testes_disponiveis():

    """
    Retorna os ensaios disponíveis para um laboratório específico ou para todos,
    filtrando apenas os que têm horas disponíveis.
    """
    try:

        lab_id_raw = request.args.get("lab_id")

        try:
            lab_id = (
                int(lab_id_raw)
                if lab_id_raw not in (None, '', 'todos')
                else None
            )
        except (ValueError, TypeError):
            lab_id = None

        query = (
            Testes.query
            .join(Ensaio)
            .filter(
                Ensaio.anulado == False,
                or_(
                    Testes.horasesgotadas == 0,
                    Testes.horasesgotadas.is_(None)
                    )
            )
        )

        if lab_id is not None:
            query = query.filter(
                Ensaio.laboratorio_id == lab_id
            )

        testes = query.all()

        resultados = []

        for teste in testes:

            info = calcular_horas_teste(teste)

            if not info:
                continue

            if info["horas_disponiveis"] <= 0:
                continue

            resultados.append({
                "ensaio": teste.ensaio.ensaio,
                "link": f"/ensaios?ensaio={teste.ensaio.ensaio}",
                "teste": teste.teste.teste,
                "datainicio": (
                    parse_data(teste.datainicio).strftime('%Y-%m-%d')
                    if parse_data(teste.datainicio)
                    else ''
                ),
                "datafim": (
                    parse_data(teste.datafim).strftime('%Y-%m-%d')
                    if parse_data(teste.datafim)
                    else ''
                ),
                "ensaio_id": teste.ensaio.id,
                "teste_id": teste.id,
                "horas_max": info["horas_max"],
                "horas_colocadas": info["horas_colocadas"],
                "horas_disponiveis": info["horas_disponiveis"],
                "inserir": "<i class='far fa-clock inserir-horas' style='cursor:pointer' title='Inserir Horas'></i>"
            })

        return jsonify(resultados)
    except Exception as e:
        traceback.print_exc()
        raise

@testes_bp.route('/recalcular_horasesgotadas')
def recalcular_horasesgotadas():

    """
    Código temporário para marcar os testes antigos com horasesgotadas
    """

    total = atualizar_todos_horasesgotadas()

    return jsonify({
        "success": True,
        "total": total
    })