from services.testes_service import (
    atualizar_horasesgotadas
)


def recalcular_teste_horas(teste_id):

    if not teste_id:
        return

    atualizar_horasesgotadas(
        teste_id
    )