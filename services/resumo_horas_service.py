from datetime import date, timedelta
from calendar import monthrange
from services.calendario_service import calcular_horas_previstas

from app import db
from app.models import (
    User,
    Horas,
    Codigosg,
    ConfHorasAuto,
    UserCalendar,
    Feriado
)



def obter_resumo_horas(tecnicos, ano, mes):

    hoje = date.today()

    ultimo_dia = monthrange(ano, mes)[1]
    dia_fim = hoje.day if (ano == hoje.year and mes == hoje.month) else ultimo_dia

    data_ini = date(ano, mes, 1)
    data_fim = date(ano, mes, dia_fim)

    result = []

    for tecnico in tecnicos:

        conf = ConfHorasAuto.query.filter_by(
            tecnico_id=tecnico.id
        ).first()

        horasdia = conf.horasdia if conf and conf.horasdia else 0

        horas_previstas = calcular_horas_previstas(
            tecnico.id,
            ano,
            mes,
            horasdia,
            ate_hoje=True
        )

        horas_lancadas = (
            db.session.query(
                db.func.coalesce(db.func.sum(Horas.horas), 0)
            )
            .filter(
                Horas.tecnico_id == tecnico.id,
                Horas.data >= data_ini,
                Horas.data <= data_fim
            )
            .scalar()
            or 0
        )

        horas_gerais = (
            db.session.query(
                db.func.coalesce(db.func.sum(Horas.horas), 0)
            )
            .join(Codigosg, Horas.codigog_id == Codigosg.id)
            .filter(
                Horas.tecnico_id == tecnico.id,
                Horas.data >= data_ini,
                Horas.data <= data_fim,
                Codigosg.codigog.like('E.G7%')
            )
            .scalar()
            or 0
        )

        pct_gerais = (
            horas_gerais / horas_lancadas * 100
            if horas_lancadas else 0
        )

        ultima_exportacao = (
            db.session.query(
                db.func.max(Horas.exportado)
            )
            .filter(
                Horas.tecnico_id == tecnico.id
            )
            .scalar()
        )

        exportacao_alerta = (
            ultima_exportacao is None
            or (hoje - ultima_exportacao).days > 7
        )

        result.append({
            'tecnico': tecnico.full_name,
            'horas_previstas': horas_previstas,
            'horas_lancadas': round(horas_lancadas, 2),
            'percentagem_gerais': round(pct_gerais, 1),
            'limite_gerais': conf.horasgerais if conf and conf.horasgerais is not None else 0,
            'ultima_exportacao': ultima_exportacao.strftime('%Y-%m-%d') if ultima_exportacao else '',
            'exportacao_alerta': exportacao_alerta
        })

    return result

def obter_preview_periodo(start, end):
    """
    Gera o preview de um único período.

    Args:
        start (date)
        end (date)

    Returns:
        dict
    """

    return gerar_resumo_periodo(
        start,
        end
    )