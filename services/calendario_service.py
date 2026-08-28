from datetime import date, timedelta
from calendar import monthrange

from app.models import UserCalendar, Feriado


def obter_periodo_mes(ano, mes, ate_hoje=False):

    hoje = date.today()

    ultimo_dia = monthrange(ano, mes)[1]

    if ate_hoje and ano == hoje.year and mes == hoje.month:
        ultimo_dia = hoje.day

    return (
        date(ano, mes, 1),
        date(ano, mes, ultimo_dia)
    )


def obter_feriados_mes(data_ini, data_fim):

    return {
        f.data
        for f in Feriado.query.filter(
            Feriado.data >= data_ini,
            Feriado.data <= data_fim
        ).all()
    }


def obter_calendario_utilizador(tecnico_id, data_ini, data_fim):

    return {
        r.data: r
        for r in UserCalendar.query.filter(
            UserCalendar.user_id == tecnico_id,
            UserCalendar.data >= data_ini,
            UserCalendar.data <= data_fim
        ).all()
    }


def horas_previstas_dia(
    dia,
    horasdia,
    calendario,
    feriados
):

    reg = calendario.get(dia)

    if reg and reg.tipo == "trabalhou":
        return float(reg.horas or horasdia)

    if dia.weekday() >= 5:
        return 0

    if dia in feriados:
        return 0

    if reg:

        if reg.tipo in ("ferias", "falta"):
            return 0

        if reg.tipo == "parcial":
            return float(reg.horas or 0)

    return float(horasdia)


def calcular_horas_previstas(
    tecnico_id,
    ano,
    mes,
    horasdia,
    ate_hoje=False
):

    data_ini, data_fim = obter_periodo_mes(
        ano,
        mes,
        ate_hoje
    )

    feriados = obter_feriados_mes(
        data_ini,
        data_fim
    )

    calendario = obter_calendario_utilizador(
        tecnico_id,
        data_ini,
        data_fim
    )

    total = 0

    dia = data_ini

    while dia <= data_fim:

        total += horas_previstas_dia(
            dia,
            horasdia,
            calendario,
            feriados
        )

        dia += timedelta(days=1)

    return round(total, 2)