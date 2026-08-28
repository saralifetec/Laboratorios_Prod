from datetime import timedelta
from app import db
from app.models import (
    Horas,
    ConfHorasAuto
)
from services.calendario_service import (
    obter_periodo_mes,
    obter_feriados_mes,
    obter_calendario_utilizador,
    horas_previstas_dia
)


def obter_horas_mensais(tecnico_id, ano, mes):

    conf = ConfHorasAuto.query.filter_by(
        tecnico_id=tecnico_id
    ).first()

    horasdia = conf.horasdia if conf else 8

    data_ini, data_fim = obter_periodo_mes(
        ano,
        mes
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

    registos = (
        db.session.query(Horas)
        .filter(
            Horas.tecnico_id == tecnico_id,
            Horas.data >= data_ini,
            Horas.data <= data_fim
        )
        .all()
    )

    resultado = {}

    for r in registos:

        dia = r.data.day

        resultado[str(dia)] = (
            resultado.get(str(dia), 0)
            + float(r.horas or 0)
        )

    dia = data_ini

    while dia <= data_fim:

        resultado[f"{dia.day}_prev"] = horas_previstas_dia(
            dia,
            horasdia,
            calendario,
            feriados
        )

        dia += timedelta(days=1)

    return resultado