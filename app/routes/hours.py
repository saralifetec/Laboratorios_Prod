from calendar import monthrange
from datetime import date, timedelta
from sqlalchemy.orm import joinedload
from app import db
from flask import Blueprint, jsonify, request
from app.models import ConfHorasAuto, Horas
from services.hours_service import delete_horas_ensaio_nao_exportadas, get_ensaios_com_horas_bloqueadas_exportacao, get_horas_previstas_periodo,  get_resumo_horas_periodo, get_ultima_exportacao
from services.users_service import get_scope_users

hours_bp = Blueprint('hours', __name__)

@hours_bp.route('/horas_calendario')
def horas_calendario():

    try:

        ano = int(request.args.get('ano'))
        mes = int(request.args.get('mes'))
        tecnico_id = int(request.args.get('tecnico_id'))

        data_inicio = date(ano, mes, 1)

        if mes == 12:
            data_fim = date(ano + 1, 1, 1)
        else:
            data_fim = date(ano, mes + 1, 1)

        # horas registadas
        registros = (
            db.session.query(Horas)
            .options(joinedload(Horas.codigog))
            .filter(
                Horas.tecnico_id == tecnico_id,
                Horas.data >= data_inicio,
                Horas.data < data_fim
            )
            .all()
        )

        resultado = {}

        for reg in registros:

            if not reg.data:
                continue

            dia = reg.data.day

            resultado[str(dia)] = (
                resultado.get(str(dia), 0)
                + float(reg.horas or 0)
            )

            codigog_txt = (
                (
                    reg.codigog.codigog
                    if reg.codigog
                    else ''
                ) or ''
            ).strip().upper()

            if codigog_txt.startswith('E.G7'):

                resultado[f'{dia}_g'] = (
                    resultado.get(f'{dia}_g', 0)
                    + float(reg.horas or 0)
                )

        # horas previstas
        previstas = get_horas_previstas_periodo(
            tecnico_id,
            data_inicio,
            data_fim - timedelta(days=1)
        )

        for data_dia, horas_prev in previstas.items():

            resultado[f'{data_dia.day}_prev'] = horas_prev

        return jsonify(resultado)

    except Exception as e:

        return jsonify({
            'error': str(e)
        }), 500

@hours_bp.route('/index/home/resumo_horas')
def resumo_horas():

    laboratorio_id = request.args.get('laboratorio_id', type=int)
    ano = request.args.get('ano', type=int)
    mes = request.args.get('mes', type=int)
    apenas_eu = request.args.get(
        'apenas_eu',
        'false'
    ).lower() == 'true'

    hoje = date.today()

    data_inicio = date(ano, mes, 1)

    if ano == hoje.year and mes == hoje.month:
        data_fim = hoje
    else:
        data_fim = date(
            ano,
            mes,
            monthrange(ano, mes)[1]
        )

    utilizadores = [
        u for u in get_scope_users(
            laboratorio_id,
            apenas_eu
        )
        if not u.obsoleto
    ]

    resultado = []

    for utilizador in utilizadores:

        horas_previstas = sum(
            get_horas_previstas_periodo(
                utilizador.id,
                data_inicio,
                data_fim
            ).values()
        )

        resumo = get_resumo_horas_periodo(
            utilizador.id,
            data_inicio,
            data_fim
        )

        horas_lancadas = resumo["horas_inseridas"]
        horas_gerais = resumo["horas_gerais"]

        percentagem_gerais = round(
            (horas_gerais / horas_lancadas) * 100,
            1
        ) if horas_lancadas else 0

        conf = ConfHorasAuto.query.filter_by(
            tecnico_id=utilizador.id
        ).first()

        limite_gerais = (
            conf.horasgerais
            if conf and conf.horasgerais
            else 0
        )

        ultima_exportacao = get_ultima_exportacao(
            utilizador.id
        )

        exportacao_alerta = False

        if ultima_exportacao:
            exportacao_alerta = (
                date.today() - ultima_exportacao
            ).days > 7

        resultado.append({
            "tecnico": utilizador.full_name,
            "horas_previstas": round(horas_previstas, 2),
            "horas_lancadas": round(horas_lancadas, 2),
            "percentagem_gerais": percentagem_gerais,
            "limite_gerais": limite_gerais,
            "ultima_exportacao": (
                ultima_exportacao.strftime("%d/%m/%Y")
                if ultima_exportacao
                else ""
            ),
            "exportacao_alerta": exportacao_alerta
        })

    return jsonify(resultado)

@hours_bp.route('/index/home/horas_bloqueadas_exportacao')
def horas_bloqueadas_exportacao():

    laboratorio_id = request.args.get(
        'laboratorio_id',
        type=int
    )

    dados = get_ensaios_com_horas_bloqueadas_exportacao(
        laboratorio_id
    )

    return jsonify(dados)


@hours_bp.route('/hours/delete_ensaio_hours/<int:ensaio_id>/<tipo>', methods=['POST'])
def delete_ensaio_hours(ensaio_id, tipo):

    resultado = delete_horas_ensaio_nao_exportadas(
        ensaio_id,
        tipo
    )

    return jsonify({
        "success": True,
        "total_apagadas": resultado["total_apagadas"],
        "emails": resultado["notificacoes"]
    })
