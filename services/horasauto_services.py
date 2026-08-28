from datetime import datetime, timedelta, date
from sqlalchemy import func, or_
from app.models import Ensaio, Horas, HorasAuto, Templatenormas, Testes, db, HorasAutoExecucao
from datetime import datetime, timedelta, date
from collections import defaultdict
from app.models import User, UserCalendar, Feriado, ConfHorasAuto
from datetime import datetime



def obter_periodos_historico():

    config = HorasAuto.query.first()

    if not config:
        return []

    repeticao = config.repeticao

    hoje = date.today()

    ano_atual = hoje.year

    anos = [ano_atual]

    if hoje.month == 1:
        anos.append(ano_atual - 1)

    resultado = []

    for ano in anos:

        dia = date(ano, 1, 1)

        while dia.year == ano:

            dias_diff = (
                dia.isoweekday() - repeticao
            ) % 7

            inicio = dia - timedelta(days=dias_diff)

            fim = inicio + timedelta(days=6)

            if fim.year > ano and ano != ano_atual:
                break

            resultado.append({
                "ano": ano,
                "mes": inicio.month,
                "inicio": inicio.isoformat(),
                "fim": fim.isoformat()
            })

            dia = fim + timedelta(days=1)

    return resultado

def get_or_create_horas_auto():

    config = HorasAuto.query.first()

    if not config:
        config = HorasAuto(
            ativo=False,
            frequencia="semanal",
            repeticao=2  # segunda por default
        )
        db.session.add(config)
        db.session.commit()

    return config

def verificar_alerta_horas_auto(user):
    """
    Verifica se deve aparecer um alerta para gerar horas automaticamente.
    """

    if user.funcao_id not in [2, 3]:
        return False

    config = HorasAuto.query.first()

    if not config or not config.ativo:
        return False

    today = datetime.today().date()

    if config.dia_inicio and today < config.dia_inicio:
        return False

    #  baseado em períodos completos
    ultimo_fim = calcular_ultimo_fim_valido(config)

    if not ultimo_fim:
        return False

    ultima = HorasAutoExecucao.query.order_by(
        HorasAutoExecucao.data_fim.desc()
    ).first()

    if not ultima:
        return True

    return ultima.data_fim < ultimo_fim


def obter_periodos_pendentes(config):
    """
    Determina todos os períodos semanais (7 dias) ainda não exportados.

    Args:
        config (HorasAuto)

    Returns:
        list[tuple(date, date)]
    """

    if not config or not config.ativo or not config.dia_inicio:
        return []

    ultimo_fim_valido = calcular_ultimo_fim_valido(config)

    if not ultimo_fim_valido:
        return []

    # última execução
    ultima = HorasAutoExecucao.query.order_by(
        HorasAutoExecucao.data_fim.desc()
    ).first()

    if ultima:
        current_start = ultima.data_fim + timedelta(days=1)
    else:
        current_start = config.dia_inicio

    periodos = []

    while True:

        current_end = current_start + timedelta(days=6)

        if current_end > ultimo_fim_valido:
            break

        periodos.append((current_start, current_end))

        current_start += timedelta(days=7)

    return periodos

def calcular_ultimo_fim_valido(config):
    """
    Calcula o último dia até ao qual já existe um ciclo completo fechado.

    Args:
        config (HorasAuto)

    Returns:
        date | None
    """

    if not config or not config.ativo:
        return None

    today = datetime.today().date()

    repeticao = config.repeticao  # 1=segunda ... 7=domingo

    dias_diff = (today.isoweekday() - repeticao) % 7
    last_cycle_day = today - timedelta(days=dias_diff)

    # se ainda é o próprio dia → ciclo ainda não terminou
    if last_cycle_day == today:
        last_cycle_day -= timedelta(days=7)

    # último dia do período gerável
    return last_cycle_day - timedelta(days=1)

def gerar_resumo_periodo(start, end):

    feriados = {
        f.data for f in Feriado.query.filter(
            Feriado.data.between(start, end)
        ).all()
    }

    # configs
    configs = ConfHorasAuto.query.filter_by(auto=True).all()

    conf_map = {c.tecnico_id: c for c in configs}
    user_ids = [c.tecnico_id for c in configs]

    users = {
        u.id: u.full_name for u in User.query.filter(
            User.id.in_(user_ids)
        ).all()
    }

    # calendário
    eventos = UserCalendar.query.filter(
        UserCalendar.user_id.in_(user_ids),
        UserCalendar.data.between(start, end)
    ).all()

    mapa = {(e.user_id, e.data): e for e in eventos}

    #  NOVO: ir buscar horas já inseridas
    horas_registos = Horas.query.filter(
        Horas.tecnico_id.in_(user_ids),
        Horas.data.between(start, end)
    ).all()

    #  NOVO: agrupar horas
    horas_map = {}

    for h in horas_registos:

        key = (h.tecnico_id, h.data)

        if key not in horas_map:
            horas_map[key] = {"n": 0, "g": 0}

        # ENSAIOS
        if h.ensaio_id or (h.manual and not h.manual.startswith("E.G")):
            horas_map[key]["n"] += float(h.horas)

        # GERAIS
        elif h.codigog_id or (h.manual and h.manual.startswith("E.G")):
            horas_map[key]["g"] += float(h.horas)

    resultado = {}

    dias_total = (end - start).days + 1

    for user_id, nome in users.items():

        conf = conf_map.get(user_id)
        horas_dia = conf.horasdia if conf else 0

        percent_g = conf.horasgerais or 0

        resultado[user_id] = {
            "nome": nome,
            "pepnet": conf.pepnet,
            "dias": {}
        }

        for i in range(dias_total):

            dia = start + timedelta(days=i)
            weekday = dia.isoweekday()

            evento = mapa.get((user_id, dia))
            tipo = evento.tipo if evento else "normal"

            horas = 0

            # REGRAS BASE
            if tipo in ["ferias", "falta"]:
                horas = 0

            elif tipo == "parcial":
                horas = evento.horas or 0

            elif weekday >= 6:
                if tipo in ["trabalhou", "parcial"]:
                    horas = horas_dia
                else:
                    horas = 0

            elif dia in feriados:
                if tipo in ["trabalhou", "parcial"]:
                    horas = horas_dia
                else:
                    horas = 0

            else:
                horas = horas_dia

            #  horas já existentes
            registo = horas_map.get((user_id, dia), {"n": 0, "g": 0})

            existente_n = registo["n"]
            existente_g = registo["g"]

            #  necessário
            necessario_total = horas

            necessario_g = round(necessario_total * (percent_g / 100), 2)
            necessario_n = round(necessario_total - necessario_g, 2)

            #  a gerar inicial
            gerar_n = necessario_n - existente_n
            gerar_g = necessario_g - existente_g

            #  compensação cruzada
            if gerar_n < 0:
                gerar_g += gerar_n
                gerar_n = 0

            if gerar_g < 0:
                gerar_n += gerar_g
                gerar_g = 0

            gerar_n = max(gerar_n, 0)
            gerar_g = max(gerar_g, 0)

            resultado[user_id]["dias"][dia.isoformat()] = {
                "total": necessario_total,

                "n_necessario": necessario_n,
                "g_necessario": necessario_g,

                "n_existente": existente_n,
                "g_existente": existente_g,

                "n_gerar": round(gerar_n, 2),
                "g_gerar": round(gerar_g, 2),
            }

    return resultado

def obter_preview_horas_auto():
    """
    Gera preview completo de todos os períodos pendentes.

    Returns:
        list[dict]
        [
            {
                "start": "YYYY-MM-DD",
                "end": "YYYY-MM-DD",
                "resumo": {...}
            }
        ]
    """

    config = HorasAuto.query.first()

    periodos = obter_periodos_pendentes(config)

    resultado = []

    for start, end in periodos:

        resumo = gerar_resumo_periodo(start, end)

        resultado.append({
            "start": start.isoformat(),
            "end": end.isoformat(),
            "resumo": resumo
        })

    return resultado

def calcular_total_disponivel():

    ensaios = Ensaio.query.filter_by(anulado=False).all()

    total_disponivel = 0

    #  1 query em vez de centenas
    horas_por_teste = dict(
        db.session.query(
            Horas.teste_id,
            db.func.sum(Horas.horas)
        )
        .filter(or_(Horas.extra.is_(False), Horas.extra.is_(None)))
        .group_by(Horas.teste_id)
        .all()
    )

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

            #  já otimizado
            horas_colocadas = horas_por_teste.get(teste.id, 0)

            horas_disp = horas_max - horas_colocadas

            if horas_disp > 1e-6:
                total_disponivel += horas_disp

    return round(total_disponivel, 2)

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

    db.session.commit()

    return len(inserts)

def validar_disponibilidade(total_gerar, total_disponivel):

    return total_gerar <= (total_disponivel + 0.001)

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

    db.session.commit()

    return len(inserts)

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

def obter_horas_por_ensaio(user_id, data):

    resultados = db.session.query(
        Horas.ensaio_id,
        func.sum(Horas.horas)
    ).filter(
        Horas.tecnico_id == user_id,
        Horas.data == data,
        Horas.ensaio_id.isnot(None)
    ).group_by(Horas.ensaio_id).all()

    return {
        r[0]: float(r[1]) for r in resultados if r[0]
    }

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

def pode_ver_horas_auto(user):

    config = HorasAuto.query.first()

    if not config or not config.ativo:
        return False

    return user.funcao_id in [2, 3]


from datetime import date, timedelta


def obter_periodos_historico():

    config = HorasAuto.query.first()

    if not config or not config.ativo:
        return {
            "periodos": [],
            "periodo_default": None
        }

    hoje = date.today()

    periodos = []

    current_start = config.dia_inicio

    while True:

        current_end = current_start + timedelta(days=6)

        if current_end >= hoje:
            break

        periodos.append({
            "ano": current_start.year,
            "mes": current_start.month,
            "inicio": current_start.isoformat(),
            "fim": current_end.isoformat()
        })

        current_start += timedelta(days=7)


    periodo_default = None

    for p in reversed(periodos):
       
        fim = date.fromisoformat(p["fim"])
       
        if fim < hoje:
        
            periodo_default = {
                "ano": p["ano"],
                "mes": p["mes"],
                "inicio": p["inicio"],
                "fim": p["fim"]
            }
            break

    return {
        "periodos": periodos,
        "periodo_default": periodo_default
    }