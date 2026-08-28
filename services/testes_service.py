from sqlalchemy import or_

from app import db
from app.models import (
    Ensaio,
    Testes,
    Horas,
    Templatenormas
)


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


def atualizar_horasesgotadas(teste_id):

    teste = Testes.query.get(teste_id)

    if not teste:
        return None

    info = calcular_horas_teste(teste)

    if not info:
        return None

    print("TESTE:", teste.id, "ESGOTADO:", teste.horasesgotadas)

    teste.horasesgotadas = info["horasesgotadas"]

    return info



def atualizar_todos_horasesgotadas():

    """
    Código temporário para marcar os testes antigos com horasesgotadas
    """

    total = 0

    for teste in Testes.query.all():

        info = atualizar_horasesgotadas(teste.id)

        if info is not None:
            total += 1

    db.session.commit()

    return total


def calcular_total_horas_disponiveis():

    testes = (
        Testes.query
        .join(Ensaio)
        .filter(
            Ensaio.anulado == False,
            Testes.horasesgotadas == 0
        )
        .all()
    )

    total = 0

    for teste in testes:

        info = calcular_horas_teste(teste)

        if not info:
            continue

        total += info["horas_disponiveis"]

    return round(total, 2)