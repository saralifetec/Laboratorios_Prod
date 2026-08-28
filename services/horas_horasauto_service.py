from datetime import date, datetime, timedelta
from sqlalchemy import or_, func
from app.models import ConfHorasAuto, Ensaio, Horas, HorasAuto, HorasAutoExecucao, Templatenormas, Testes, User
from services.horasauto_services import gerar_resumo_periodo
from app import db

def obter_periodos_disponiveis():

    config = HorasAuto.query.first()

    if not config or not config.dia_inicio:
        return {
            "periodos": [],
            "periodo_default": None
        }

    hoje = date.today()

    periodos = []

    current_start = config.dia_inicio

    while True:

        current_end = current_start + timedelta(days=6)

        # só períodos completos
        if current_end >= hoje:
            break

        periodos.append({
            "ano": current_start.year,
            "mes": current_start.month,
            "inicio": current_start.isoformat(),
            "fim": current_end.isoformat()
        })

        current_start += timedelta(days=7)

        periodo_default = periodos[-1] if periodos else None

    return {
        "periodos": periodos,
        "periodo_default": periodo_default
    }

def obter_preview_periodo(start, end):
    """
    Devolve o resumo de um único período.
    """

    resumo = gerar_resumo_periodo(
        start,
        end
    )

    return {
        "start": start.isoformat(),
        "end": end.isoformat(),
        "resumo": resumo
    }

def obter_historico_exportacoes():

    """
        Histórico de exportações já realizadas
    """

    exportacoes = (
        HorasAutoExecucao.query
        .outerjoin(User)
        .order_by(
            HorasAutoExecucao.data_execucao.desc()
        )
        .all()
    )

    resultado = []

    for exp in exportacoes:

        resultado.append({
            "id": exp.id,
            "data_execucao": (
                exp.data_execucao.strftime('%Y-%m-%d')
                if exp.data_execucao else ''
            ),
            "data_inicio": (
                exp.data_inicio.strftime('%Y-%m-%d')
                if exp.data_inicio else ''
            ),
            "data_fim": (
                exp.data_fim.strftime('%Y-%m-%d')
                if exp.data_fim else ''
            ),
            "utilizador": (
                exp.user.full_name
                if exp.user else ''
            ),
            "anular": (
                f"<i class='fas fa-times text-danger "
                f"anular-exportacao' "
                f"data-id='{exp.id}' "
                f"style='cursor:pointer'></i>"
            )
        })

    return resultado

def anular_exportacao_horas_auto(execucao_id):

    execucao = HorasAutoExecucao.query.get(
        execucao_id
    )

    if not execucao:

        return {
            "ok": False,
            "error_key": "msg.exportacao_nao_encontrada"
        }

    horas = Horas.query.filter_by(
        execucao_id=execucao_id
    ).all()

    existe_exportada = any(
        h.exportado is not None
        for h in horas
    )

    if existe_exportada:

        return {
            "ok": False,
            "error_key": "msg.exportacao_ja_exportada_sap"
        }

    Horas.query.filter_by(
        execucao_id=execucao_id
    ).delete(
        synchronize_session=False
    )

    db.session.delete(execucao)

    atualizar_horasesgotadas()

    db.session.commit()

    return {
        "ok": True
    }

def calcular_total_disponivel():

    total_disponivel = 0

    testes = Testes.query.filter_by(
        horasesgotadas=0
    ).all()

    horas_por_teste = dict(
        db.session.query(
            Horas.teste_id,
            db.func.sum(Horas.horas)
        )
        .filter(
            or_(
                Horas.extra.is_(False),
                Horas.extra.is_(None)
            )
        )
        .group_by(Horas.teste_id)
        .all()
    )

    for teste in testes:

        ensaio = Ensaio.query.get(teste.ensaio_id)

        if not ensaio or not ensaio.norma_id:
            continue

        tpl = Templatenormas.query.filter_by(
            norma_id=ensaio.norma_id,
            teste_id=teste.teste_id
        ).first()

        if not tpl:
            continue

        horas_max = (
            (tpl.duracaomontagem or 0)
            +
            ((tpl.tempopp or 0) * (teste.qtd or 0))
        )

        usadas = horas_por_teste.get(teste.id, 0)

        total_disponivel += max(
            horas_max - usadas,
            0
        )

    return round(total_disponivel, 2)

def calcular_tarefas(periodos):

    tarefas = []
    total_gerar = 0

    for periodo in periodos:

        resumo = periodo["resumo"]

        for user_id, user in resumo.items():

            #  FILTRO
            if user.get("pepnet") != "network":
                continue

            for dia, info in user["dias"].items():

                horas = info.get("n_gerar", 0)

                if horas > 0:
                    tarefas.append({
                        "user_id": int(user_id),
                        "data": dia,
                        "horas": horas
                    })

                    total_gerar += horas

    return tarefas, round(total_gerar, 2)

def calcular_disponibilidade_por_teste():

    disponibilidade = {}

    # horas já colocadas por teste (OTIMIZADO)
    horas_por_teste = dict(
        db.session.query(
            Horas.teste_id,
            db.func.sum(Horas.horas)
        )
        .filter(or_(Horas.extra.is_(False), Horas.extra.is_(None)))
        .group_by(Horas.teste_id)
        .all()
    )

    ensaios = Ensaio.query.filter_by(anulado=False).all()

    for ensaio in ensaios:

        if not ensaio.norma_id:
            continue

        templates = Templatenormas.query.filter_by(norma_id=ensaio.norma_id).all()
        template_map = {t.teste_id: t for t in templates}

        testes = Testes.query.filter_by(ensaio_id=ensaio.id).all()

        for teste in testes:

            tpl = template_map.get(teste.teste_id)
            if not tpl:
                continue

            num_pecas = teste.qtd or 0

            horas_max = (tpl.duracaomontagem or 0) + ((tpl.tempopp or 0) * num_pecas)

            usadas = horas_por_teste.get(teste.id, 0)

            disponivel = max(horas_max - usadas, 0)

            if disponivel > 0:

                disponibilidade[teste.id] = {
                    "teste": teste,
                    "disponivel": float(disponivel)
                }

    return disponibilidade


def distribuir_horas(tarefas, disponibilidade):

    inserts = []

    #  normalizar tarefas
    tarefas_pendentes = [
        {
            "user_id": t["user_id"],
            "data": t["data"],
            "horas": float(t["horas"])
        }
        for t in tarefas
    ]

    #  função para normalizar datas
    def parse_data(valor):

        if not valor:
            return datetime.max

        if isinstance(valor, datetime):
            return valor

        if isinstance(valor, str):
            try:
                return datetime.fromisoformat(valor)
            except:
                return datetime.max

        return datetime.max


    #  ordenação segura
    def ordenar_teste(item):

        t = item["teste"]

        datafim = parse_data(t.datafim)
        datainicio = parse_data(t.datainicio)

        return (
            0 if t.datafim else 1,
            datafim,
            datainicio
        )


    #  ordenar testes
    lista_testes = sorted(disponibilidade.values(), key=ordenar_teste)


    #  distribuição
    for info in lista_testes:

        disp = float(info["disponivel"])
        teste = info["teste"]

        idx = 0  #  índice rotativo (round-robin)

        while disp > 0 and tarefas_pendentes:

            tarefa = tarefas_pendentes[idx]

            user_id = tarefa["user_id"]
            data = tarefa["data"]
            horas_faltam = tarefa["horas"]

            usar = min(1, disp, horas_faltam)

            data_dt = datetime.strptime(data, "%Y-%m-%d").date()

            inserts.append({
                "tecnico_id": user_id,
                "data": data_dt,
                "horas": round(usar, 2),
                "teste_id": teste.id,
                "ensaio_id": teste.ensaio_id
            })

            disp -= usar
            tarefa["horas"] -= usar

            #  se tarefa acabou → remover
            if tarefa["horas"] <= 0:
                tarefas_pendentes.pop(idx)

                # ajustar índice
                if tarefas_pendentes:
                    idx = idx % len(tarefas_pendentes)
                continue

            #  passar para próxima pessoa
            idx = (idx + 1) % len(tarefas_pendentes)

        info["disponivel"] = disp


    return inserts

def calcular_tarefas_gerais(periodos):

    tarefas = []

    for periodo in periodos:

        resumo = periodo["resumo"]

        for user_id, user in resumo.items():

            if user.get("pepnet") != "network":
                continue

            for dia, info in user["dias"].items():

                horas = info.get("g_gerar", 0)

                if horas > 0:
                    tarefas.append({
                        "user_id": int(user_id),
                        "data": dia,
                        "horas": float(horas)
                    })

    return tarefas

def obter_codigosg_por_user():

    resultado = {}

    configs = ConfHorasAuto.query.all()

    for conf in configs:

        codigos = [
            c.codigog_id
            for c in conf.codigosg
        ]

        if codigos:
            resultado[conf.tecnico_id] = codigos

    return resultado

def distribuir_horas_gerais(tarefas, codigos_por_user):

    inserts = []

    for tarefa in tarefas:

        user_id = tarefa["user_id"]
        data = tarefa["data"]
        horas = tarefa["horas"]

        codigos = codigos_por_user.get(user_id, [])

        if not codigos:
            continue  # sem códigos → ignora

        num_codigos = len(codigos)

        #  dividir equitativamente
        base = horas / num_codigos

        data_dt = datetime.strptime(data, "%Y-%m-%d").date()

        for codg_id in codigos:

            inserts.append({
                "tecnico_id": user_id,
                "data": data_dt,
                "horas": round(base, 2),
                "codigog_id": codg_id
            })

    return inserts

def calcular_tarefas_pep(periodos):

    tarefas = []

    for periodo in periodos:

        resumo = periodo["resumo"]

        for user_id, user in resumo.items():

            if user.get("pepnet") != "pep":
                continue

            for dia, info in user["dias"].items():

                tarefas.append({
                    "user_id": int(user_id),
                    "data": dia,
                    "n_gerar": info.get("n_gerar", 0),
                    "g_gerar": info.get("g_gerar", 0)
                })

    return tarefas

def distribuir_ensaios_pep(tarefas):

    inserts = []

    #  cache para performance (importantíssimo)
    cache_network = {}

    for tarefa in tarefas:

        user_id = tarefa["user_id"]
        data = tarefa["data"]
        data_dt = datetime.strptime(data, "%Y-%m-%d").date()

        n_gerar = tarefa["n_gerar"]

        if n_gerar <= 0:
            continue

        #  usar cache (evita N queries por dia)
        if data_dt not in cache_network:
            cache_network[data_dt] = obter_horas_network_por_ensaio(data_dt)

        horas_network = cache_network[data_dt]

        total_network = sum(horas_network.values())

        if total_network <= 0:
            continue

        total_distribuido = 0
        inserts_user = []

        for ensaio_id, horas_net in horas_network.items():

            proporcao = horas_net / total_network

            horas_novas = round(n_gerar * proporcao, 2)

            if horas_novas <= 0:
                continue

            inserts_user.append({
                "tecnico_id": user_id,
                "data": data_dt,
                "horas": horas_novas,
                "ensaio_id": ensaio_id,
                "teste_id": None
            })

            total_distribuido += horas_novas

        #  CORREÇÃO DE ARREDONDAMENTO
        diff = round(n_gerar - total_distribuido, 2)

        if diff != 0 and inserts_user:
            inserts_user[-1]["horas"] += diff

        inserts.extend(inserts_user)

    return inserts

def obter_horas_network_por_ensaio(data):

  
    resultados = db.session.query(
        Horas.ensaio_id,
        func.sum(Horas.horas)
    ).join(User).join(ConfHorasAuto).filter(

        Horas.data == data,
        Horas.ensaio_id.isnot(None),

        #  só NETWORK
        ConfHorasAuto.pepnet == "network"

    ).group_by(Horas.ensaio_id).all()

    return {
        r[0]: float(r[1]) for r in resultados if r[0]
    }

def distribuir_gerais_pep(tarefas, codigos_por_user):

    inserts = []

    for tarefa in tarefas:

        user_id = tarefa["user_id"]
        data = tarefa["data"]
        data_dt = datetime.strptime(data, "%Y-%m-%d").date()

        g_gerar = tarefa.get("g_gerar", 0)

        if g_gerar <= 0:
            continue

        codigos = codigos_por_user.get(user_id, [])

        if not codigos:
            continue

        base = g_gerar / len(codigos)

        for codg_id in codigos:

            inserts.append({
                "tecnico_id": user_id,
                "data": data_dt,
                "horas": round(base, 2),
                "codigog_id": codg_id
            })

    return inserts

def inserir_horas(inserts, execucao_id):

    for ins in inserts:

        h = Horas(
            tecnico_id=ins["tecnico_id"],
            data=ins["data"],
            horas=ins["horas"],
            ensaio_id=ins["ensaio_id"],
            teste_id=ins["teste_id"],
            obs=f"Gerado automaticamente (execução {execucao_id})",
            auto=True,
            execucao_id=execucao_id
        )

        db.session.add(h)

    return len(inserts)

def inserir_horas_gerais(inserts, execucao_id):

    for ins in inserts:

        h = Horas(
            tecnico_id=ins["tecnico_id"],
            data=ins["data"],
            horas=ins["horas"],
            codigog_id=ins["codigog_id"],
            ensaio_id=None,
            teste_id=None,
            obs=f"Gerado automaticamente (execução {execucao_id})",
            auto=True,
            execucao_id=execucao_id
        )

        db.session.add(h)

    return len(inserts)

def inserir_horas_pep(inserts, execucao_id):

    for ins in inserts:

        h = Horas(
            tecnico_id=ins["tecnico_id"],
            data=ins["data"],
            horas=ins["horas"],
            ensaio_id=ins.get("ensaio_id"),
            teste_id=ins.get("teste_id"),
            codigog_id=ins.get("codigog_id"),
            obs=f"Gerado automaticamente (execução {execucao_id})",
            auto=True,
            execucao_id=execucao_id  
        )

        db.session.add(h)

    return len(inserts)

def atualizar_horasesgotadas():
    """
    Atualiza o campo horasesgotadas de todos os testes.
    """

    horas_por_teste = dict(
        db.session.query(
            Horas.teste_id,
            db.func.sum(Horas.horas)
        )
        .filter(
            or_(
                Horas.extra.is_(False),
                Horas.extra.is_(None)
            )
        )
        .group_by(Horas.teste_id)
        .all()
    )

    testes = Testes.query.all()

    for teste in testes:

        ensaio = Ensaio.query.get(teste.ensaio_id)

        if not ensaio or not ensaio.norma_id:

            teste.horasesgotadas = False
            continue

        tpl = Templatenormas.query.filter_by(
            norma_id=ensaio.norma_id,
            teste_id=teste.teste_id
        ).first()

        if not tpl:

            teste.horasesgotadas = False
            continue

        num_pecas = teste.qtd or 0

        horas_max = (
            (tpl.duracaomontagem or 0)
            +
            ((tpl.tempopp or 0) * num_pecas)
        )

        horas_usadas = horas_por_teste.get(
            teste.id,
            0
        ) or 0

        horas_disponiveis = horas_max - horas_usadas

        teste.horasesgotadas = (
            horas_disponiveis <= 0.01
        )


def ano_data(valor):

    if not valor:
        return None

    if isinstance(valor, str):

        if valor.startswith('0000-00-00'):
            return None

        try:
            return datetime.fromisoformat(
                valor
            ).year
        except Exception:
            return None

    try:
        return valor.year
    except Exception:
        return None



def atualizar_horasesgotadas_teste(teste_id):

    teste = Testes.query.get(teste_id)

    if not teste:
        return None

    info = calcular_horas_teste(teste)

    if not info:
        return None

    print("TESTE:", teste.id, "ESGOTADO:", teste.horasesgotadas)

    teste.horasesgotadas = info["horasesgotadas"]

    return info

def calcular_horas_teste(teste):

    if not teste.ensaio or not teste.ensaio.norma_id:
        return None

    template = (
        Templatenormas.query
        .filter_by(
            norma_id=teste.ensaio.norma_id,
            teste_id=teste.teste_id
        )
        .first()
    )

    if not template:
        return None

    qtd = teste.qtd or 0

    horas_max = (
        (template.duracaomontagem or 0)
        + ((template.tempopp or 0) * qtd)
    )

    horas_colocadas = (
        db.session.query(
            db.func.coalesce(
                db.func.sum(Horas.horas),
                0
            )
        )
        .filter(
            Horas.teste_id == teste.id,
            or_(
                Horas.extra.is_(False),
                Horas.extra.is_(None)
            )
        )
        .scalar()
    )

    TOLERANCIA_HORAS = 0.05

    horas_disponiveis = round(
        horas_max - horas_colocadas,
        2
    )

    if horas_disponiveis < TOLERANCIA_HORAS:
        horas_disponiveis = 0

    horas_disponiveis = max(0, horas_disponiveis)

    return {
        "horas_max": round(horas_max, 2),
        "horas_colocadas": round(horas_colocadas, 2),
        "horas_disponiveis": horas_disponiveis,
        "horasesgotadas": 1 if horas_disponiveis == 0 else 0
    }

