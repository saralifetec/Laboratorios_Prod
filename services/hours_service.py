from datetime import timedelta
from app import db
from app.models import (
    ConfHorasAuto,
    Ensaio,
    Horas,
    User,
    UserCalendar,
    Feriado
)

def get_tipo_exportacao_hora(hora, configs):
    """
    Determina o tipo de exportação da hora.

    Prioridade:
    1. Hora.tipo
    2. ConfHorasAuto.pepnet
    """

    if hora.tipo:
        return hora.tipo.strip().upper()

    conf = configs.get(hora.tecnico_id)

    if conf and conf.pepnet:
        return conf.pepnet.strip().upper()

    return None

def get_horas_previstas_periodo(user_id, data_inicio, data_fim):
    """
    Calcula as horas previstas de um utilizador para um determinado período.

    Regras:
    - O calendário do utilizador tem prioridade máxima.
    - Se existir registo em UserCalendar:
        - trabalhou -> horasdia
        - parcial   -> horas definidas no calendário
        - falta     -> 0
        - ferias    -> 0
        - feriado   -> 0
    - Se não existir registo em UserCalendar:
        - sábado/domingo -> 0
        - feriado global -> 0
        - restantes dias -> horasdia

    Args:
        user_id (int):
            ID do utilizador.

        data_inicio (date):
            Data inicial do período.

        data_fim (date):
            Data final do período.

    Returns:
        dict:
            Dicionário com a data e respetivas horas previstas.

            Exemplo:
            {
                date(2026, 9, 1): 8,
                date(2026, 9, 2): 8,
                date(2026, 9, 3): 4,
                date(2026, 9, 4): 0,
            }
    """

    # Configuração do colaborador
    conf = ConfHorasAuto.query.filter_by(
        tecnico_id=user_id
    ).first()

    if not conf:
        return {}

    horas_dia = conf.horasdia or 0

    # Calendário pessoal no período
    calendar_entries = UserCalendar.query.filter(
        UserCalendar.user_id == user_id,
        UserCalendar.data >= data_inicio,
        UserCalendar.data <= data_fim
    ).all()

    calendar_map = {
        entry.data: entry
        for entry in calendar_entries
    }

    # Feriados globais do período
    feriados = {
        f.data
        for f in Feriado.query.filter(
            Feriado.data >= data_inicio,
            Feriado.data <= data_fim
        ).all()
    }

    resultado = {}

    dia = data_inicio

    while dia <= data_fim:

        calendar = calendar_map.get(dia)

        # ---------------------------------------------------------
        # 1. Calendário pessoal tem prioridade máxima
        # ---------------------------------------------------------
        if calendar:

            if calendar.tipo == "trabalhou":

                resultado[dia] = horas_dia

            elif calendar.tipo == "parcial":

                resultado[dia] = calendar.horas or 0

            elif calendar.tipo in (
                "falta",
                "ferias",
                "feriado"
            ):

                resultado[dia] = 0

            else:

                resultado[dia] = horas_dia

        # ---------------------------------------------------------
        # 2. Aplicar regras gerais
        # ---------------------------------------------------------
        else:

            # sábado=5 domingo=6
            if dia.weekday() >= 5:

                resultado[dia] = 0

            elif dia in feriados:

                resultado[dia] = 0

            else:

                resultado[dia] = horas_dia

        dia += timedelta(days=1)

    return resultado

def get_registos_horas_periodo(user_id, data_inicio, data_fim):
    """
    Devolve todos os registos da tabela Horas
    para um utilizador e período.
    """

    return Horas.query.filter(
        Horas.tecnico_id == user_id,
        Horas.data >= data_inicio,
        Horas.data <= data_fim
    ).all()

def get_total_horas_inseridas_periodo(user_id, data_inicio, data_fim):
    """
    Devolve o total global tabela Horas
    para um utilizador e período.
    """
    return sum(
        h.horas
        for h in get_registos_horas_periodo(
            user_id,
            data_inicio,
            data_fim
        )
    )

def get_total_horas_gerais_periodo(user_id, data_inicio, data_fim):
    """
    Devolve o total de horas Gerais colocadas
    para um utilizador e período.
    """
    return sum(
        h.horas
        for h in get_registos_horas_periodo(
            user_id,
            data_inicio,
            data_fim
        )
        if h.codigog_id
    )

def get_total_horas_ensaios_periodo(user_id, data_inicio, data_fim):
    """
    Devolve o total de horas em Ensaios colocadas
    para um utilizador e período.
    """
    return sum(
        h.horas
        for h in get_registos_horas_periodo(
            user_id,
            data_inicio,
            data_fim
        )
        if h.ensaio_id or h.manual
    )

def get_resumo_horas_periodo(user_id, data_inicio, data_fim):
    """
    Devolve um resumo das horas do utilizador
    para um determinado período.

    Returns:
    {
        "horas_inseridas": 120,
        "horas_gerais": 25,
        "horas_ensaios": 95,
        "registos": [...]
    }
    """

    registos = get_registos_horas_periodo(
        user_id,
        data_inicio,
        data_fim
    )

    horas_inseridas = sum(
        h.horas
        for h in registos
    )

    horas_gerais = sum(
        h.horas
        for h in registos
        if h.codigog_id
    )

    horas_ensaios = sum(
        h.horas
        for h in registos
        if h.ensaio_id or h.manual
    )

    return {
        "horas_inseridas": round(horas_inseridas, 2),
        "horas_gerais": round(horas_gerais, 2),
        "horas_ensaios": round(horas_ensaios, 2),
        "registos": registos
    }

def get_ultima_exportacao(user_id):
    """
    Devolve a data da última exportação do utilizador.
    """

    ultima = db.session.query(
        db.func.max(Horas.exportado)
    ).filter(
        Horas.tecnico_id == user_id,
        Horas.exportado.isnot(None)
    ).scalar()

    return ultima

def hora_nao_exportada(hora):
    """
    Determina se uma hora ainda não foi exportada.
    """

    if hora.exportado is None:
        return True

    if str(hora.exportado) == "0000-00-00":
        return True

    return False

def get_ensaios_com_horas_bloqueadas_exportacao(laboratorio_id=None):
    """
    Devolve as horas não exportadas bloqueadas
    por falta de PEP ou Network.

    O agrupamento é feito por:
        - ensaio
        - tipo (PEP / NET)

    Assim um mesmo ensaio pode surgir duas vezes.
    """

    query = (
        db.session.query(Horas, Ensaio)
        .join(
            Ensaio,
            Ensaio.id == Horas.ensaio_id
        )
        .filter(
            Horas.ensaio_id.isnot(None)
        )
    )

    if laboratorio_id:
        query = query.filter(
            Ensaio.laboratorio_id == laboratorio_id
        )

    registos = query.all()

    resultado = {}

    # Carregar todas as configurações dos utilizadores
    configs = {
        c.tecnico_id: c
        for c in ConfHorasAuto.query.all()
    }

    for hora, ensaio in registos:

        if not hora_nao_exportada(hora):
            continue

        tipo = get_tipo_exportacao_hora(
            hora,
            configs
        )

        if not tipo:
            continue

        motivo = None

        if tipo == "PEP" and not ensaio.pep:
            motivo = "PEP em falta"

        elif tipo in ("NET", "NETWORK") and not ensaio.network:
            motivo = "Network em falta"

        if not motivo:
            continue

        chave = (
            ensaio.id,
            tipo
        )

        if chave not in resultado:

            resultado[chave] = {
                "ensaio_id": ensaio.id,
                "ensaio": ensaio.ensaio,
                "tipo": tipo,
                "motivo": motivo,
                "horas": 0,
                "link": f"/ensaios?ensaio={ensaio.ensaio}"
            }

        resultado[chave]["horas"] += float(hora.horas)

    for item in resultado.values():
        item["horas"] = round(item["horas"], 2)

    return list(resultado.values())

def delete_horas_ensaio_nao_exportadas(ensaio_id, tipo):
    """
    Elimina as horas não exportadas do tipo indicado
    para o ensaio.
    """

    print("Recebido:", ensaio_id, tipo)

    horas = Horas.query.filter(
        Horas.ensaio_id == ensaio_id
    ).all()


    configs = {
        c.tecnico_id: c
        for c in ConfHorasAuto.query.all()
    }

    horas_a_apagar = []

    for hora in horas:

        if not hora_nao_exportada(hora):
            continue

        tipo_hora = get_tipo_exportacao_hora(
            hora,
            configs
        )

        if tipo_hora == tipo:
            horas_a_apagar.append(hora)


    print("APAGAR:", len(horas_a_apagar))

    for hora in horas_a_apagar:
        db.session.delete(hora)

    db.session.commit()

    return len(horas_a_apagar)
