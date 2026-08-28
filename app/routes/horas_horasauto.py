from datetime import date

from flask import Blueprint, jsonify, render_template, request, session
from sqlalchemy import or_
from app.models import Ensaio, HorasAuto, HorasAutoExecucao, Testes, Tipotestes, User, db
from app.routes.geral import login_required
from app.utils.datas import formatar_data
from services.horas_horasauto_service import anular_exportacao_horas_auto, atualizar_horasesgotadas, atualizar_horasesgotadas_teste, calcular_tarefas_pep, calcular_total_disponivel, calcular_disponibilidade_por_teste, calcular_tarefas, calcular_tarefas_gerais, distribuir_ensaios_pep, distribuir_gerais_pep, distribuir_horas, distribuir_horas_gerais, inserir_horas, inserir_horas_gerais, inserir_horas_pep, obter_codigosg_por_user, obter_historico_exportacoes, obter_periodos_disponiveis, obter_preview_periodo
from services.horas_pessoa_service import obter_horas_mensais


horas_horasauto_bp = Blueprint('horas_horasauto', __name__)


@horas_horasauto_bp.route('/horasauto')
@login_required
def horas_horasauto():

    """
        Página para gerar horas automáticamente para todos
    """

    user = User.query.get(session['user_id'])

    config = HorasAuto.query.first()

    if not config or not config.ativo:
        return render_template('404.html'), 404

    if user.funcao_id not in [2, 3]:
        return render_template('403.html'), 403

    return render_template(
        'horas_horasauto.html',
        user=user
    )

@horas_horasauto_bp.route('/periodos')
def periodos_historico():

    """
        Preencher ano, mês e semana, no início da página
    """

    return jsonify(
        obter_periodos_disponiveis()
    )


@horas_horasauto_bp.route('/preview_periodo', methods=['GET'])
def preview_periodo():

    """
        Primeira tabela resumo da função gerar horas
    """

    start = request.args.get("start")
    end = request.args.get("end")

    if not start or not end:
        return jsonify({
            "ok": False,
            "error": "missing_dates"
        })

    data = obter_preview_periodo(
        date.fromisoformat(start),
        date.fromisoformat(end)
    )

    return jsonify({
        "ok": True,
        "resumo": data
    })

@horas_horasauto_bp.route('/historico_exportacoes')
def historico_exportacoes():

    """
        Tabela com o histórico das exportações
    """

    return jsonify(
        obter_historico_exportacoes()
    )

@horas_horasauto_bp.route('/anular/<int:execucao_id>',methods=['DELETE'])
def anular_exportacao(execucao_id):

    return jsonify(
        anular_exportacao_horas_auto(
            execucao_id
        )
    )

@horas_horasauto_bp.route('/disponivel')
def horas_disponiveis():

    return jsonify({
        "total": calcular_total_disponivel()
    })

@horas_horasauto_bp.route('/gerar', methods=['POST'])
def gerar_horasauto():

    try:

        progresso["percentagem"] = 0
        progresso["texto"] = "msg.a_iniciar"

        data = request.get_json()

        periodos = data.get("periodos")

        if not periodos:
            return jsonify({
                "ok": False,
                "error": "no_data"
            }), 400

        # =====================================================
        # NETWORK ENSAIOS
        # =====================================================

        progresso["percentagem"] = 10
        progresso["texto"] = "msg.calcular_tarefas_network"

        tarefas, total_gerar = calcular_tarefas(periodos)

        progresso["percentagem"] = 20
        progresso["texto"] = "msg.calcular_disponibilidade"

        disponibilidade = calcular_disponibilidade_por_teste()

        progresso["percentagem"] = 30
        progresso["texto"] = "msg.distribuir_horas_network"

        inserts = distribuir_horas(
            tarefas,
            disponibilidade
        )

        # =====================================================
        # NETWORK GERAIS
        # =====================================================

        progresso["percentagem"] = 40
        progresso["texto"] = "msg.distribuir_horas_gerais"

        tarefas_g = calcular_tarefas_gerais(periodos)

        codigos_por_user = obter_codigosg_por_user()

        inserts_g = distribuir_horas_gerais(
            tarefas_g,
            codigos_por_user
        )

        # =====================================================
        # CRIAR EXECUÇÃO
        # =====================================================

        progresso["percentagem"] = 50
        progresso["texto"] = "msg.criar_execucao"

        start = date.fromisoformat(
            periodos[0]["start"]
        )

        end = date.fromisoformat(
            periodos[0]["end"]
        )

        execucao = HorasAutoExecucao(
            data_execucao=date.today(),
            data_inicio=start,
            data_fim=end,
            user_id=session["user_id"]
        )

        db.session.add(execucao)
        db.session.flush()

        # =====================================================
        # INSERIR NETWORK
        # =====================================================

        progresso["percentagem"] = 60
        progresso["texto"] = "msg.inserir_horas_network"

        total_network = inserir_horas(
            inserts,
            execucao.id
        )

        total_gerais = inserir_horas_gerais(
            inserts_g,
            execucao.id
        )

        # =====================================================
        # PEP
        # =====================================================

        progresso["percentagem"] = 70
        progresso["texto"] = "msg.distribuir_horas_pep"

        tarefas_pep = calcular_tarefas_pep(periodos)

        inserts_pep_ensaios = distribuir_ensaios_pep(
            tarefas_pep
        )

        inserts_pep_gerais = distribuir_gerais_pep(
            tarefas_pep,
            codigos_por_user
        )

        total_pep_ensaios = inserir_horas_pep(
            inserts_pep_ensaios,
            execucao.id
        )

        total_pep_gerais = inserir_horas_pep(
            inserts_pep_gerais,
            execucao.id
        )

        # =====================================================
        # RECALCULAR DISPONIBILIDADES
        # =====================================================

        progresso["percentagem"] = 90
        progresso["texto"] = "msg.recalcular_disponibilidades"

        atualizar_horasesgotadas()

        # =====================================================
        # COMMIT
        # =====================================================

        db.session.commit()

        total_final = (
            total_network +
            total_gerais +
            total_pep_ensaios +
            total_pep_gerais
        )

        progresso["percentagem"] = 100
        progresso["texto"] = "field.concluido"

        return jsonify({
            "ok": True,
            "execucao_id": execucao.id,
            "total_network": total_network,
            "total_gerais": total_gerais,
            "total_pep_ensaios": total_pep_ensaios,
            "total_pep_gerais": total_pep_gerais,
            "total_inserts": total_final
        })

    except Exception as e:

        db.session.rollback()

        progresso["percentagem"] = 100
        progresso["texto"] = "field.erro"

        return jsonify({
            "ok": False,
            "error": str(e)
        })

progresso = {
    "percentagem": 0,
    "texto": ""
}


@horas_horasauto_bp.route('/estado')
def estado():

    return jsonify({
        "percentagem": progresso["percentagem"],
        "texto": progresso["texto"]
    })

@horas_horasauto_bp.route('/testes_disponiveis')
def testes_disponiveis():

    laboratorio_id = request.args.get(
        'laboratorio_id',
        type=int
    )

    texto = (
        request.args.get('texto', '')
        .strip()
    )

    query = (
        Testes.query
        .join(Ensaio)
        .join(Tipotestes)
        .filter(
            Testes.horasesgotadas == 0
        )
    )

    if laboratorio_id:

        query = query.filter(
            Tipotestes.laboratorio_id ==
            laboratorio_id
        )

    if texto:

        query = query.filter(
            Ensaio.ensaio.ilike(
                f"%{texto}%"
            )
        )

    testes = (
        query
        .order_by(
            Ensaio.ensaio
        )
        .all()
    )

    resultado = []

    for teste in testes:

        resultado.append({

            "id": teste.id,

            "selecionar": (
                f"<input "
                f"type='checkbox' "
                f"class='chk-esgotar-teste' "
                f"value='{teste.id}'>"
            ),

            "laboratorio": (
                teste.teste.laboratorio.laboratorio
                if teste.teste
                and teste.teste.laboratorio
                else ""
            ),

            "ensaio": (
                teste.ensaio.ensaio
                if teste.ensaio
                else ""
            ),

            "teste": (
                teste.teste.teste
                if teste.teste
                else ""
            ),

            "datainicio": formatar_data(teste.datainicio),
            "datafim": formatar_data(teste.datafim),

        })

    return jsonify(resultado)

@horas_horasauto_bp.route('/esgotar_testes',methods=['POST'])
def esgotar_testes():

    dados = request.get_json()

    ids = dados.get(
        'testes',
        []
    )

    if not ids:
        return jsonify({
            'success': False,
            'error_key': 'msg.nenhum_teste_selecionado'
        }), 400

    (
        Testes.query
        .filter(
            Testes.id.in_(ids)
        )
        .update(
            {
                Testes.horasesgotadas: 1,
                Testes.esgotadomanualmente: 1
            },
            synchronize_session=False
        )
    )

    db.session.commit()

    return jsonify({
        'success': True
    })

@horas_horasauto_bp.route('/testes_recalcular')
def testes_recalcular():

    laboratorio_id = request.args.get(
        'laboratorio_id',
        type=int
    )

    ano = request.args.get(
        'ano',
        type=int
    )

    incluir_esgotados = (
        request.args.get(
            'incluir_esgotados',
            '0'
        ) == '1'
    )

    query = (
        Testes.query
        .join(Ensaio)
        .join(Tipotestes)
    )

    if laboratorio_id:
        query = query.filter(
            Tipotestes.laboratorio_id ==
            laboratorio_id
        )

    if ano:
        query = query.filter(

            or_(

                Ensaio.concluido.is_(None),

                Ensaio.concluido == '0000-00-00',

                db.extract(
                    'year',
                    Ensaio.concluido
                ) == ano

            )

        )

    if not incluir_esgotados:
        query = query.filter(
            Testes.esgotadomanualmente == 0
        )

    testes = (
        query
        .order_by(
            Ensaio.ensaio
        )
        .all()
    )

    resultado = []

    for teste in testes:

        resultado.append({

            "id": teste.id,

            "selecionar": (
                f"<input "
                f"type='checkbox' "
                f"class='chk-recalcular-teste' "
                f"value='{teste.id}' "
                f"checked>"
            ),

            "laboratorio": (
                teste.teste.laboratorio.laboratorio
                if teste.teste and teste.teste.laboratorio
                else ""
            ),

            "ensaio": (
                teste.ensaio.ensaio
                if teste.ensaio
                else ""
            ),

            "teste": (
                teste.teste.teste
                if teste.teste
                else ""
            ),

            "datainicio": formatar_data(
                teste.datainicio
            ),

            "datafim": formatar_data(
                teste.datafim
            ),

        })

    return jsonify(resultado)


@horas_horasauto_bp.route('/recalcular_testes', methods=['POST'])
def recalcular_testes():

    dados = request.get_json()

    ids = dados.get(
        'testes',
        []
    )

    if not ids:

        return jsonify({
            'success': False,
            'error_key': 'msg.nenhum_teste_selecionado'
        }), 400

    total = 0

    for teste in Testes.query.filter(
        Testes.id.in_(ids)
    ).all():

        info = atualizar_horasesgotadas_teste(
            teste.id
        )

        if info is not None:

            teste.esgotadomanualmente = 0

            total += 1

    db.session.commit()

    return jsonify({
        'success': True,
        'total': total
    })

@horas_horasauto_bp.route('/horas_dia')
def horas_dia():

    try:

        ano = int(request.args.get('ano'))
        mes = int(request.args.get('mes'))
        tecnico_id = int(request.args.get('tecnico_id'))

        resultado = obter_horas_mensais(
            tecnico_id,
            ano,
            mes
        )

        return jsonify(resultado)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


