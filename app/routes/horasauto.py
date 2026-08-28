from datetime import datetime, date
from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for
from sqlalchemy import or_
from app.models import Ensaio, Horas, HorasAutoExecucao, Templatenormas, Testes, User, db, HorasAuto
from app.routes.geral import login_required
from services.horasauto_services import calcular_disponibilidade_por_teste, calcular_tarefas, calcular_tarefas_gerais, calcular_tarefas_pep, calcular_total_disponivel, distribuir_ensaios_pep, distribuir_gerais_pep, distribuir_horas, distribuir_horas_gerais, get_or_create_horas_auto, inserir_horas, inserir_horas_gerais, inserir_horas_pep, obter_codigosg_por_user, obter_periodos_historico, obter_preview_horas_auto
from flask import jsonify
from services.testes_service import (
    calcular_total_horas_disponiveis
)


horasauto_bp = Blueprint('horasauto', __name__)




@horasauto_bp.route('/horasauto', methods=['GET', 'POST'])
@login_required
def horasauto():

    """
        Página de configuração da exportação automática de horas.

        Métodos suportados:
            GET:
                - Carrega a página com os dados atuais da configuração
                - Envia para o template:
                    - config (HorasAuto): configuração atual
                    - user (User): utilizador autenticado
                    - tecnicos (list[User]): lista de utilizadores
                    - current_date (str): data atual (YYYY-MM-DD)

            POST:
                - Atualiza a configuração com base nos dados do formulário
                - Guarda os dados na base de dados
                - Mostra mensagem de sucesso
                - Redireciona para a mesma página (refresh padrão Post/Redirect/Get)

        Campos esperados no formulário:
            estadoSwitch (str/bool): indica se a funcionalidade está ativa
            frequencia (str): tipo de frequência (ex: semanal)
            repeticao (int): dia da semana (1=segunda, ..., 7=domingo)
            dia1 (str): data de início no formato "YYYY-MM-DD" (opcional)

        Regras:
            - A configuração é única (obtida ou criada via get_or_create_horas_auto)
            - O campo dia_inicio só é atualizado se fornecido

        Returns:
            GET:
                HTML page (horasauto.html)

            POST:
                Redirect para o mesmo endpoint após guardar dados
        """


    config = get_or_create_horas_auto()
    user = User.query.get(session['user_id'])
    tecnicos = User.query.all()
    current_date = datetime.today().date().isoformat()

    if request.method == 'POST':

        config.ativo = bool(request.form.get("estadoSwitch"))
        config.frequencia = request.form.get("frequencia")
        config.repeticao = int(request.form.get("repeticao"))
        
        dia1 = request.form.get("dia1")
        if dia1:
            config.dia_inicio = datetime.strptime(dia1, "%Y-%m-%d").date()

        db.session.commit()

        flash("Configuração guardada com sucesso", "success")

        return redirect(url_for('horasauto.horasauto'))

    return render_template("horasauto.html", config=config, user=user, tecnicos=tecnicos, current_date=current_date)

@horasauto_bp.route('/save', methods=['POST'])
def save_horasauto():

    """
        Guarda ou atualiza a configuração de exportação automática de horas.

        Endpoint que recebe dados em formato JSON e cria ou atualiza o registo
        único da tabela HorasAuto.

        Regras de funcionamento:
        - Se não existir configuração, é criada uma nova
        - Caso exista, os valores são atualizados
        - O campo dia_inicio é opcional

        Request JSON esperado:
            {
                "ativo": bool,
                "frequencia": str,
                "repeticao": int,   # 1 (segunda) a 7 (domingo)
                "dia1": str | null  # formato "YYYY-MM-DD"
            }

        Campos:
            ativo (bool): Indica se a funcionalidade está ativa
            frequencia (str): Tipo de frequência (ex: semanal)
            repeticao (int): Dia da semana de execução (ISO: 1-7)
            dia1 (str | None): Data de início no formato YYYY-MM-DD

        Returns:
            JSON:
                {
                    "ok": True
                }

        Notes:
            - Assume-se que existe apenas um registo de configuração (singleton)
            - Não faz validação avançada dos dados recebidos
        """


    data = request.get_json()

    config = HorasAuto.query.first()

    if not config:
        config = HorasAuto()
        db.session.add(config)

    # guardar
    config.ativo = bool(data.get("ativo"))
    config.frequencia = data.get("frequencia")
    config.repeticao = int(data.get("repeticao"))

    dia1 = data.get("dia1")
    if dia1:
        config.dia_inicio = datetime.strptime(dia1, "%Y-%m-%d").date()
    else:
        config.dia_inicio = None

    db.session.commit()

    return jsonify({"ok": True})




######## VERIFICAR SE SÃO NECESSÁRIOS

@horasauto_bp.route('/preview', methods=['GET'])
def preview_horasauto():

    data = obter_preview_horas_auto()

    if not data:
        return jsonify({
            "ok": False,
            "error": "not_ready"
        })

    return jsonify({
        "ok": True,
        "periodos": data
    })

@horasauto_bp.route('/disponivel', methods=['GET'])
def horas_disponiveis():
    """
    Retorna o total de horas disponíveis em todos os testes.
    (Versão simplificada para horas auto)
    """

    return jsonify({
        "total": calcular_total_disponivel()
    })


@horasauto_bp.route('/gerar', methods=['POST'])
def gerar_horasauto():

    try:

        data = request.get_json()
        periodos = data.get("periodos")

        if not periodos:
            return jsonify({"ok": False, "error": "no_data"}), 400

        #  extrair datas
        start = periodos[0]["start"]
        end = periodos[0]["end"]

        
        #  1. tarefas NETWORK (ensaios)
        tarefas, total_gerar = calcular_tarefas(periodos)

        #  2. disponibilidade
        total_disponivel = calcular_total_disponivel()

        if total_gerar > total_disponivel + 0.001:
            return jsonify({
                "ok": False,
                "error": "not_enough_hours",
                "gerar": total_gerar,
                "disponivel": total_disponivel
            })

        #  CRIAR EXECUÇÃO (ANTES DE TUDO)
        execucao = HorasAutoExecucao(
            data_execucao=date.today(),
            data_inicio=start,
            data_fim=end
        )

        db.session.add(execucao)
        db.session.flush()  #  importante para obter ID

        #  3. disponibilidade por teste
        disponibilidade = calcular_disponibilidade_por_teste()

        #  4. distribuição ensaios (network)
        inserts = distribuir_horas(tarefas, disponibilidade)

        #  5. inserir ensaios (network)
        total = inserir_horas(inserts, execucao.id)

        #  6. GERAIS (network)
        tarefas_g = calcular_tarefas_gerais(periodos)
        codigos_por_user = obter_codigosg_por_user()

        inserts_g = distribuir_horas_gerais(tarefas_g, codigos_por_user)
        total_g = inserir_horas_gerais(inserts_g, execucao.id)

        #  7. PEP USERS

        tarefas_pep = calcular_tarefas_pep(periodos)

        # ensaios PEP
        inserts_pep_ensaios = distribuir_ensaios_pep(tarefas_pep)

        # gerais PEP
        inserts_pep_gerais = distribuir_gerais_pep(tarefas_pep, codigos_por_user)

        # inserir PEP
        inserir_horas_pep(inserts_pep_ensaios, execucao.id)
        inserir_horas_pep(inserts_pep_gerais, execucao.id)

        total_pep = len(inserts_pep_ensaios) + len(inserts_pep_gerais)

        #  COMMIT ÚNICO FINAL
        db.session.commit()

        total_final = total + total_g + total_pep

        return jsonify({
            "ok": True,
            "execucao_id": execucao.id,
            "total_ensaios": total,
            "total_gerais": total_g,
            "total_pep": total_pep,
            "total_inserts": total_final
        })

    except Exception as e:
        import traceback
        print(traceback.format_exc())

        #  rollback em caso de erro
        db.session.rollback()

        return jsonify({
            "ok": False,
            "error": str(e)
        })
    


@horasauto_bp.route('/periodos')
def periodos_historico():

    return jsonify(
        obter_periodos_historico()
    )





